from flask import Flask, request, render_template
import os
import dialogflow
import json
from google.api_core.exceptions import InvalidArgument

#add bot credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'static/sano-sinw-d733cd018a51.json'

DIALOGFLOW_PROJECT_ID = 'sano-sinw'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'sano_interface'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/home')
def sano_bot():
    return render_template('index.html')

@app.route('/botlink', methods=['POST'])
def create_item():
    data = request.get_json()
    message = data['message']

    #send message to dialog server
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    return response.query_result.fulfillment_text, 201

app.run(host='0.0.0.0', port=8080)