from jinjafy.jinjafy import jinjafy_comment
from jinjafy.jinjafy import jinjafy_template
from jinjafy.jinja_matlab_load import matlab_load
from jinjafy.textools import mat2table
import subprocess
# from subprocess import subprocess

# def get_system_name():
#     if is_win():
#         return "Win"
#     if is_compute():
#         return "thinlinc.compute.dtu.dk"
#     if is_cogsys_cluster():
#         return "cogys cluster"

def execute_command(command, shell=True):
    if not isinstance(command, list):
        command = [command]
    # if not is_compute():
    # result = subprocess.run(command, stdout=subprocess.PIPE, shell=shell)
    # out = result.stdout
    # else:
    out = subprocess.check_output(command, shell=shell)
    s = out.decode("utf-8")
    OK = True
    return s, OK