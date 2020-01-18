import csv
import unittest

import parse

class TestParse(unittest.TestCase):
    FILES = ['data/inputFile1.csv', 'data/inputFile2.csv', 'data/inputFile3.csv']

    def test_parse_row(self):
        for filename in self.FILES:
            with open(filename) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[0]:
                        parse.parse_row(row)

    def test_parse_csv(self):
        for filename in self.FILES:
            with open(filename) as csv_file:
                parse.parse_csv(csv_file)

    def test_idempotent(self):
        for filename in self.FILES:
            with open(filename) as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[0]:
                        parsed = parse.parse_row(row)
                        if isinstance(parsed, parse.HourOut):
                            out_row = parsed.to_row()
                            parsed2 = parse.parse_row(out_row)
                            self.assertEqual(parsed, parsed2)




if __name__ == '__main__':
    unittest.main()

