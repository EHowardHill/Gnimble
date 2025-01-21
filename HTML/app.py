from flask import Flask, render_template, request
from os import path, listdir
from json import load, dump

import socket

def get_intranet_ip():
    """Gets the IP address of the current machine on the intranet."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external IP
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return None
    
IPAddr = get_intranet_ip()

app = Flask(__name__)

@app.route('/')
def menu():

    stories = []
    for link in listdir("stories"):
        with open(path.join("stories", link), "r") as f:
            data = load(f)
            print(data["title"])
            stories.append({"ref": data["ref"], "title": data["title"]})
    
    return render_template('menu.html', stories=stories, ip=IPAddr)

@app.route('/edit')
def edit():
    ref = request.args.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    title = data["title"]
    content = data["content"]

    return render_template('index.html', title=title, content=content, ref=ref)

@app.route('/rename', methods=["POST"])
def rename():
    ref = request.json.get("ref")
    title = request.json.get("title")

    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)

    data["title"] = title

    with open(path.join("stories", ref + ".json"), "w") as f:
        dump(data, f)

    return {
        "success": 1
    }

@app.route('/create', methods=["POST"])
def rename():
    ref = request.json.get("ref")
    title = request.json.get("title")

    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)

    data["title"] = title

    with open(path.join("stories", ref + ".json"), "w") as f:
        dump(data, f)

    return {
        "success": 1
    }

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