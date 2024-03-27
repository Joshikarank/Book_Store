# flask --app app:user run --debug --port 7000
# flask --app app:carts run --debug --port 8000
# flask --app app:book run --debug --port 5000
import subprocess
import sys

# Define commands to run each Flask application
commands = [
    "flask --app app:user run --debug --port 7000",
    "flask --app app:carts run --debug --port 8000",
    "flask --app app:book run --debug --port 5000"
]

# Function to start a new terminal with the specified command
def start_new_terminal(command):
    if sys.platform == 'win32':
        subprocess.Popen(['start', 'cmd', '/k', command], shell=True)
    

# Start each Flask application in a separate terminal
for command in commands:
    start_new_terminal(command)
