import json
import requests
import argparse
import sys
import logging


logger = logging.getLogger("APICalls.CreateGroup")


class CreateGroup:

	def __init__(self, URL, auth):
		self.URL = URL
		self.auth = auth
		self.appName=''
		self.groupName=''
		self.header = {"Content-type": "application/json", "Accept":"application/json"}

		logger.info("Initializing CreateGroup")
		logger.debug("URL: %s, auth: %s, appName: %s, groupName: %s, header: %s", self.URL, self.auth, self.appName, self.groupName, self.header)


	#Functionality to Check OA Controller. 
	def CheckController(self):
		try:
			URI = '/controller/rest/serverstatus'
			chkController = requests.get(self.URL+URI, auth=self.auth)
			logger.info("CreateGroup Controller Check Status: %d", chkController.status_code)
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

	# Create a Group, which is a collection of agents. 
	def CreateGroup(self):

		self.appName = self.AppManifestJSON['name']
		#self.appName = self.AppManifestJSON['rules'][0]['config']['application_name']

		self.groupName = self.removeSpace(self.appName)

		#Create cURL statement to create group in controller
		URI = '/controller/universalagent/v1/user/groups/byName/' + self.groupName

		#Edit the payload to insert the correct group name
		payload = {'name':self.groupName,'comments':'This group is for ' + self.groupName}

		logger.debug("AppName: %s, GroupName: %s, URI: %s, payload: %s", self.appName, self.groupName, URI, payload)

		#Convert dictionary to Json Object
		jsonData = json.dumps(payload)

		try:
			createGroup = requests.put(self.URL+URI, headers=self.header, auth=self.auth, data=jsonData)
		except requests.exceptions.RequestException as e:
			logger.debug(str(e))
			sys.exit(1)
		finally:
			logger.info("CreateGroup REST API Status: %d", createGroup.status_code)


	# Execute function should be called from APICalls.py
	def Execute(self, AppManifestJSONFile):

		self.AppManifestJSON = AppManifestJSONFile

		self.CheckController()
		self.CreateGroup()
