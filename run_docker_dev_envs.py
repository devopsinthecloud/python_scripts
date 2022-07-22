import sys, subprocess, pathlib, os, platform, time, re, threading
import docker

client = docker.from_env()

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
    subprocess.call(["tmux", "new-session", "cd remark-vp-cf && bin/dev --skip-npx", ";", "split-window", "cd remark-vp-crm && bin/dev --skip-npx", ";", "split-window", "cd remark-vp-admin && bin/dev --skip-npx", ";", "split-window", "cd remark-vp-login/remark-login && bin/dev --skip-npx", ";", "select-layout", "tiled"])


client = docker.from_env()
def checks():

    matches = ["remark-vp-crm-webserver-1", "remark-vp-admin-webserver-1", "remark-vp-cf-webserver-1", "remark-login-webserver-1"]
    c_names = []
    containers = client.containers.list()
    length = len(containers)
    for i in range(length):
        if containers[i].name in matches:
            c_names.append((containers[i].name))
    return c_names

def networks():
    matches = ["remark-vp-crm-webserver-1", "remark-vp-admin-webserver-1", "remark-vp-cf-webserver-1", "remark-login-webserver-1"]
    while len(checks()) != len(matches):
        time.sleep(10)
        print("Waiting for containers to start up")

    print('Lets connect our containers to the network!')
    subprocess.call(["docker", "network", "create", "vp", "--attachable"])
    subprocess.call(["docker", "network", "connect", "vp", "remark-vp-crm-webserver-1"])
    subprocess.call(["docker", "network", "connect", "vp", "remark-vp-admin-webserver-1"])
    subprocess.call(["docker", "network", "connect", "vp", "remark-vp-cf-webserver-1"])
    subprocess.call(["docker", "network", "connect", "vp", "remark-login-webserver-1"])
    print('Now containers can talk to each other!')

t1 = threading.Thread(target=networks)

t1.start()

if "Linux" not in osys:
    print("We can use Macos terminal")
    apple()
else:
    tmux()


t1.join()

print("Done!")
        
