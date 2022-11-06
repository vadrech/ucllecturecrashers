from flask import Flask, redirect, request, render_template
import requests
import pandas as pd
import spacy
import numpy as np
# import datetime
app = Flask(__name__)
token = None
client_id = '7993613939801141.5837972735640426'
url = f"https://uclapi.com/oauth/authorise/?client_id={client_id}&state=1"
client_secret = "e7926d66972661804ea229c464f6f1831499189ad3e5ac553ea2a6cc6b3e4c22"
user_data = {}
token = ""
course = ""
year = ""
module_data = []
module_selected = ""
prof = ""
prof_email = ""

@app.route('/login')
def uclapi_login():
    return redirect(url)

@app.route('/callback')
def receive_callback():
    global token, user_data
    # extract query parameters
    code = request.args.get('code', '')
    # e.g. request an auth token behind-the-scenes
    params = {"client_id": client_id, "code": code,
              "client_secret": client_secret}
    r = requests.get("https://uclapi.com/oauth/token", params=params)
    decoded = r.json()
    # print(decoded)  # your access token!
    token = decoded['token']
    # print("TOKEN", token)
    params = {"token": token,"client_secret": client_secret}
    my_request = requests.get("https://uclapi.com/oauth/user/data", params=params)
    request1 = my_request.json()
    user_data["given_name"] = request1["given_name"]
    user_data["full_name"] = request1["full_name"]
    user_data["email"] = request1["email"]
    
    my_request_2 = requests.get("https://uclapi.com/oauth/user/studentnumber", params=params)
    request2 = my_request_2.json()
    user_data["student_number"] = request2["student_number"]
    return redirect("/course_finder")


@app.route('/demo')
def demo():
    global token
    # e.g. request an auth token behind-the-scenes
    params = {"token": token, "client_secret": client_secret, "department": "COMPS_ENG"}
    r = requests.get("https://uclapi.com/timetable/data/modules", params=params)
    return r.json()  # your timetable!



@app.route('/')
def hello():
    return render_template("home.html", url = url)


@app.route("/module-selector", methods=["GET", "POST"])
def module_selector():
    if request.method == "GET":
        global course, year
        if "First" in year:
            year = 1
        elif "Second" in year:
            year = 2
        elif "Third" in year:
            year = 3
        else:
            year = 4
        
        term = 1
        
        def filterByYearAndTerm(df, year, term):
            c = df.loc[df[2] == year]
            d = c.loc[c[3] == term]
            
            return d
    
        df = pd.read_csv("csvfile.csv", header=None)
        nlp = spacy.load("en_core_web_md")
        filteredDF = filterByYearAndTerm(df, year, term)
        narrow_names = filteredDF.reset_index()[1]
        narrow_ids = filteredDF.reset_index()[0]
    
        sim_scores = []
        doc1 = nlp(course)
            
        for d_name in narrow_names:
            score = 0
           # for word in d_name.replace(",", "").replace("&", "").replace("a", "").replace("an", "").replace("of", "").replace("and", "").replace("to", "").split(" "):
                #if len(word) > 2 and word in course:
                    #score += 0.4
            doc2 = nlp(d_name)
            score += doc1.similarity(doc2)
            sim_scores.append(score)
    
        top_2_idx = np.argsort(sim_scores)[-10:]
    
        module_ids = []
        module_names = []
    
        for idx in top_2_idx:
            module_ids.append(narrow_ids[idx])
            module_names.append(narrow_names[idx])
            
        module_ids.reverse()
        module_names.reverse()
        
        return render_template("module_selector.html", course = course, year = year, module_ids = module_ids, module_names = module_names, enumerate=enumerate)

    elif request.method == "POST":
        global module
        module = request.form.get("module")
        return redirect("/module")

@app.route("/module")
def module():
    module_data = []
    date = "2022-11-14"
    params = {"token": token,"client_secret": client_secret, "modules": module, "date": date}
    my_request = requests.get("https://uclapi.com/timetable/bymodule", params=params)
    decode = my_request.json()
    for i in range(len(decode["timetable"][date])):
        data = {}
        data["Start Time"] = decode["timetable"][date][i]["start_time"]
        data["End Time"] = decode["timetable"][date][i]["end_time"]
        data["Module ID"] = decode["timetable"][date][i]["module"]["module_id"]
        data["Module Name"] = decode["timetable"][date][i]["module"]["name"]
        global module_selected
        module_selected = data["Module Name"]
        data["Lecturer"] = decode["timetable"][date][i]["module"]["lecturer"]["name"]
        global prof
        prof = data["Lecturer"]
        data["Email"] = decode["timetable"][date][i]["module"]["lecturer"]["email"]
        global prof_email
        prof_email = data["Email"]
        data["Location"] = decode["timetable"][date][i]["location"]["name"]
        module_data.append(data)
        
    
    return render_template("modules.html", course = course, year = year, l = module_data)


@app.route("/confirm")
def confirm():
    return render_template("confirm_page.html", module = module_selected, professor = prof)


@app.route("/send-email")
def send_email():
    return render_template("end.html", email = prof_email, course_name = module_selected, Lecturer = prof, full_name = user_data["full_name"], given_name = user_data["given_name"], student_number = user_data["student_number"], course_id = module)

@app.route("/course_finder", methods=["GET", "POST"])
def course_finder():
    if request.method == "GET":
        return render_template("course_finder.html", name=user_data["given_name"], l = ["First Year", "Second Year", "Third Year", "Fourth Year"])

    elif request.method == "POST":
        global course
        course = request.form.get("course")
        global year
        year = request.form.get("year")
        return redirect("/module-selector")
    
if __name__ == "__main__":
    app.run(debug=True)
#from
#function for getting current term
#fheq - 3 = year (translate to 'difficulty')
    #filtering:
        #year/difficulty
#store all departments locally