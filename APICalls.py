import json
import requests
import argparse
import AddAgents
from CreateGroup import CreateGroup
from CreateRuleBook import CreateRuleBook
from AddAgents import AddAgents
from AssociateRulebook import AssociateRulebook
from argparse import RawTextHelpFormatter
import logging
import logging.config
import os

manifest = ''

# Used only when executing this playbook from the command line
class HostVerification(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
    	import re
        if re.match('^[a-z]*:\/\/[^:]*$', values):
        	setattr(namespace, self.dest, values)
        else:
        	raise ValueError("Controller host invalid. Please enter a valid hostname.")

# Used only when executing this playbook from the command line
class PortVerification(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
    	import re
        if re.match('^\d*$', values):
        	setattr(namespace, self.dest, values)
        else:
        	raise ValueError("Controller Port invalid. Please enter a valid port.")

def CmdInit():

	logging.config.fileConfig('logging.conf')

	logger = logging.getLogger("APICalls")

	global manifest

	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

	parser.add_argument('--split', action='store', type=int, dest='splitAction',
	                    help='Usage includes splitting up REST API calls: \n Enter 1 for Create Group \n Enter 2 for Create RuleBook \n Enter 3 for Add Agents \n Enter 4 for Associate Rulebook')

	parser.add_argument('manifest', action='store', help='App Manifest file is required')

	parser.add_argument('--controller-host', required=True, action=HostVerification, dest='controllerHost',
                    help='Controller Host the Universal Agents will report to. \nFor Example - http://<controller_host>')
	parser.add_argument('--controller-port', required=True, action=PortVerification, dest='controllerPort',
                    help='Controller Port the Universal Agents will report to')
	parser.add_argument('--userName', required=True, action='store', dest='userName',
		help='Username required for executing the REST API calls. \nFormat is: <user_name>@<account_name> ')
	parser.add_argument('--password', required=True, action='store', dest='password',
		help='Password required for specified user executing the REST API calls ')

	args = parser.parse_args()
	manifest = args.manifest
	action = args.splitAction
	controllerHost = args.controllerHost
	controllerPort = args.controllerPort
	userName = args.userName
	password = args.password

	auth = (str(userName),str(password))
	URL = str(controllerHost) + ':' + str(controllerPort)

	jsonfile = open(manifest, "r")
	AppManifestJSON = json.load(jsonfile)


	if action == 1:
		logger.info("Calling CreateGroup. Action value is %d", action)
		createGroup = CreateGroup(URL,auth)
		createGroup.Execute(AppManifestJSON)
	elif action == 2:
		logger.info("Calling CreateRulebook. Action value is %d", action)
		createRuleBook = CreateRuleBook(URL,auth)
		createRuleBook.Execute(AppManifestJSON)
	elif action == 3:
		logger.info("Calling AddAgents. Action value is %d", action)
		addAgents = AddAgents(URL,auth)
		addAgents.Execute(AppManifestJSON)
	elif action == 4:
		logger.info("Calling AssociateRulebook. Action value is %d", action)
		associateRulebook = AssociateRulebook(URL,auth)
		associateRulebook.Execute(AppManifestJSON)
	else:
		logger.info("Calling CreateGroup, CreateRulebook, AddAgents, AssociateRulebook")

		createGroup = CreateGroup(URL,auth)
		createRuleBook = CreateRuleBook(URL,auth)
		addAgents = AddAgents(URL,auth)
		associateRulebook = AssociateRulebook(URL,auth)

		createGroup.Execute(AppManifestJSON)
		createRuleBook.Execute(AppManifestJSON)
		addAgents.Execute(AppManifestJSON)
		associateRulebook.Execute(AppManifestJSON)


if __name__ == '__main__':
	CmdInit()