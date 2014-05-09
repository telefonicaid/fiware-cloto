__author__ = 'gjp'
import json


class information():

    def __init__(self, owner=None, windowsize=None, version=None, runningfrom=None, doc=None):
        self.owner = owner
        self.windowsize = windowsize
        self.version = version
        if runningfrom != None:
            self.runningfrom = runningfrom.strftime("%y/%m/%d %H:%M:%S")
        self.doc = doc

    def parse(self, d):
        """
        Convert from a dict to an information object.
        """
        try:
            self.windowsize = json.loads(d)['windowsize']
            return self
        except (ValueError, KeyError, TypeError):
            print ("error")
            return None

    def getVars(self):
        return vars(self)
