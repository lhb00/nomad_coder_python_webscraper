from flask import Flask, render_template, request
from extractors.wwr import extract_wwr_jobs
from extractors.remoteok import extract_remoteok_jobs

app = Flask("JobScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs = db[keyword]
    else:
        global remoteok, wwr, number
        remoteok = extract_remoteok_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = wwr + remoteok
        number = len(jobs)
        db[keyword] = jobs
    return render_template("search.html",
                           keyword=keyword,
                           jobs=jobs,
                           wwr=wwr,
                           remoteok=remoteok,
                           number=number)


app.run(host="0.0.0.0", port=8080)
