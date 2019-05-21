import subprocess

def run_code(code):
    try:
        output=subprocess.check_output(['python','-c',code],universal_newlines=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output=e.output
    except subprocess.TimeoutExpired as e:
        output='\r\n'.join(['Time Out!!!',e.output])
    return output

code="""print('Test success')"""
print(run_code(code))