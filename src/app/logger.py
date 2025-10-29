from enum import Enum


class LogType(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2


class Logger:
    def __init__(self, log_name):
        self.log_name = log_name

    def log(self, message, log_type="INFO", sender=None, params=None):
        with open(self.log_name, 'a', ) as log:
            end = ''
            date = str(datetime.datetime.now())
            if params:
                end = '{' + ', '.join([f"{k}: {params[k]}" for k in params.keys()]) + '}'
            if sender:
                log.write(f"({time}) FROM {sender} {log_type.value}: {message} {end}\n")
            else:
                log.write(f"({time}) {log_type.value}: {message} {end}\n")
    def info(self,message, sender=None, params=None):
        self.log(message, log_type=LogType.INFO, sender=sender, params=params)
    def warn(self, message, sender=None, params=None):
        self.log(message, log_type=LogType.WARNING, sender=sender, params=params)
    def error(self, message, sender=None, params=None):
        self.log(message, log_type=LogType.ERROR, sender=sender, params=params)