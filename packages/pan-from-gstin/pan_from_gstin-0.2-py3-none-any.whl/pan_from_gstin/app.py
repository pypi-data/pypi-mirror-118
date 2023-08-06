# doing necessary imports
from logger_class import getLog
#from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
import re
logger = getLog('user1')
#app = Flask(__name__)  # initialising the flask app with the name 'app'
class GST:
    def __init__(self, gstin):
        self.gstin= gstin
    def pan_from_gstin(self):
        try:
            pattern = re.compile(r'(\d{2})([a-zA-Z]{5}\d{4}[a-zA-Z]{1})[1-9a-zA-Z]{1}[zZ]{1}[a-zA-Z\d]{1}')
            gst = re.search(pattern, self.gstin)
            if gst:
                logger.info("PAN for GSTIN %s is %s",self.gstin,gst.group(2))
                return gst.group(2)
            else:
                logger.info('Format of input GSTIN %s is incorrect, Please check it',self.gstin)
                return ('Check input GSTIN format')
        except Exception as e:
            logger.info("Exception has occurred for GSTIN %s Error message is ",self.gstin, +str(e))
            raise Exception("(pypi_project.py) - Something went wrong while getting gstin details\n" + str(e))

