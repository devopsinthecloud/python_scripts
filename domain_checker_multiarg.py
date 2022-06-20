import subprocess, os, pydig, sys, getopt 
ipa = sys.argv[1]

def load_domains():
    domains = []
    for y in range(2, len(sys.argv)):
        domains.append(sys.argv[y])
    return(domains) 


domain_list = load_domains()

def domain_checker():
    for d in domain_list:
        output = pydig.query(d, 'A')
        #import pdb; pdb.set_trace()
        print(output)
        if ipa in output:
            print("The domain matches the IP")
        else:
            print("The domain does not match the IP address") 

domain_checker()
