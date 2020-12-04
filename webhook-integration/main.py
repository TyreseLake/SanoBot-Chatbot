from flask import Flask, request
import pandas as pd

data = pd.read_csv("illnesses.csv") #load the list of symptoms and illnesses

#this function gets a list of illnesses from inputted symptoms
def getIllnesses(symptoms):
  if not type(symptoms) is list:
    raise ValueError("Expected a List")
  illnesses = []
  illnesses = [x[0] for x in data.values.tolist() if set(symptoms) <= set(x)]
  illnesses = list(dict.fromkeys(illnesses))
  return illnesses
  
#this function gets the conversational name of a illness
def getName(d):
  if not type(d) is str:
    raise ValueError("Expected a String")
  illness_dict = {
    "Fungal Infection":"a fungal infection",
    "Allergy":"an allergic reaction",
    "Common Cold":"the common cold",
    "Pneumonia":"pneumonia",
    "Tuberculosis": "tuberculosis",
    "Diabetes":"diabetes",
    "Chicken Pox":"chicken pox",
    "Dengue":"dengue fever"
  }
  if d in illness_dict:
    return illness_dict[d]
  else:
    return None

#this function determines if an illness is contagious
def isContagious(d):
  if not type(d) is str:
    raise ValueError("Expected a String")
  contagious_dict = {
    "Fungal Infection":1,
    "Allergy":0,
    "Common Cold":1,
    "Pneumonia":1,
    "Tuberculosis": 2,
    "Diabetes":0,
    "Chicken Pox":2,
    "Dengue":0
  }
  if d in contagious_dict:
    return contagious_dict[d]
  else:
    return None

#this creates a response given a list of illnesses
def getIllnessResponse(illnesses):
  if not type(illnesses) is list:
    raise ValueError("Expected a List")
  if(illnesses == []):
    response = "Unfortunately, right now I am unable to determine whats wrong. We would need to run some tests first to figure out the issue."
  else:
    statement = ""
    for x, illness in enumerate(illnesses):
      if x > 0:
        if x < len(illnesses)-1:
          statement += ", "
        else:
          statement += " or "
      illnessName = getName(illness)
      if (illnessName is None):
        raise TypeError("Invalid illness such as NoneType")
      else:
        statement += illnessName
    contagiousStatement = ""
    contagious = [isContagious(d) for d in illnesses]
    if max(contagious)==1:
      contagiousStatement = "This may be mildly contagious, so avoid too much physical contact with anyone. "
    elif max(contagious)>1:
      contagiousStatement = "This may be very contagious. Avoid being in close proximity to others and contact a doctor immediately. "
    response = "You may have " + statement + ". " + contagiousStatement + "Please be careful."
  return response

#this removes a context from a list of contexts
def removeContext(outputContexts, context):
  if not type(outputContexts) is list:
    raise ValueError("Expected a List")

  if not type(context) is str:
    raise ValueError("Expected a String")

  newOutputContexts = []

  for d in outputContexts:
    if not type(d) is dict:
      raise ValueError("Expected a Dictionary")

    if 'name' not in d:
      raise ValueError("Expected a Dictionary with 'name' key")

    if not d['name'].endswith(context):
      newOutputContexts.append(d)

  return newOutputContexts

#gets a list of symptoms from output context
def getSymptomsFromContext(outputContexts):
  if not type(outputContexts) is list:
    raise ValueError("Expected a List")

  symptoms = []

  for d in outputContexts:
    if not type(d) is dict:
      raise ValueError("Expected a Dictionary")

    if 'name' not in d:
      raise ValueError("Expected a Dictionary with 'name' key")
      
    if d['name'].endswith("symptomslist"):
      symptoms = d['parameters'].get('symptomslist')

  return symptoms

app = Flask(__name__)

#default route
@app.route('/')
def hello_world():
    return "Hello world!"

#route used for dialog webhook requests    
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True) #Extract request from dialogueflow

  text = {} #set the default fullfillment response text to nothing

  query_result = req.get('queryResult') #Get the query result from the request

  outputContexts = query_result.get('outputContexts')  #get the current output context

  #if the intent uses the getSymptom function
  if query_result.get('action') == 'getSymptoms':
    #make one context with all symptoms as a parameter
    symptoms = getSymptomsFromContext(outputContexts)

    userEnteredSymptoms = query_result.get('parameters').get('symptoms') #get the newly entered symptoms from the user

    newSymptoms = list(dict.fromkeys(symptoms + userEnteredSymptoms)) #combine the symptomsList and new symtpoms and remove duplicates

    newSymptomsListContext = { #create a new symptoms list context with the updated user entered symptoms
      "name": req.get('session')+"/contexts/symptomslist",
      "lifespanCount": 5,
      "parameters" : {"symptomslist" : newSymptoms}
    }

    newOutputContexts = removeContext(outputContexts, "symptomslist") #remove the symptomslist context
    
    newOutputContexts.append(newSymptomsListContext) #append the newly created symptoms list context to the new output contexts
    text = {
      "outputContexts": newOutputContexts
    }

  #if the intent uses the finishSymptom function
  if query_result.get('action') == 'finishSymptoms':
    symptoms = getSymptomsFromContext(outputContexts)
    
    illnesses = getIllnesses(symptoms)
    
    statement = getIllnessResponse(illnesses)
    text = {
      "fulfillmentText": statement
    }

  #return response to dialogflow
  return text
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)