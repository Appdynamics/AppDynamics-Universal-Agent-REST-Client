import json
import requests
import argparse
import logging


logger = logging.getLogger("APICalls.CreateRuleBook")

class CreateRuleBook:

	def __init__(self, URL, auth):
		self.URL = URL
		self.auth = auth
		self.appName=''
		self.ruleBook=''
		self.header = {"Content-type": "application/json", "Accept":"application/json"}

		logger.info("Initializing CreateRuleBook")
		logger.debug("URL: %s, auth: %s, appName: %s, rulebBok: %s, header: %s", self.URL, self.auth, self.appName, self.ruleBook, self.header)

	#Functionality to Check OA Controller. 
	def CheckController(self):
		try:
			URI = '/controller/rest/serverstatus'
			chkController = requests.get(self.URL+URI, auth=self.auth)
			logger.info("CreateRulebook Controller Check Status: %d", chkController.status_code)
		except requests.exceptions.RequestException as e:
			logger.debug(str(e))  
			sys.exit(1)

	def removeSpace(self,string):
		stringArray = string.split(' ')
		stringLength = len(stringArray)
		if stringArray != 0:
			string =''
			for x in range (0,stringLength):
				string = string + stringArray[x]

		logger.debug("Final string: %s", string)

		return string

	# Creating Rulebook 
	def CreateRuleBook(self):

		monitorRules = []

		self.appName = self.AppManifestJSON['name']
		#self.appName = self.AppManifestJSON['rules'][0]['config']['application_name']

		self.ruleBook = self.removeSpace(self.appName)
		
		# Read all rules from the template file and iteratively add it to the rulebook
		javaRuleLength = len(self.AppManifestJSON['rules'])

		for rule in range(0, javaRuleLength):
			monitorRules.append(self.AppManifestJSON['rules'][rule])

		payload =  {
		 'name': self.ruleBook,
		 'comments': self.AppManifestJSON['comments'],
		 'config': self.AppManifestJSON['config'],
		 'rules': monitorRules
		}

		URI = '/controller/universalagent/v1/user/rulebooks/byName/' + self.ruleBook

		logger.debug("AppName: %s, RuleBook: %s, URI: %s, payload: %s", self.appName, self.ruleBook, URI, payload)

		jsonData = json.dumps(payload)

		try:
			createRuleBook = requests.put(self.URL+URI, headers=self.header, auth=self.auth, data=jsonData)
		except requests.exceptions.RequestException as e:
			logger.debug(str(e))
			sys.exit(1)
		finally:
			logger.info("CreateRuleBook REST API Status: %d", createRuleBook.status_code)


	# Execute function should be called from APICalls.py
	def Execute(self,AppManifestJSONFile):
		self.AppManifestJSON = AppManifestJSONFile
		self.CheckController()
		self.CreateRuleBook()

