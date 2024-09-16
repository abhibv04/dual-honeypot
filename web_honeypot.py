import logging
from flask import Flask,render_template,request,redirect,url_for
from logging.handlers import RotatingFileHandler
#Logging format
logging_format=logging.Formatter('%(asctime)s %(message)s')

#HTTP Logger

funnel_logger=logging.getLogger('HTTPLogger') #capture ip addresses and passwords
funnel_logger.setLevel(logging.INFO)
funnel_handler=RotatingFileHandler('http_audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

#Baseline HP
def web_honepot(input_username="admin", input_password="password"):
    app=Flask(__name__)
    @app.route('/')
    def index():
        return render_template('wp-admin.html')
    @app.route('/wp-admin-login', methods=['POST'])  #making sure that user interacts with webpage only through POST
    def login():
        username=request.form['username']
        password=request.form['password']
        ip_address=request.remote_addr
        funnel_logger.info(f'Clients with IP Address: {ip_address} entered\n Username: {username}, Password: {password}')
        if username==input_username and password==input_password:
            return 'DEEBODAHH'
        else:
            return "Invalid username and password. Try Again"
    return app

    
def run_web_honeypot(port=5000,input_username="admin", input_password="password"):
    run_web_honeypot_app=web_honepot(input_username,input_password)
    run_web_honeypot_app.run(debug=True,port=port,host="0.0.0.0")
    return run_web_honeypot_app
run_web_honeypot(port=5000, input_username="admin", input_password="password")

    
