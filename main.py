from flask import Flask

app = Flask(__name__)


#API token = ########################################
#client_id =  ################################
#client_secret =  ###############################################################

#callback = redirect to page of our site
#two paths one for login 

#callback from ucl api exchange auth code for access token

@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)
