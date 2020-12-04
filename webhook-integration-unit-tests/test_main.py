#Unit Tests for SanoBot Webhook Backend

from unittest import TestCase
from main import getIllnesses, getName, isContagious, getIllnessResponse, removeContext, getSymptomsFromContext

class MainTest(TestCase):
    #--get illnesses test cases--
    def test_get_illness_valid_input(self):
        input = ["sneezing", "chills", "watering from eyes"]
        expect_output = ["Allergy"]
        self.assertEqual(getIllnesses(input), expect_output)
        input = ["itching", "a skin rash"]
        expect_output = ["Fungal Infection", "Chicken Pox"]
        self.assertEqual(getIllnesses(input), expect_output)
        input = ["non_symptom"]
        expect_output = []
        self.assertEqual(getIllnesses(input), expect_output)

    def test_get_illness_empty_input(self):
        input = []
        expect_output = ['Fungal Infection', "Allergy", 'Common Cold', 'Pneumonia', 'Diabetes', 'Chicken Pox', 'Dengue', 'Tuberculosis']
        self.assertEqual(getIllnesses(input), expect_output)

    def test_get_illness_invalid_input(self):
        with self.assertRaises(ValueError) as E:
            i = getIllnesses("string")
        with self.assertRaises(ValueError) as E:
            i = getIllnesses(None)
        with self.assertRaises(ValueError) as E:
            i = getIllnesses(10)
    
    #--get name test cases--
    def test_get_name_valid_input(self):
        input = "Allergy"
        expect_output = "an allergic reaction"
        self.assertEqual(getName(input), expect_output)
        input = "non_illness"
        expect_output = None
        self.assertEqual(getName(input), expect_output)
    
    def test_get_name_invalid_input(self):
        with self.assertRaises(ValueError) as E:
            i = getName(["list"])
        with self.assertRaises(ValueError) as E:
            i = getName(None)
        with self.assertRaises(ValueError) as E:
            i = getName(10)

    #--get name test cases--
    def test_is_contagious_valid_input(self):
        input = "Allergy"
        expect_output = 0
        self.assertEqual(isContagious(input), expect_output)
        input = "non_illness"
        expect_output = None
        self.assertEqual(isContagious(input), expect_output)
    
    def test_is_contagious_invalid_input(self):
        with self.assertRaises(ValueError) as E:
            i = isContagious(["list"])
        with self.assertRaises(ValueError) as E:
            i = isContagious(None)
        with self.assertRaises(ValueError) as E:
            i = isContagious(10)

    #--get illness response test cases--
    def test_get_illness_response_valid_input(self):
        input = ["Fungal Infection", "Chicken Pox"]
        expect_output = "You may have a fungal infection or chicken pox. This may be very contagious. Avoid being in close proximity to others and contact a doctor immediately. Please be careful."
        self.assertEqual(getIllnessResponse(input), expect_output)
        input = ["Diabetes"]
        expect_output = "You may have diabetes. Please be careful."
        self.assertEqual(getIllnessResponse(input), expect_output)
    
    def test_get_illness_response_invalid_illness(self):
        input = ["non_symptom"]
        with self.assertRaises(TypeError) as E:
            i = getIllnessResponse(input)

    def test_get_illness_response_empty_input(self):
        input = []
        expect_output = "Unfortunately, right now I am unable to determine whats wrong. We would need to run some tests first to figure out the issue."
        self.assertEqual(getIllnessResponse(input), expect_output)

    def test_get_illness_response_invalid_input(self):
        with self.assertRaises(ValueError) as E:
            i = getIllnessResponse("string")
        with self.assertRaises(ValueError) as E:
            i = getIllnessResponse(None)
        with self.assertRaises(ValueError) as E:
            i = getIllnessResponse(10)

    #--remove context test cases--
    def test_remove_context_valid_input(self):
        input1 = [{'name': 'session_name/context1', 'value': 1}, {'name': 'session_name/context2', 'value': 1}, {'name': 'session_name/context3', 'value': 1}]
        input2 = 'context2'
        expect_output = [{'name': 'session_name/context1', 'value': 1}, {'name': 'session_name/context3', 'value': 1}]
        self.assertEqual(removeContext(input1, input2), expect_output)
        input1 = [{'name': 'session_name/context1', 'value': 1}, {'name': 'session_name/context2', 'value': 1}, {'name': 'session_name/context3', 'value': 1}]
        input2 = 'noncontext'
        expect_output = [{'name': 'session_name/context1', 'value': 1}, {'name': 'session_name/context2', 'value': 1}, {'name': 'session_name/context3', 'value': 1}]
        self.assertEqual(removeContext(input1, input2), expect_output)
        
    def test_remove_context_empty_input(self):
        input1 = []
        input2 = 'context'
        expect_output = []
        self.assertEqual(removeContext(input1, input2), expect_output)

    def test_remove_context_invalid_input(self):
        with self.assertRaises(ValueError) as E:
            c = removeContext("string", "string")
        with self.assertRaises(ValueError) as E:
            c = removeContext("string", 5)
        with self.assertRaises(ValueError) as E:
            c = removeContext(["non dict"], "string")

    #--get symptoms from context test cases--
    def test_get_symptoms_from_context_valid_input(self):
        input1 = [{'name': 'session_name/symptomslist', 'parameters': {"symptomslist" : ["symptom1", "symptom2"]}}]
        expect_output = ["symptom1", "symptom2"]
        self.assertEqual(getSymptomsFromContext(input1), expect_output)
        input1 = [{'name': 'session_name/othercontext', 'parameters': {"otherparameter" : ["value1", "value2"]}}]
        expect_output = []
        self.assertEqual(getSymptomsFromContext(input1), expect_output)
        
    def test_get_symptoms_from_context_empty_input(self):
        input1 = []
        expect_output = []
        self.assertEqual(getSymptomsFromContext(input1), expect_output)

    def test_get_symptoms_from_context_invalid_input(self):
        with self.assertRaises(ValueError) as E:
            c = getSymptomsFromContext("string")
        with self.assertRaises(ValueError) as E:
            c = getSymptomsFromContext(["non dict"])
        