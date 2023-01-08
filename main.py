from flask import Flask, render_template, jsonify
from flask import request

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial

from dotenv import load_dotenv
import os
import pprint as p

load_dotenv()

account_sid = os.environ[AC8b48cfa0f629200c0ece640400c22c71]
auth_token = os.environ[71eb9c2ac31e415cac70c5c91058ce1b]
api_key = os.environ[SK786f9cd701f92db9094e2118a9e106d4]
api_key_secret = os.environ[SXlqUXQLnqEVZxMTqS1Vh3afZ75HbrAJ]
twiml_app_sid = os.environ[AP37e2baf5905a9115cbf96dac243836fc]
twilio_number = os.environ[+16627677230]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'home.html',
        title="In browser calls",
    )


@app.route('/token', methods=['GET'])
def get_token():
    identity = twilio_number
    outgoing_application_sid = twiml_app_sid

    access_token = AccessToken(account_sid, api_key,
                               api_key_secret, identity=identity)

    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True,
    )
    access_token.add_grant(voice_grant)

    response = jsonify(
        {'token': access_token.to_jwt().decode(), 'identity': identity})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/handle_calls', methods=['POST'])
def call():
    p.pprint(request.form)
    response = VoiceResponse()
    dial = Dial(callerId=twilio_number)

    if 'To' in request.form and request.form['To'] != twilio_number:
        print('outbound call')
        dial.number(request.form['To'])
    else:
        print('incoming call')
        caller = request.form['Caller']
        dial = Dial(callerId=caller)
        dial.client(twilio_number)

    return str(response.append(dial))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
