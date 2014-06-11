uber-emailer
============

INSTALLATION
------------
$ pip install -r requirements.txt

If you do not have pip installed, manually install
- flask (http://flask.pocoo.org/docs/installation/)
- requests (http://docs.python-requests.org/en/latest/user/install/#install)


LANGUAGE AND FRAMEWORK CHOICE
-----------------------------
I chose Python because it is easy to get something running quickly. The amount of code to get a working prototype in Python is much less than, for example, in Java.
Flask was my framework of choice because I've been wanting to hack with it for a while, this seemed like the perfect opportunity. I liked that is minimalistic and seems to have only the barebones while suiting all my needs for a short-term project.


FUTURE IMPROVEMENTS
-------------------
If I had more time on this project, I would have improved my regexes for email validation. My current regex allows me to reject invalid emails, but is stricter than necessary as detailed in section 3.4.1 of RFC 2822. While email addresses may contain a wide variety of symbols, since most emails use only the characters in [-0-9a-zA-Z.+_], I am rejecting all other symbols.

If I had more time, I would also have given more detailed error messages to the user. For example, it is the same error message if the user leaves a field empty or gives an invalid email. The error message is also vague as to why an email failed to send if it passed validation.


CONFIG SETUP
------------
Replace the following values with your own in settings.cfg:
- your_secret_key
- your_mandrill_key
- your_mailgun_domain
- your_mailgun_key"

Set DEFAULT_MAIL_SERVICE to "mailgun" or "mandrill"


RUN APP
-------
$ export EMAILER_SETTINGS=/path/to/settings.cfg

$ python emailer.py


RUN TESTS
---------
$ python tests.py