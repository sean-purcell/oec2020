import csv
import unittest

import parse

class TestParse(unittest.TestCase):

    def test_stupid(self):
        with open('data/inputFile1.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0]:
                    parse.parse_row(row)

        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()

