import argparse
from ssh_honeypot import *
from web_honeypot import *
#parse args
if __name__ =="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-a','--address',type=str,required=True)
    parser.add_argument('-p','--port', type=int, required=True)
    parser.add_argument('-u','--username',type=str)
    parser.add_argument('-pw', '--password', type=str)
    parser.add_argument('-s','--sh', action="store_true")  #ssh honeypot
    parser.add_argument('-w', '--http', action="store_true")  #web honeypot
    args=parser.parse_args()

    try:
        if args.ssh:
            print("[-] Running SSH Honeypot...")
            honeypot(args.address, args.port, args.username, args.password)
            if not args.username:
                username=None
            if not args.password:
                password=None

        elif args.http:
            print("[-] Running HTTP Honeypot...")
            if not args.username:
                args.username="admin"
            if not args.password:
                args.password="password"
            print(f"Port: {args.port} Username: {args.username} Password: {args.password}")
            run_web_honeypot(args.port,args.username,args.password)
            pass
        else:
            print("[!] Choose a particular honeypot- SSH or HTTP")
    except:
        print("\n Exiting HONEYPY...\n")
            

