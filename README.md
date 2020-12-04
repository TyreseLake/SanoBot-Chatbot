# SanoBot-Chatbot
SanoBot is a healthcare Chatbot developed by Hotfix2020 using Dialogflow. It was created inorder for users to describe symptoms and determine a list of potential illnesses user may have as well as information on how contagious these illnesses might be. The team developed this application using the SCRUM methodology.

![SanoBot](https://github.com/FadedHearts/SanoBot-Chatbot/blob/main/SanoBot.png)
## The SanoBot Architecture 
![SanoBot Architecture](https://raw.githubusercontent.com/FadedHearts/SanoBot-Chatbot/main/SanoBot%20Architecture.png "SanoBot Architecture")

## Setup
This Repository contains for main folders:
 - dialogflow-agent
 - webhook-integration
 - application-interface
 - webhook-integration-unit-tests
 
 _*Note:* Setting this up may reque knowlege of the python language and knowlege of FLASK servers_
 
### Dialogflow Agent
 1. Sign-u/Log-in to Dialogflow
 2. Select *Create New Agent*
 3. After creating an Agent, select settings for that agent
 4. Select the *Export and Import* tab
 5. Select *Import From Zip*
 6. Select the _Sano.zip_ file from the folder _dialogflow-agent_
 7. Select *Import*
 
### Webhook Integration
#### Repl.it 
 1. Create a new Repl.it python file
 2. Add the files from the  _webhook-integration_ directory
 3. Run the code and copy the web hook route url of your deployed server, e.g _https://repl.it/name/webhook_
 4. Go to the Dialogflow console and select Fulfillment from the left navigation menu.
 5. Enable Webhook > URL to the URL of the JSON file from the previous step, then select Save.
#### Firebase
 1. Sign-up/Login to Google account
 2. Create a Firebase project
 3. Deploy the _webhook-integration_ directory with Firebase hosting:
    - Follow the instructions to set up and initialize Firebase SDK for Cloud Functions. Make sure to select the project that you have previously generated in the Actions on Google Console and to reply N when asked to overwrite existing files by the Firebase CLI.
    - Run firebase deploy --only hosting and take note of the endpoint where the responses folder has been published. It should look like Hosting URL: https://${PROJECTID}.firebaseapp.com
 4. Select the correct JSON file for your Dialogflow fulfillment and take a note of the URL of the file (e.g. https://${PROJECTID}.firebaseapp.com/main.py/webhook)
 5. Go to the Dialogflow console and select Fulfillment from the left navigation menu.
 6. Enable Webhook > URL to the URL of the JSON file from the previous step, then select Save.

### Application Interface
 1. Set up the FLASK server in the _application-interface_ directory
 2. Run the server and navigate to the "/home" route
 3. Modify the python code to include your agents *key.json*
    - Go to your dialog flow agent
    - Go to settings and select the project id to navigate to the console.cloud page
    - Select *Go to project settings*
    - Create a new Service Account
    - Fillout the information and select *Create*
    - Add the role *Dialogflow API Client* or *Dialogflow API Admin*
    - Click _Continue_ then _Done_
    - Now to create your json key, select your new service account and select *Add Key*
    - Select the _JSON_ optionand select create and this will give u the key.json
 4. Add the key.json file to your FLASK servers static folder and modify the _main.py_ code and add the bot credentials, 'key.json', with ur new key file.
 5. Change the project id to the project id of your create agent
 6. Change the session id to somthing uniue, e.g. "my_session_id"
 
 ### Running Test Cases
 1. Add the *test_main.py* from the _webhook-integration-unit-tests_ directory to your main.py for your webhook inegration server.
 2. Install the "unittest" library in python
 3. Type the command "unittest -m test_main.py" to run the unit tests.
