from flask import json
import emailer
import parser
import unittest


class EmailerTestCase(unittest.TestCase):
    """ Tests the emailer functionality """

    def setUp(self):
        emailer.app.config['TESTING'] = True
        self.app = emailer.app

    def test_email_mandrill(self):
        """ Tests an email send with Mandrill """
        self.app.config['DEFAULT_MAIL_SERVICE'] = "mandrill"
        payload = {
            'to': "fake@example.com",
            'to_name': "Ms. Fake",
            'from': "noreply@uber.com",
            'from_name': "Uber",
            'subject': "A Message from Uber",
            'body': "<h1>Your Bill</h1><p>$10</p>"
        }
        with self.app.test_request_context('/email', method='POST'):
            with self.app.test_client() as c:
                response = c.post('/email', data=json.dumps(payload),
                                  content_type='application/json')
                response_data = json.loads(response.get_data())
                assert response_data['success'] is True

    def test_email_mailgun(self):
        """ Tests an email send with Mailgun """
        self.app.config['DEFAULT_MAIL_SERVICE'] = "mailgun"
        payload = {
            'to': "fake@example.com",
            'to_name': "Ms. Fake",
            'from': "noreply@uber.com",
            'from_name': "Uber",
            'subject': "A Message from Uber",
            'body': "<h1>Your Bill</h1><p>$10</p>"
        }
        with self.app.test_request_context('/email', method='POST'):
            with self.app.test_client() as c:
                response = c.post('/email', data=json.dumps(payload),
                                  content_type='application/json')
                response_data = json.loads(response.get_data())
                assert response_data['success'] is True

    def test_email_missing_field(self):
        """ Tests an email send with a field missing """
        payload = {
            'to': "fake@example.com",
            'to_name': "",  # missing field
            'from': "noreply@uber.com",
            'from_name': "Uber",
            'subject': "A Message from Uber",
            'body': "<h1>Your Bill</h1><p>$10</p>"
        }
        with self.app.test_request_context('/email', method='POST'):
            with self.app.test_client() as c:
                response = c.post('/email', data=json.dumps(payload),
                                  content_type='application/json')
                response_data = json.loads(response.get_data())
                assert response_data['success'] is False
                assert "field" in response_data['result']

    def test_email_invalid_email(self):
        """ Tests an email send with an invalid email """
        payload = {
            'to': "Ms. Fake",  # invalid email (to fields switched)
            'to_name': "fake@example.com",
            'from': "noreply@uber.com",
            'from_name': "Uber",
            'subject': "A Message from Uber",
            'body': "<h1>Your Bill</h1><p>$10</p>"
        }
        with self.app.test_request_context('/email', method='POST'):
            with self.app.test_client() as c:
                response = c.post('/email', data=json.dumps(payload),
                                  content_type='application/json')
                response_data = json.loads(response.get_data())
                assert response_data['success'] is False
                assert "email" in response_data['result']


class ParserTestCase(unittest.TestCase):
    """ Tests html stripping and email validation """

    def test_strip_simple(self):
        """ Tests simple html stripping """
        text = "<h1>Your Bill</h1><p>$10</p>"
        cleaned_text = "Your Bill $10"
        assert parser.strip_html(text) == cleaned_text

    def test_strip_html_complex(self):
        """ Tests complex email stripping """
        with open("testdata/test-strip-html.html") as original:
            with open("testdata/test-strip-html-clean.txt") as cleaned:
                dirty_text = original.read()
                cleaned_text = cleaned.read()
                assert cleaned_text == parser.strip_html(dirty_text)

    def test_validate_emails(self):
        """ Tests email validation """
        email_tests = [("email", False),
                       ("@email", False),
                       ("_Steely.Morneau@uber.com", True),
                       (".steely@uber.com", False),
                       ("st..eely@uber.com", False),
                       ("steely.@uber.com", False),
                       (".@uber.com", False),
                       ("Steely.Morneau5@uber.com", True),
                       ("Steely Morneau@uber.com", False)]

        for index, (email, is_valid) in enumerate(email_tests):
            assert parser.validate_email(email) == is_valid, (
                "%s (%d); expected %s." % (email, index, is_valid))


if __name__ == '__main__':
    unittest.main()
