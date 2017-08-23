import logging
import random
import os

class myFileHandler(logging.FileHandler):
    def __init__(self,fileName,mode):

    	path = os.path.dirname(os.path.realpath(__file__))
        path = path+"/log"

        if not os.path.isdir(path):
        	os.mkdir(path)
        
        super(myFileHandler,self).__init__(path+"/"+fileName,mode)