__author__ = 'gjimenez'
import json, datetime


class information():
    d = datetime.datetime.now()

    def __init__(self):
        self.owner = 'Telefonica I+D'
        self.windowsize = 5
        self.version = 1.0
        self.runningfrom = self.d.strftime("%y/%m/%d %H:%M:%S")
        self.doc = 'http://wikis.hi.inet/boi/index.php/Dinge_API'

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
