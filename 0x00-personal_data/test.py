import unittest
import logging
from io import StringIO
from filtered_logger import get_logger, RedactingFormatter, filter_datum, PII_FIELDS


class TestLoggingModule(unittest.TestCase):

    def setUp(self):
        self.logger = get_logger()
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        handler.setFormatter(RedactingFormatter(PII_FIELDS))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def test_filter_datum(self):
        fields = ['name', 'email']
        redaction = '***'
        message = 'name=John; email=john.doe@example.com; ssn=123-45-6789;'
        separator = '; '
        expected_message = 'name=***; email=***; ssn=123-45-6789;'
        self.assertEqual(filter_datum(fields, redaction, message, separator), expected_message)

    def test_logger_name(self):
        self.assertEqual(self.logger.name, 'user_data')

    def test_logger_level(self):
        self.assertEqual(self.logger.level, logging.INFO)

    def test_propagate(self):
        self.assertFalse(self.logger.propagate)

    def test_log_redaction(self):
        self.logger.info('name=John Doe; email=john.doe@example.com; ssn=123-45-6789;')
        output = self.stream.getvalue().strip()
        expected_output = '[HOLBERTON] user_data INFO : name=***; email=***; ssn=***;'
        self.assertIn(expected_output, output)

    def test_empty_fields(self):
        message = 'name=John Doe; email=john.doe@example.com;'
        self.assertEqual(filter_datum([], '***', message, '; '), message)

    def test_empty_message(self):
        self.assertEqual(filter_datum(['name'], '***', '', '; '), '')

    def test_non_matching_fields(self):
        message = 'username=johndoe;'
        self.assertEqual(filter_datum(['name'], '***', message, '; '), message)

if __name__ == '__main__':
    unittest.main()

