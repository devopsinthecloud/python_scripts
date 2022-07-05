import sys, subprocess, pathlib, os, platform

chd = pathlib.Path.home()
command = "bin/dev"
directories = open("dirs.txt", "r")
subprocess.call(["npx", "--ignore-existing", "google-artifactregistry-auth", f"--repo-config={chd}/.npmrc", f"--credential-config={chd}/.npmrc"])

def npmrc():
    for dir in directories:
        subprocess.call(["cp", f"{chd}/.npmrc", dir])

def apple():
    import applescript
    from applescript import tell 
    for directory in directories:
        tell.app('Terminal', f'do script "cd {directory}; {command}"')

osys = platform.system()
print(osys)

def tmux():
    for dir in directories:
        subprocess.call(["tmux", "new-session", f"cd {dir} && bin/dev --skip-npx", ";", "split-window", "select-layout", "tiled"])

if "Linux" not in osys:
    print("We can use Macos terminal")
    apple()
else:
    tmux()
