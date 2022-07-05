import sys, subprocess, pathlib, os, platform

chd = pathlib.Path.home()
command = "bin/dev"
directories = open("dirs.txt", "r")
subprocess.call(["npx", "--ignore-existing", "google-artifactregistry-auth", f"--repo-config={chd}/.npmrc", f"--credential-config={chd}/.npmrc"])

def npmrc():
    for dir in directories:
        subprocess.call(["cp", f"{chd}/.npmrc", dir])
npmrc()

def apple():
    import applescript
    from applescript import tell 
    for directory in directories:
        tell.app('Terminal', f'do script "cd {directory}; {command}"')

osys = platform.system()
print(osys)

def tmux():
    subprocess.call(["tmux", "new-session", "cd remark-vp-cf && bin/dev --skip-npx", ";", "split-window", "cd remark-vp-crm && bin/dev --skip-npx", ";", "split-window", "cd remark-vp-admin && bin/dev --skip-npx", ";", "split-window", "cd remark-vp-login/remark-login && bin/dev --skip-npx", ";", "select-layout", "tiled"])

if "Linux" not in osys:
    print("We can use Macos terminal")
    apple()
else:
    tmux()

