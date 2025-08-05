import logging

class LogUtil:
    def __init__(self):
        self.log = logging
        self.configure()
        pass
    def configure(self):
        self.log.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')