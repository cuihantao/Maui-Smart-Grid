#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

from mecoconfig import MECOConfiger
from mecodbutils import MECODBUtil
from mecologger import MECOLogger


class MECODupeChecker(object):
    """
    Check for duplicate data in the database.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = MECOLogger(__name__, 'debug')
        self.mecoConfig = MECOConfiger()
        self.currentReadingID = 0
        self.dbUtil = MECODBUtil()


    def readingBranchDupeExists(self, conn, meterName, endTime, channel = None,
                                DEBUG = False):
        """
        Duplicate cases:
        1. meterID and endTime combination exists in the database.
            @deprecated in favor of full meterName-endTime-channel query

        2. meterID, endTime, channel combination exists in the database.

        :param conn: database connection
        :param meterID: Meter name in MeterData table
        :param endTime: End time in Interval table
        :param channel: Required parameter that was previously optional. An
        optional channel is now deprecated.
        :return: True if combo exists, False if not.
        """

        dbCursor = conn.cursor()

        if DEBUG:
            print "readingBranchDupeExists():"

        if channel != None:
            sql = """SELECT	"Interval".end_time,
                        "MeterData".meter_name,
	                    "MeterData".meter_data_id,
	                    "Reading".channel,
	                    "Reading".reading_id
                 FROM "MeterData"
                 INNER JOIN "IntervalReadData" ON "MeterData".meter_data_id =
                  "IntervalReadData".meter_data_id
                 INNER JOIN "Interval" ON "IntervalReadData"
                 .interval_read_data_id = "Interval".interval_read_data_id
                 INNER JOIN "Reading" ON "Interval".interval_id = "Reading"
                 .interval_id
                 WHERE "Interval".end_time = '%s' and meter_name = '%s' and
                 channel = '%s'""" % (
                endTime, meterName, channel)

        else: # deprecated query
            sql = """SELECT	"Interval".end_time,
                        "MeterData".meter_name,
	                    "MeterData".meter_data_id
                 FROM "MeterData"
                 INNER JOIN "IntervalReadData" ON "MeterData".meter_data_id =
                  "IntervalReadData".meter_data_id
                 INNER JOIN "Interval" ON "IntervalReadData"
                 .interval_read_data_id = "Interval".interval_read_data_id
                 WHERE "Interval".end_time = '%s' and meter_name = '%s'""" % (
                endTime, meterName)

        self.dbUtil.executeSQL(dbCursor, sql)
        rows = dbCursor.fetchall()

        if len(rows) > 0:
            assert len(
                rows) < 2, "dupes should be less than 2, found %s: %s" % (
                len(rows), rows)
            if channel and len(rows) == 1 and \
                    self.mecoConfig.configOptionValue("Debugging", 'debug'):
                print "Found %s existing matches in \"Reading\"." % len(rows)
                print "rows = ",
                print rows

                self.currentReadingID = self.getLastElement(rows[0])
                print "reading id = %s" % self.currentReadingID

            # self.logger.log(
            #     "Duplicate found for meter %s, end time %s, channel %s." % (
            #         meterName, endTime, channel), 'debug')

            return True
        else:
            self.logger.log(
                "Found no rows for meter %s, end time %s, channel %s." % (
                    meterName, endTime, channel), 'debug')
            return False


    def getLastElement(self, rows):
        """
        Get the last element in a collection.

        Example:
            rows = (element1, element2, element3)
            getLastElement(rows) # return element3

        :param rows Result froms from a query
        :return last element in the collection
        """

        for i, var in enumerate(rows):
            if i == len(rows) - 1:
                return var


    def readingValuesAreInTheDatabase(self, conn, readingDataDict):
        """
        Given a reading ID, verify that the values associated are present
        in the database.

        Values are from the columns:
            1. channel
            2. raw_value
            3. uom
            4. value

        :param dictionary containing reading values
        :return True if the existing values are the same, otherwise return False
        """

        dbCursor = conn.cursor()

        sql = """SELECT "Reading".reading_id,
                        "Reading".channel,
                        "Reading".raw_value,
                        "Reading".uom,
                        "Reading"."value"
                 FROM "Reading"
                 WHERE "Reading".reading_id = %s""" % (self.currentReadingID)

        self.dbUtil.executeSQL(dbCursor, sql)
        rows = dbCursor.fetchall()

        if self.currentReadingID == 0:
            return False

        # assert len(rows) == 1 or len(rows) == 0
        assert len(rows) == 1, "Didn't find a matching reading for reading ID %s." % self.currentReadingID
        if len(rows) == 1:
            print "Found %s existing matches." % len(rows)
            print "rows = %s" % rows

            print "dict:"
            for key in readingDataDict.keys():
                print key, readingDataDict[key]
            print "row:"
            index = 0
            for item in rows[0]:
                print "index %s: %s" % (index, item)
                index += 1

            allEqual = True
            if int(readingDataDict['Channel']) == int(rows[0][1]):
                print "channel equal,"
            else:
                print "channel not equal: %s,%s,%s" % (
                    int(readingDataDict['Channel']), int(rows[0][1]),
                    readingDataDict['Channel'] == rows[0][1])
                allEqual = False

            if int(readingDataDict['RawValue']) == int(rows[0][2]):
                print "raw value equal,"
            else:
                print "rawvalue not equal: %s,%s,%s" % (
                    int(readingDataDict['RawValue']), int(rows[0][2]),
                    readingDataDict['RawValue'] == rows[0][2])
                allEqual = False

            if readingDataDict['UOM'] == rows[0][3]:
                print "uom equal,"
            else:
                print "uom not equal: %s,%s,%s" % (
                    readingDataDict['UOM'], rows[0][3],
                    readingDataDict['UOM'] == rows[0][3])
                allEqual = False

            if self.approximatelyEqual(float(readingDataDict['Value']), float(rows[0][4]), 0.001):
                print "value equal"
            else:
                print "value not equal: %s,%s,%s" % (
                    float(readingDataDict['Value']), float(rows[0][4]),
                    readingDataDict['Value'] == rows[0][4])
                allEqual = False

            if allEqual:
                print "all are equal"
                return True
            else:
                print "NOT all are equal!"
                print rows[0][1], rows[0][2], rows[0][3], rows[0][4]
                return False
        else:
            return False


    def approximatelyEqual(self, a, b, tolerance):
        return abs(a - b) < tolerance

