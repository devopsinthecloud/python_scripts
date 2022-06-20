#===Check if the domains match the ip===
import subprocess, os, pydig 
domains = ["online-uitje.nl","www.online-uitje.nl","uitjesbazen.nl","www.uitjesbazen.nl","autogarage-henkhenk.nl","www.autogarage-henkhenk.nl","wieisderat-events.nl","www.wieisderat-events.nl", "gamificationers.nl","www.gamificationers.nl","escaperoom-op-locatie.nl","www.escaperoom-op-locatie.nl", "ub-games.com", "www.ub-games.com","virtualreality-op-locatie.nl","www.virtualreality-op-locatie.nl","crazy88-events.nl","www.crazy88-events.nl"]
ipa = "84.22.106.117"

def domain_checker():
    for x in domains:
        output = pydig.query(x, 'A')
        print(output)
        if ipa in output:
            print("The domain matches the IP")
        else:
            print("The domain does not match the IP address") 

domain_checker()
