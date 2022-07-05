import sys, subprocess, pathlib, os, platform

chd = pathlib.Path.home()
command = "bin/shell"
directories = open("dirs.txt", "r")

def apple():
    import applescript
    from applescript import tell 
    for directory in directories:
        tell.app('Terminal', f'do script "cd {directory}; {command}"')

osys = platform.system()
print(osys)

def tmux():
    subprocess.call(["tmux", "new-session", "cd remark-vp-cf && bin/shell", ";", "split-window", "cd remark-vp-crm && bin/shell", ";", "split-window", "cd remark-vp-admin && bin/shell", ";", "split-window", "cd remark-vp-login/remark-login && bin/shell", ";", "select-layout", "tiled"])

if "Linux" not in osys:
    print("We can use Macos terminal")
    apple()
else:
    tmux()
