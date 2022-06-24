import subprocess, os, pydig, sys, getopt, yaml
import colorama
from colorama import Fore 
domain = sys.argv[1]
d_ipa = pydig.query(domain, 'AAAA') #arr
d_ipa4 = pydig.query(domain, 'A')
d_cname = pydig.query(domain, 'CNAME')  #array
d_cname_str = ''.join(d_cname)
ipa_str = ''.join(d_ipa)
ipa4_str = ''.join(d_ipa4)

def printaline():
    print("================================\n================================\n================================")

printaline()

print(f"Checking a domain with IPV6 {d_ipa} and IPV4 {d_ipa4}")

printaline()

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

printaline()

def domain_checker():
    for dom in domain_list:
        output = pydig.query(dom, 'AAAA')
        output4 = pydig.query(dom, 'A')
       # import pdb; pdb.set_trace()
        if len(output) == 0:
            if ipa4_str not in output4:
                print(Fore.MAGENTA + f"The domain {dom} does't have an IPV6 record and the IPV4 address doesn't match")
            else:
                print(Fore.YELLOW + f"The domain {dom} does not have an IPV6 record")
        else:
            if ipa_str not in output and ipa4_str not in output4:
                print(Fore.RED + f"The domain {dom} does not match the given IPV6 and IPV4 addresses")

domain_checker()

#import pdb; pdb.set_trace()
def cname_checker():
    for dom in domain_list:
        cname = pydig.query(dom, 'CNAME')
        if d_cname_str in cname:
            print(f"{dom} has a CNAME: {cname} and we will check it")
            cname_s = ''.join(cname)
            cname_end = pydig.query(cname_s, 'CNAME') #can i query this?
            if len(cname_end) == 0:
                print(f"The end domain {cname_s} has no CNAME record")

cname_checker()
