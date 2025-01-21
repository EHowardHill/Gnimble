from flask import Flask, render_template, request
from os import path, listdir
from json import load, dump

app = Flask(__name__)

@app.route('/')
def menu():

    stories = []
    for link in listdir("stories"):
        with open(path.join("stories", link), "r") as f:
            data = load(f)
            print(data["title"])
            stories.append({"ref": data["ref"], "title": data["title"]})
    
    return render_template('menu.html', stories=stories)

@app.route('/edit')
def edit():
    ref = request.args.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    title = data["title"]
    content = data["content"]

    return render_template('index.html', title=title, content=content, ref=ref)

@app.route('/save', methods=["POST"])
def save():
    ref = request.json.get("ref")
    title = request.json.get("title")
    content = request.json.get("content")

    data = {
        "ref": ref,
        "title": title,
        "content": content
    }

    with open(path.join("stories", ref + ".json"), "w") as f:
        dump(data, f)

    return {
        "success": 1
    }