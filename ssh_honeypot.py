import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import paramiko.transport
import threading
logging_format=logging.Formatter('%(message)s')
SSH_BANNER="SSH-2.0-MySSHServer_1.0"    #gives metadata abt ssh connection
#host_key='server.key'   
host_key=paramiko.RSAKey(filename='server.key')    #priv key= server.key

# Loggers and Logging files

funnel_logger=logging.getLogger('FunnelLogger') #capture ip addresses and passwords
funnel_logger.setLevel(logging.INFO)
funnel_handler=RotatingFileHandler('audits.log', maxBytes=1000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)


creds_logger=logging.getLogger('CredsLogger') #capture ip addresses and passwords
creds_logger.setLevel(logging.INFO)
creds_handler=RotatingFileHandler('cmd_audits.log', maxBytes=1000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)


# Emulated Shell- commands used by attackers

def emulated_shell(channel, client_ip):
    channel.send(b'corporate-jumpbox-2$ ')     # sending a default prompt
    command= b""
    while True:
        char=channel.recv(1)   #listening to user input
        channel.send(char)
        if not char:
            channel.close()    #if we dont get any char input

        command+=char

        if char==b'\r':
            if command.strip()==b'exit':   #closes channel when exit entered
                response=b'\nGoodBye!\n'
                channel.close()
            elif command.strip()==b'pwd':
                response=b"\n" + b"\\usr\\local" + b"\r\n"
                creds_logger.info(f'Command :{command.strip()}' + 'executed by' + f'{client_ip}')  
            elif command.strip()== b'whoami':
                response=b"\n" + b"corpuser1" + b"\r\n" 
                creds_logger.info(f'Command :{command.strip()}' + 'executed by' + f'{client_ip}')
            elif command.strip()== b'ls':
                response=b"\n" + b"jumpbox1.conf" + b"\r\n"
                creds_logger.info(f'Command :{command.strip()}' + 'executed by' + f'{client_ip}')
            elif command.strip()== b'cat jumpbox1.conf':
                response=b"\n" + b"Go to deebodah.com" + b"\r\n"
                creds_logger.info(f'Command :{command.strip()}' + 'executed by' + f'{client_ip}')
            else:
                response=b"\n" + bytes(command.strip()) + b"\r\n"
                creds_logger.info(f'Command :{command.strip()}' + 'executed by' + f'{client_ip}')

            channel.send(response)
            channel.send(b'corporate-jumpbox-2$ ')
            command=b""
#SSH Server + Sockets
class Server(paramiko.ServerInterface):
    def __init__(self,client_ip, input_username=None, input_password=None):
        self.event= threading.Event()
        self.client_ip=client_ip
        self.input_username=input_username
        self.input_password=input_password

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind=='session':
            return paramiko.OPEN_SUCCEEDED 
    def get_allowed_auth(self):
        return "password"
    def check_auth_password(self, username, password):
        funnel_logger.info(f'Client {self.client_ip} attempted connection with ' + f'username: {username}, ' + f'password: {password}')
        creds_logger.info(f'{self.client_ip},{username},{password}')  #logging the creds
        if self.input_username is not None and self.input_password is not None:
            if username== self.input_username and password== self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL
    def check_channel_shell_request(self,channel):
        self.event.set()
        return True
    def check_channel_pty_request(self,channel,term,width,height,pixelWidth,pixelHeight,modes):
        return True
    def check_channel_exec_request(self,channel,command):
        command=str(command)
        return True
def client_handle(client,addr,username,password):
    client_ip=addr[0]   #to gather the IP addr
    print(f"{client_ip} has connected to the server.")

    try:
        transport=paramiko.Transport(client)
        transport.local_version=SSH_BANNER
        server=Server(client_ip=client_ip, input_username=username, input_password=password)
        transport.add_server_key(host_key)
        transport.start_server(server=server)
        channel=transport.accept(100)   #waits for client to open a shell; time duration for client to req a channel=100ms; opens a bidirectional tunnel
        if channel is None:
            print("No channel was opened")
        standard_banner="Welcome Abhinav \r\n\r\n"
        channel.send(standard_banner)
        emulated_shell(channel,client_ip=client_ip)
        
    except Exception as error:
        print(error)
        print("!!!Error !!!")
        
    finally:
        try:
            transport.close()
        except Exception as error:
            print(error)
            print("!!! Error !!!")
        client.close()

# Provision based SSH Honeypot

def honeypot(address,port,username,password):
    socks=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #tcp,ipv4
    socks.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    socks.bind((address,port))
    socks.listen(100)   #can handle 100 connections
    print(f"SSH Server is listening on port {port}.")
    while True:
        try:
            client,addr=socks.accept()
            ssh_honeypot_thread= threading.Thread(target=client_handle, args=(client,addr,username,password))
            ssh_honeypot_thread.start()

        except Exception as error:
            print(error)

honeypot('127.0.0.1', 2223, username=None ,password=None)   #can use any password now
            



    
