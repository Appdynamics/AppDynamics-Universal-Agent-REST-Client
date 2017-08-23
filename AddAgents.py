import json
import requests
import argparse
import logging

logger = logging.getLogger("APICalls.AddAgents")

class AddAgents:

	def __init__(self,URL,auth):
		self.URL = URL
		self.auth = auth
		self.header = {"Content-type": "application/json", "Accept":"application/json"}
		self.UAhosts = ''
		self.AppManifestJSON = ''
		self.hosts = []

		logger.info("Initializing AddAgents")
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
			logger.info("AddAgents Controller Check Status: %d", chkController.status_code)


	def removeSpace(self,string):
		stringArray = string.split(' ')
		stringLength = len(stringArray)
		if stringArray != 0:
			string =''
			for x in range (0,stringLength):
				string = string + stringArray[x]

		logger.debug("Final string: %s", string)

		return string

	def AddAgents(self):

		appName = self.AppManifestJSON['name']
		#appName = self.AppManifestJSON['rules'][0]['config']['application_name']
		groupName = self.removeSpace(appName)

		self.UAhosts = self.AppManifestJSON['hosts']

		logger.debug("AppName: %s, GroupName: %s, UAhosts: %s", appName, groupName, self.UAhosts)

		for hostName in self.UAhosts:
			if not hostName in self.hosts:
				self.hosts.append(hostName)
				URI = '/controller/universalagent/v1/user/agents/membership/' + hostName + '/groups/' + groupName
				try:
					addAgent = requests.put(self.URL+URI, headers=self.header, auth=self.auth)
				except requests.exceptions.RequestException as e:
					logger.debug(str(e))
					sys.exit(1)
				finally:
					logger.info("AddAgents REST API Status: %d for hostname: %s", addAgent.status_code, hostName)
		self.ValidateAgentAddition(groupName)

	# Validating that the agents specified for addition have infact been added
	def ValidateAgentAddition(self,groupName):
		URI = '/controller/universalagent/v1/user/agents/?groups=' + groupName

		try:
			r = requests.get(self.URL+URI, headers=self.header, auth=self.auth)
		except requests.exceptions.RequestException as e:
			logger.debug(str(e))
			sys.exit(1)
		finally:
			logger.info("ValidateAgentAddition REST API Status: %d", r.status_code)


		jsonFormat = json.dumps(r.json())
		hostLength = len(self.hosts)

		for x in range(0,hostLength):
			if not self.hosts[x] in jsonFormat:
				logger.debug("Agent %s not found in group", self.hosts[x])

	# Execute function should be called from APICalls.py
	def Execute(self,AppManifestJSONFile):
		#global AppManifestJSON

		self.AppManifestJSON = AppManifestJSONFile
		self.CheckController()
		self.AddAgents()
