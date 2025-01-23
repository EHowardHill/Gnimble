from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from os import path, listdir, remove
from json import load, dump
import subprocess
import socket
from PIL import Image
import platform

if platform.system() == "Windows":
    from os import add_dll_directory
    add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

import weasyprint

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def list_wifi_networks():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SECURITY", "dev", "wifi", "list"],
            capture_output=True,
            text=True,
            check=True
        )
    except:
        print("Error")

    networks = []
    lines = result.stdout.strip().split("\n")
    for line in lines:
        # Each line is something like "MyWiFiSSID:WPA2"
        parts = line.split(":", 1)
        if len(parts) == 2:
            ssid, security = parts
            # Exclude hidden SSIDs or blank lines
            if ssid.strip():
                if [ssid.strip(), security.strip()] not in networks:
                    networks.append([ssid.strip(), security.strip()])

    print(networks)
    return networks

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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def menu():

    print([request.remote_addr, IPAddr])
    local = "Y" if request.remote_addr == '127.0.0.1' else "N"

    stories = []
    for link in listdir("stories"):
        with open(path.join("stories", link), "r") as f:
            data = load(f)
            print(data["title"])
            stories.append({"ref": data["ref"], "title": data["title"]})

    bg = listdir(path.join("static", "tmp"))[0]
    
    return render_template('menu.html', stories=stories, ip=IPAddr, bg=bg, local=local)

@app.route('/edit')
def edit():

    print([request.remote_addr, IPAddr])
    local = "Y" if request.remote_addr == '127.0.0.1' else "N"

    ref = request.args.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    title = data["title"]
    content = data["content"]

    bg = listdir(path.join("static", "tmp"))[0]

    return render_template('index.html', title=title, content=content, ref=ref, bg=bg, local=local)

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

@app.route('/delete', methods=["POST"])
def delete():
    ref = request.json.get("ref")
    remove(path.join("stories", ref + ".json"))

    return {
        "success": 1
    }

@app.route('/create', methods=["POST"])
def create():
    title = request.json.get("title")

    ref = title.replace(" ","-").lower().strip()

    data = {
        "ref": ref,
        "title": title,
        "content": "It was a dark and stormy night..."
    }

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

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        tmp_path = path.join("static", 'tmp', filename)
        for f in listdir(path.join("static", "tmp")):
            remove(path.join("static", "tmp", f))
        file.save(tmp_path)

    return redirect(url_for('menu'))

@app.route('/print', methods=['POST'])
def print_document():
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    pdf = weasyprint.HTML(string=data["content"]).write_pdf()
    open(path.join("static", 'output.pdf'), 'wb').write(pdf)
    return {
        "success": 1
    }

@app.route('/wifi-list', methods=['POST'])
def wifi_list():
    result = subprocess.run(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
                capture_output=True,
            text=True,
            check=True)
    output = result.stdout.strip().split("\n")

    current = "Not Connected"
    for c in output:
        print(c)
        if "yes:" in c:
            current = c.replace("yes:", "")

    return {
        "success": 1,
        "current": current,
        "networks": list_wifi_networks()
    }

@app.route('/wifi-connect', methods=['POST'])
def wifi_connect():
    ssid = request.json.get("ssid")
    password = request.json.get("password")
    print(["Trying: ", ssid, password])

    cmd = ["sudo", "/home/user/wifi/connect.sh", ssid]
    if password != "":
        cmd.append(password)

    try:
        subprocess.run(cmd, check=True)
        return {
            "success": 1
        }
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to '{ssid}'.\nError: {e}")

    return {
        "success": 0
    }