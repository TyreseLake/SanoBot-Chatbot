from flask import Flask, request
import pandas as pd

data = pd.read_csv("illnesses.csv") #load the list of symptoms and illnesses

def getName(d):
  illness_dict = {
    "Fungal Infection":"a fungal infection",
    "Allergy":"an allergic reaction",
    "Common Cold":"the common cold",
    "Pneumonia":"pneumonia",
    "Diabetes":"diabetes",
    "Chicken Pox":"chicken pox"
  }
  if d in illness_dict:
    return illness_dict[d]
  else:
    return None
  
def isContagious(d):
  contagious_dict = {
    "Fungal Infection":1,
    "Allergy":0,
    "Common Cold":1,
    "Pneumonia":1,
    "Diabetes":0,
    "Chicken Pox":2
  }
  if d in contagious_dict:
    return contagious_dict[d]
  else:
    return None

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  #Extract request from dialogueflow
  req = request.get_json(silent=True, force=True)

  #set the default fullfillment responce text to nothing
  text = {}

  #Get the query result from the request
  query_result = req.get('queryResult')
  if query_result.get('action') == 'getSymptoms':
    #make one context with all symptoms as a paramter
    outputContexts = query_result.get('outputContexts')  #get the current output context

    symptoms = []
    for d in outputContexts:
      if d['name'].endswith("symptomslist"):
        symptoms = d['parameters'].get('symptomslist')

    userEnteredSymptoms = query_result.get('parameters').get('symptoms') #get the newly entered symptoms from the user

    newSymptoms = list(dict.fromkeys(symptoms + userEnteredSymptoms)) #combine the symptomsList and new symtpoms and remove duplicates

    newOutputContexts = []
    for d in outputContexts:
      if not d['name'].endswith("symptomslist"):
        newOutputContexts.append(d)

    newSymptomsListContext = { #create a new symptoms list context with the updated user entered symptoms
        "name": req.get('session')+"/contexts/symptomslist",
        "lifespanCount": 5,
        "parameters" : {"symptomslist" : newSymptoms}
        }
    
    newOutputContexts.append(newSymptomsListContext) #append the newly created symptoms list context to the new output contexts
    text = {
      "outputContexts": newOutputContexts
    }

  if query_result.get('action') == 'finishSymptoms':
    outputContexts = query_result.get('outputContexts')

    symptoms = []
    for d in outputContexts:
      if d['name'].endswith("symptomslist"):
        symptoms = d['parameters'].get('symptomslist')
        illnesses = [x[0] for x in data.values.tolist() if set(symptoms) <= set(x)]
        illnesses = list(dict.fromkeys(illnesses))
    if(illnesses == []):
      text = {
        "fulfillmentText": "Unfortunately, right now I am unable to determine whats wrong. We would need to run some tests first to figure out the issue."
      }
    else:
      statement = ""
      for x, illness in enumerate(illnesses):
        if x > 0:
          if x < len(illnesses)-1:
            statement += ", "
          else:
            statement += " or "
        statement += getName(illness)
      contagiousStatement = ""
      contagious = [isContagious(d) for d in illnesses]
      if max(contagious)==1:
        contagiousStatement = "This is mildly contagious, so avoid too much physical contact with anyone. "
      elif max(contagious)>1:
        contagiousStatement = "This is very contagious. Avoid being in close proximity to others and conact a doctor immediately. "
      text = {
        "fulfillmentText": "You may have " + statement + ". " + contagiousStatement + "Please be careful."
      }

  #return responce to dialogflow
  return text
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

