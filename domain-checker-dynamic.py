import subprocess, os, pydig, sys, getopt 
domain = sys.argv[2]
ipa = sys.argv[1]

def domain_checker():
    output = pydig.query(domain, 'A')
    #import pdb; pdb.set_trace()
    print(output)
    if ipa in output:
        print("The domain matches the IP")
    else:
        print("The domain does not match the IP address") 

domain_checker()
#print(f"Arguments count: {len(sys.argv)}")
