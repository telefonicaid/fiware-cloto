__author__ = 'artanis'

from subprocess import Popen
from time import sleep
from commons.configuration import REST_PATH, REST_PORT
from commons.constants import LITTLE_SLEEP


class EnvironmentUtils(object):

    def __init__(self):

        self.proc_policy_manager = None

    def start_policy_manager(self):

        self.proc_policy_manager = Popen(['python', REST_PATH, REST_PORT])
        sleep(LITTLE_SLEEP)

    def stop_policy_manager(self):

        if self.proc_policy_manager is not None:

            try:
                self.proc_policy_manager.terminate()
                sleep(LITTLE_SLEEP)
                if self.proc_policy_manager.wait() != 0:
                    self.proc_policy_manager.kill()
                self.proc_policy_manager = None

            except OSError:
                pass

        else:
            print 'Police Manager is not running'

    def police_manager_is_up(self):

        #There are two possibilities to know if the police manager is up. The first is using the process using the
        #Django port. Another option can be doing a requests to the server and checking the response. In my opinion the
        #better option is the second.

        pass
