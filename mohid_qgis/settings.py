from pathlib import Path

LOGGING = {
    'version': 1,
    'formatters': {
        'console': {
            'format': '[%(asctime)s]:[%(module)s]:[%(levelname)s]: - %(message)s',
            'datefmt': '%H:%M:%S'
        },
        'file': {
            'format': '[%(asctime)s]:[%(name)s]:[%(levelname)s] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': str(Path(__file__).parent.absolute()/"mohid_qgis.log")
        },
    },
    'loggers':{
        'mohid_qgis.plugin': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'mohid_qgis.core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    }
}