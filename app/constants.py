import logging

logging_level_switcher={ 'CRITICAL':logging.CRITICAL, 'ERROR':logging.ERROR, 'WARNING':logging.WARNING, 'INFO':logging.INFO, 'DEBUG':logging.DEBUG, 'NOTSET':logging.NOTSET}
supported_ext = ["xls", "xlsx", "xlsm", "xlsb", "xltx", "xltm", "xls", "xlt", "xml", "xlam", "xla", "xlw", "xlr", "csv"]
location_header = ['CITY', 'COUNTRY', 'SUB_COUNTRY', 'LOCATION', 'DEPARTMENT']
