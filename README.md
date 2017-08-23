# AppDynamics-Universal-Agent-REST-Client


# Introduction
The AppDynamics Universal Agent REST Client is an automation tool for executing different workflows related to Universal Agent management. 

The AppDynamics Universal Agent REST Client is developed using python 2.7 on MACOSX. It is known to work on linux with python 2.7.x.

This repository contains four main python modules for executing the REST calls and one wrapper module.

To use the tool, execute the wrapper module "APICalls.py" as seen below.


# Usage

`python APICalls.py --controller-host <controller host> --controller-port <controller port> --userName <username>@<account name> --password <password> <Manifest File>`

Please note to provide the Manifest file as a positional argument. An example manifest file is found in this repository. 

# Prerequisites

The following modules are required in order to use the AppDynamics Universal Agent REST Client:

> - requests
> - json
> - argparse
> - logging
> - os
> - sys

# Support

For information on Universal Agent, please refer to the official [AppDynamics Documentation](https://docs.appdynamics.com/display/PRO43/AppDynamics+Universal+Agent)

For reporting issues, please use the GitHub Issues link.
