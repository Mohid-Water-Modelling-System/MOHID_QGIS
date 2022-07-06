from typing import Optional, List
import os
import sys
import signal

from PyQt5.QtCore import  QThread, pyqtSignal

from mohid_qgis.core.program import runExternalProgram

_THREADS = [] # type: List[QThread]

class ProgramThread(QThread):
    output = pyqtSignal(str)

    def __init__(self, path: str, args: Optional[List[str]] = None) -> None:
        super().__init__()
        self.path = path
        self.pid = -1
        self.error = None
        self.exc_info = None
        self.args = args

        # need to keep reference alive while thread is running
        _THREADS.append(self)

    def run(self):
        try:
            runExternalProgram(self.path, self.args)
        except:
            self.exc_info = sys.exc_info()

    # def kill_program(self):
    #     if self.pid == -1:
    #         raise UserError('Program not started yet')
    #     os.kill(self.pid, signal.SIGTERM)