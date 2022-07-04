#don't forget to create a file with your directories
import applescript
from applescript import tell 

command = "bin/dev"
directories = open("dirs.txt", "r")
for directory in directories:
    tell.app('Terminal', f'do script "cd {directory}; {command}"')
