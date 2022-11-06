from flask import Flask

app = Flask(__name__)


#API token = uclapi-14368d4948fb65d-7998a1883fb66c6-218ced184285808-584da96c6f03c13
#client_id = 7993613939801141.5837972735640426
#client_secret = e7926d66972661804ea229c464f6f1831499189ad3e5ac553ea2a6cc6b3e4c22

#callback = redirect to page of our site
#two paths one for login 

#callback from ucl api exchange auth code for access token

@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)