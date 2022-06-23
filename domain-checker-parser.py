import subprocess, os, pydig, sys, getopt, yaml 
ipa = sys.argv[1]
file_path = "/Users/Marinadin.Grin/repositories/ivaldi-ansible/host_vars/"
file_name = sys.argv[2]
full_path = file_path + file_name
content = None

with open(full_path, "r") as stream:
    try:
        content = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

domain_list = []
for field_key in content:
    for env in content[field_key]:
        if 'server_names' in env:
            domain_list += env['server_names']
#print(domain_list)

print("================================\n================================\n================================")

def domain_checker():
    for d in domain_list:
        output = pydig.query(d, 'A')
        #import pdb; pdb.set_trace()
        if ipa not in output:
            print(f"The domain {d} does not match the IP address") 

domain_checker()
