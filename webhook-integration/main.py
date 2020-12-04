from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  #Extract request from dialogueflow 
  req = request.get_json(silent=True, force=True)

  #set the default fullfillment responce text to nothing
  text = {"fulfillmentText": ""}

  #Get the query result from the request
  query_result = req.get('queryResult')
  if query_result.get('action') == 'initialSymptom.sneezing':
    text = {
        "fulfillmentText": "Alright, have you also been experiencing shivers?",
        "outputContexts": [
            {
                "name": req.get('session')+"/contexts/shiveringQuery",
                "lifespanCount": 5
            }
        ],
        "fulfillmentMessages": [{
            "payload": {
                "message": "Alright, have you also been experiencing shivers?",
                "platform": "kommunicate",
                "metadata": {
                    "contentType": "300",
                    "templateId": "6",
                    "payload": [{
                        "title": "Yes",
                        "message": "Yes"
                    }, {
                        "title": "No ",
                        "message": "No"
                    }]
                }
            }
        }]
    }
  elif query_result.get('action') == 'initialSymptom.coughing':
    text = {
      "fulfillmentText": "Okay, do you get a runny nose often?",
      "outputContexts": [
            {
                "name": req.get('session')+"/contexts/coughingQuery",
                "lifespanCount": 5
            }
        ],
      "fulfillmentMessages": [{
          "payload": {
              "message": "Okay, do you get a runny nose often?",
              "platform": "kommunicate",
              "metadata": {
                  "contentType": "300",
                  "templateId": "6",
                  "payload": [{
                      "title": "Yes",
                      "message": "Yes"
                  }, {
                      "title": "No ",
                      "message": "No"
                  }]
              }
            }
        }]
    }
  elif query_result.get('action') == 'nextSymptom.shivering':
    status = query_result.get('parameters').get('status')
    if status == "true":
      text = {
        "fulfillmentText": "Im sorry, you may have a cold!",
        "fulfillmentMessages": [{
          "payload": {
              "message": "Im sorry, you may have a cold!",
              "platform": "kommunicate"
            }
          }]
      }
    elif status == "false":
      text = {
        "fulfillmentText": "You will be okay, get some rest.",
        "fulfillmentMessages": [{
          "payload": {
              "message": "You will be okay, get some rest.",
              "platform": "kommunicate"
            }
          }]
        }
  elif query_result.get('action') == 'nextSymptom.coughing':
    status = query_result.get('parameters').get('status')
    if status == "true":
      text = {
        "fulfillmentText": "Oh no, you may be getting the virus!",
        "fulfillmentMessages": [{
          "payload": {
              "message": "Oh no, you may be getting the virus!",
              "platform": "kommunicate"
            }
          }]
      }
    elif status == "false":
      text = {
        "fulfillmentText": "Get some rest. Let me know if things get worse.",
        "fulfillmentMessages": [{
          "payload": {
              "message": "Get some rest. Let me know if things get worse.",
              "platform": "kommunicate"
            }
          }]
        }

  #return responce to dialogflow
  return text
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

"""
  #dialogflow_response = DialogflowResponse("Have you been experiencing shivering?")
  #dialogflow_response.add(Suggestions(["Yes","No"]))
  #dialogflow_response.add(SystemIntent("actions.intent.Default_Welcome_Intent"))
  #return dialogflow_response.get_final_response()

text = {
    "fulfillmentText": "render a text message from webhook",
    "fulfillmentMessages": [{
        "payload": {
            "message": "render a Actionable message from webhook",
            "platform": "kommunicate",
            "metadata": {
                "contentType": "300",
                "templateId": "6",
                "payload": [{
                    "title": "Yes",
                    "message": "Cool! send me more."
                }, {
                    "title": "No ",
                    "message": "Don't send it to me again"
                }]
            }
        }
    }, {
        "text": {
            "text": ["render array of  text message from webhook"]
        }
    }]
}
"""