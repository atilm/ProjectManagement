import unittest
from projman.src.domain.completion_date_history import *

class AddingRecordsToTheCompletionDateHistory(unittest.TestCase):
    def test_when_a_record_is_added_an_existing_record_for_the_same_day_is_replaced(self):
        # given a history with two records
        history = CompletionDateHistory("projectId")
        firstInterval = ConfidenceInterval(datetime.date(2023, 11, 15), datetime.date(2023, 11, 16), datetime.date(2023, 11, 18))
        history.add(datetime.date(2023, 11, 1), firstInterval)
        secondInterval = ConfidenceInterval(datetime.date(2023, 11, 16), datetime.date(2023, 11, 17), datetime.date(2023, 11, 19))
        history.add(datetime.date(2023, 11, 2), secondInterval)

        # when another record is added for the same day as the second record
        thirdInterval = ConfidenceInterval(datetime.date(2023, 11, 17), datetime.date(2023, 11, 18), datetime.date(2023, 11, 21))
        history.add(datetime.date(2023, 11, 2), thirdInterval)

        # then the first entry remains and the second has been replaced
        self.assertEqual(len(history.records), 2)
        self.assertEqual(history.records[0].completion_date_interval, firstInterval)
        self.assertEqual(history.records[1].completion_date_interval, thirdInterval)
