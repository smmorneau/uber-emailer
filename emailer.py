from flask import Flask, flash, jsonify, request, render_template
import json
import parser
import requests
import traceback

app = Flask(__name__)

# Load default config
app.config.update(dict(
    DEBUG=True
))

# Load config from an environment variable with path to settings.cfg
app.config.from_envvar('EMAILER_SETTINGS', silent=True)


@app.route('/', methods=['GET'])
def index():
    """ View for url '/' """
    return render_template('index.html')


@app.route('/email', methods=['GET', 'POST'])
def email():
    """ View for url '/email' """
    try:
        if request.method == 'POST':
            # validate that no fields are empty and emails are valid
            if not _validate_fields(request.json):
                return jsonify(result=('All fields are required. Please verify'
                                       ' that the emails you provided are '
                                       'valid.'), success=False)
            # strip html from body
            request.json['body'] = parser.strip_html(request.json['body'])
            response = send_mail(request.json)
            if response:
                return jsonify(result='Your email was sent.', success=True)
            else:
                return jsonify(result='There was an error sending your email.',
                               succes=False)
        else:  # GET
            if request.args.get('result') is not None:
                flash(request.args.get('result'))
            return render_template('email.html'), 200
    except:
        app.logger.error(traceback.format_exc())
        return "Error accessing '/email' endpoint", 500


def send_mail(data):
    """ Sends mail with mailgun or mandrill
        Returns success boolean """
    if app.config['DEFAULT_MAIL_SERVICE'] == "mailgun":
        return send_with_mailgun(data)
    elif app.config['DEFAULT_MAIL_SERVICE'] == "mandrill":
        return send_with_mandrill(data)
    else:
        raise Exception("Invalid option for DEFAULT_MAIL_SERVICE.")


def send_with_mailgun(data):
    """ Sends mail with data using mailgun
        Returns True if sent successfully, False otherwise
        On error, switches the configuration to Mandrill """
    app.logger.debug("Email sent with Mailgun")
    payload = {"from": data["from_name"] + "<" + data["from"] + ">",
               "to": data["to_name"] + "<" + data["to"] + ">",
               "subject": data["subject"], "text": data["body"]}
    request = requests.post(
        app.config['MAILGUN_URL'],
        auth=("api", app.config['MAILGUN_KEY']),
        data=payload
    )
    response = request.json()
    try:
        if response['message'] == "Queued. Thank you.":
            return True
    except:
        app.logger.error("Mailgun Error: " + str(response))
        # switch to mandrill
        app.logger.debug("Switch default to Mandrill")
        app.config['DEFAULT_MAIL_SERVICE'] = "mandrill"
    return False


def send_with_mandrill(data):
    """ Sends mail with data using mandrill
        Returns True if sent successfully, False otherwise
        On error, switches the configuration to Mailgun """
    app.logger.debug("Email sent with Mandrill")
    payload = {"key": app.config['MANDRILL_KEY'],
               "message": {"text": data["body"], "subject": data["subject"],
                           "from_email": data["from"],
                           "from_name": data["from_name"],
                           "to": [{"email": data["to"],
                                   "name": data["to_name"],
                                   "type": "to"}]
                           }
               }
    request = requests.post(app.config['MANDRILL_URL'],
                            data=json.dumps(payload))
    response = request.json()
    try:
        if response[0]['status'] == "sent":
            return True
        else:
            app.logger.warning("Mandrill Send Failed: " +
                               response[0]['reject_reason'])
    except:
        app.logger.error("Mandrill Error: " + str(response))
        # switch to mailgun
        app.logger.debug("Switch default to Mailgun")
        app.config['DEFAULT_MAIL_SERVICE'] = "mailgun"
    return False


def _validate_fields(fields):
    """ Returns True if all fields are given and email fields are valid,
        False otherwise """
    return (fields is not None and fields['to'] and fields['to_name'] and
            fields['from'] and fields['from_name'] and fields['subject'] and
            fields['body'] and parser.validate_email(fields['to']) and
            parser.validate_email(fields['from']))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
