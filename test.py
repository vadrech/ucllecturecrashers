from flask import Flask, redirect, request
import requests
app = Flask(__name__)

client_id = '7993613939801141.5837972735640426'
url = f"https://uclapi.com/oauth/authorise/?client_id={client_id}&state=1"

@app.route("/callback")
def callback():
    return "Logged in ?"

@app.route('/login')
def uclapi_login():
    return redirect(url)

if __name__ == "__main__":
    app.run(debug=True)