import logging
import os
import subprocess
from typing import Optional, List

logger = logging.getLogger(__name__)

def runExternalProgram(exePath: str, exeArgs: Optional[List[str]]):
    """ TODO: support windows external programs for now """

    args = [exePath]
    if exeArgs:
        args.append(*args)
    process = subprocess.Popen(args, cwd=os.get_cwd(),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             bufsize=1, universal_newlines=True)
    
    for line in process.stdout:
        logger.debug(line)
    
    process.wait()