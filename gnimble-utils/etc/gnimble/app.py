from docx import Document
from flask import Flask, render_template, request, redirect, url_for
from htmldocx import HtmlToDocx
from json import load, loads, dump
from os import path, listdir, remove
from time import sleep
from werkzeug.utils import secure_filename
import html2text
import random
import socket
import subprocess
import weasyprint

serial_number = ""
if not path.exists("/tmp/key"):
    serial_number = str(random.randint(10000000, 99999999))
    with open("/tmp/key", "w") as f:
        f.write(serial_number)
else:
    with open("/tmp/key", "r") as f:
        serial_number = f.read()

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

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def menu():
    IPAddr = get_intranet_ip()

    print([request.remote_addr, IPAddr])
    local = "Y" if request.remote_addr == '127.0.0.1' else "N"

    stories = []
    for link in listdir("stories"):
        with open(path.join("stories", link), "r") as f:
            data = load(f)
            print(data["title"])
            stories.append({"ref": data["ref"], "title": data["title"]})

    bg = listdir(path.join("static", "tmp"))[0]
    
    return render_template('menu.html', stories=stories, ip=IPAddr, bg=bg, local=local, serial=serial_number)

@app.route('/edit')
def edit():

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
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
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
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
    ref = request.json.get("ref")
    remove(path.join("stories", ref + ".json"))

    return {
        "success": 1
    }

@app.route('/create', methods=["POST"])
def create():
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
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
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
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
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        fd = f.read()
        print("vvv" + fd)
        data = loads(fd)

    content = """<link href="//cdn.quilljs.com/1.3.6/quill.core.css" rel="stylesheet"><div class="ql-editor">""" + data["content"] + """</div>"""
    pdf = weasyprint.HTML(string=content).write_pdf()
    open(path.join("static", 'output.pdf'), 'wb').write(pdf)
    return {
        "success": 1
    }

@app.route('/docx', methods=['POST'])
def print_docx():
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    content = """<link href="//cdn.quilljs.com/1.3.6/quill.core.css" rel="stylesheet"><div class="ql-editor">""" + data["content"] + """</div>"""

    document = Document()
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(content, document)
    document.save(path.join("static", "output.docx"))

    return {
        "success": 1
    }

@app.route('/text', methods=['POST'])
def print_text():
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    
    content = html2text.html2text(data["content"])

    with open(path.join("static", "output.txt"), "w") as f:
        f.write(content)

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
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }
        
    ssid = request.json.get("ssid")
    password = request.json.get("password")
    print(["Trying: ", ssid, password])

    cmd = ["sudo", "/etc/gnimble/wifi/connect.sh", ssid]
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

@app.route('/password', methods=['POST'])
def password():
    if request.remote_addr != '127.0.0.1':
        serial = request.json.get("serial")
        if serial != serial_number:
            return {
                "success": 401
            }

    s = request.json.get("serial")
    print([s, serial_number])

    return {
        "success": 1 if s == serial_number else 0
    }