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
    process = subprocess.Popen(args, cwd=os.path.dirname(exePath),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            bufsize=1, universal_newlines=True)
    
    output = "Digital Terrain Creator output:\n"
    for line in process.stdout:
        output += line
    logger.info(output)
    
    process.wait()