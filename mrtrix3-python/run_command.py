import subprocess

def run_command(command):
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = p.communicate()
    return(output,error)