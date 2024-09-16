# dual-honeypot

Welcome to dual Honeypot.
This is a Honeypot project. A honeypot is a decoy system which traps attackers. The intention behind a honeypot is to find the methods of the attacker.
In this project however, a honeypot will be used to log any information being entered by the user, including sensitive information such as usernames and passwords.
This projectcomprises of 2 honeypots:
-> SSH Honeypot
-> Web Honeypot

The SSH honeypot:
This honeypot makes use of an emulated shell to capture the commands used by the user. Any command entered by the user will be logged into a log file for further investigation.
The information collected in the log files include:
-IP address of the user (client)
- Username and password enetered by the user to gain access to the shell
- Commands executed by the user in the shell

The Web Honeypot:
This Honeypot logs any interaction by the user with a webpage. This webpage is a WordPress login page, which was created using html code. This is useful in finding any vulnerabilities in a login page.
Similar to the previous honeypot, this one also maintains a log file, which includes information such as:
- Ip address of the clients (users)
- Timestamp of entry into the login page
- Username and password entered by the user.

These log files can later be investigated and analysed to find any suspicious activity within a network. 

This Honepot was made solely using Python and associated libraries.
Please note that a key pair needs to be generated in order to test the SSH Honeypot

Using command like "ssh -p 2223 username@ <ip-addr>", a connection can be established.

The 2 honeypots can only be run one at a time, and is thus stored in 2 different files.
Once the web honeypot is run, follow the link mentioned in the output to see the desired result. 


Any associated libraries can easily be installed, using the terminal.

Future improvements could be:
Adding and logging more information by the user

