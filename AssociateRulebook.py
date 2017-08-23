import json
import requests
import argparse
import logging

logger = logging.getLogger("APICalls.AssociateRulebook")

class AssociateRulebook:

	def __init__(self,URL,auth):
		self.URL = URL
		self.auth = auth
		self.header = {"Content-type": "application/json", "Accept":"application/json"}
		self.appName = ''
		self.groupName = ''
		self.ruleBook = ''
		self.AppManifestJSON = ''


		logger.info("Initializing AssociateRulebook")
		logger.debug("URL: %s, auth: %s, header: %s", self.URL, self.auth, self.header)

	#Functionality to Check OA Controller. 
	def CheckController(self):
		try:
			URI = '/controller/rest/serverstatus'
			chkController = requests.get(self.URL+URI, auth=self.auth)
		except requests.exceptions.RequestException as e:
			logger.debug(str(e))
			sys.exit(1)
		finally:
			logger.info("AssociateRulebook Controller Check Status: %d", chkController.status_code)

	def removeSpace(self,string):
		stringArray = string.split(' ')
		stringLength = len(stringArray)
		if stringArray != 0:
			string =''
			for x in range (0,stringLength):
				string = string + stringArray[x]

		logger.debug("Final string: %s", string)

		return string

	# Associate the Rulebook to the Group. 
	# Assumption is that the Group and Rulebooks previously created are named using the Application Name (removing any spaces)
	def AssociateRuleBook(self):

		# If this is being called from APICalls.py, retreive group and rulebook name. Group and Rulebook Names will be same as the Application Name
		#self.appName = self.AppManifestJSON['rules'][0]['config']['application_name']
		self.appName = self.AppManifestJSON['name']

		# Removing the spaces as it simplifies when making REST API Calls
		self.groupName = self.removeSpace(self.appName)
		self.ruleBook = self.removeSpace(self.appName)

		URI = '/controller/universalagent/v1/user/rulebooks/current/' + self.groupName
		
		#Edit the payload to insert the correct group name
		payload = {'ruleBookName': self.ruleBook}

		logger.debug("AppName: %s, RuleBook: %s, GroupName: %s, URI: %s, payload: %s", self.appName, self.ruleBook, self.groupName, URI, payload)

		#Convert dictionary to Json Object
		jsonData = json.dumps(payload)

		try:
			associateRulebook = requests.put(self.URL+URI, headers=self.header, auth=self.auth, data=jsonData)
		except requests.exceptions.RequestException as e:
			logger.debug(str(e))
			sys.exit(1)
		finally:
			logger.info("AssociateRulebook REST API Status: %d", associateRulebook.status_code)

	# Execute function should be called from APICalls.py
	def Execute(self,AppManifestJSONFile):
		#global AppManifestJSON

		self.AppManifestJSON = AppManifestJSONFile
		self.CheckController()
		self.AssociateRuleBook()