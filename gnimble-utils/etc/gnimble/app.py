from datetime import datetime
from docx import Document
from flask import Flask, render_template, request, redirect, url_for
from htmldocx import HtmlToDocx
from json import load, loads, dump
from os import path, listdir, remove, system, popen, mkdir
from time import sleep
from werkzeug.utils import secure_filename
import html2text
import psutil
import random
import socket
import subprocess
import weasyprint
import pyudev
import re

serial_number = ""
if not path.exists("/tmp/key"):
    serial_number = str(random.randint(10000000, 99999999))
    with open("/tmp/key", "w") as f:
        f.write(serial_number)
else:
    with open("/tmp/key", "r") as f:
        serial_number = f.read()

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def decode_mount_point(escaped):
    def replace_octal(match):
        return chr(int(match.group(1), 8))

    return re.sub(r"\\(\d{3})", replace_octal, escaped)


def get_mount_point(device_node):
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if parts[0] == device_node:
                    escaped_mount_point = parts[1]
                    return decode_mount_point(escaped_mount_point)
    except IOError:
        # Silently return None if /proc/mounts can't be read
        return None
    return None


def get_usb_mount_points():
    context = pyudev.Context()
    mount_points = []

    # Iterate over all block devices
    for device in context.list_devices(subsystem="block"):
        # Check if the device has a USB parent, indicating it's a USB mass storage device
        if device.find_parent("usb"):
            device_node = device.device_node  # e.g., '/dev/sdb1'
            mount_point = get_mount_point(device_node)
            if mount_point:
                mount_points.append(mount_point)

    return mount_points


def version():
    v = popen("apt-cache policy gnimble-utils | grep Installed:").read().strip()
    v = v.replace("Installed: ", "")
    return v


def list_wifi_networks():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SECURITY", "dev", "wifi", "list"],
            capture_output=True,
            text=True,
            check=True,
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


def get_default_printer():
    try:
        result = subprocess.run(
            ["lpstat", "-d"], capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()
        if output.startswith("system default destination:"):
            return output.split(": ")[1]
        else:
            return None
    except subprocess.CalledProcessError:
        return None


def get_available_printers():
    try:
        result = subprocess.run(
            ["lpstat", "-p"], capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().split("\n")
        printers = []
        for line in lines:
            if line.startswith("printer "):
                parts = line.split()
                printer_name = parts[1]
                printers.append(printer_name)
        return printers
    except subprocess.CalledProcessError:
        return []


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/get_time", methods=["POST"])
def get_time():
    return {"success": 1, "time": datetime.now().strftime("%I:%M %p")}


@app.route("/get_battery", methods=["POST"])
def get_battery():
    battery = psutil.sensors_battery()
    if battery is not None:
        percent = str(int(battery.percent))
        return {"success": 1, "battery": percent + "%"}
    else:
        return {"success": 1, "battery": "No Battery"}


@app.route("/")
def menu():
    IPAddr = get_intranet_ip()
    print([request.remote_addr, IPAddr])
    local = "Y" if request.remote_addr == "127.0.0.1" else "N"

    stories = []
    for link in listdir("stories"):
        with open(path.join("stories", link), "r") as f:
            data = load(f)
            print(data["title"])
            stories.append({"ref": data["ref"], "title": data["title"]})

    current_mounts = set(get_usb_mount_points())
    for mount in current_mounts:
        p = path.join(p, "stories", "raw")
        if not path.exists(p):
            mkdir(p)
        for link in listdir(p):
            with open(path.join("stories", link), "r") as f:
                data = load(f)
                print(data["title"])
                contains = False
                for s in stories:
                    if s["title"] == data["title"]:
                        contains = True
                if not contains:
                    stories.append({"ref": data["ref"], "title": data["title"]})

    bg = listdir(path.join("static", "tmp"))[0]

    time = get_time()["time"]
    battery = get_battery()["battery"]

    result = subprocess.run(
        "nmcli -t -f active,ssid dev wifi | grep yes:",
        shell=True,
        capture_output=True,  # Alternatively: stdout=subprocess.PIPE, stderr=subprocess.PIPE
        text=True,  # Alternatively: universal_newlines=True
    )

    wifi = result.stdout.strip()

    if str(wifi) == "0":
        wifi = "No Internet"
    else:
        wifi = wifi.replace("yes:", "")

    return render_template(
        "menu.html",
        stories=stories,
        ip=IPAddr,
        bg=bg,
        local=local,
        serial=serial_number,
        battery=battery,
        time=time,
        wifi=wifi,
        version=version(),
    )


@app.route("/edit")
def edit():

    local = "Y" if request.remote_addr == "127.0.0.1" else "N"

    ref = request.args.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    title = data["title"]
    content = data["content"]

    bg = listdir(path.join("static", "tmp"))[0]

    result = subprocess.run(
        "nmcli -t -f active,ssid dev wifi | grep yes:",
        shell=True,
        capture_output=True,  # Alternatively: stdout=subprocess.PIPE, stderr=subprocess.PIPE
        text=True,  # Alternatively: universal_newlines=True
    )

    wifi = result.stdout.strip()

    if str(wifi) in ["0", ""]:
        wifi = "No Internet"
    else:
        wifi = wifi.replace("yes:", "")

    print(str(wifi))

    return render_template(
        "index.html",
        title=title,
        content=content,
        ref=ref,
        bg=bg,
        local=local,
        wifi=wifi,
    )


@app.route("/rename", methods=["POST"])
def rename():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    ref = request.json.get("ref")
    title = request.json.get("title")

    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)

    data["title"] = title

    with open(path.join("stories", ref + ".json"), "w") as f:
        dump(data, f)

    return {"success": 1}


@app.route("/delete", methods=["POST"])
def delete():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    ref = request.json.get("ref")
    remove(path.join("stories", ref + ".json"))

    return {"success": 1}


@app.route("/create", methods=["POST"])
def create():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    title = request.json.get("title")

    ref = str(random.randint(0, 9999))
    while path.exists(path.join("stories", ref + ".json")):
        ref = str(random.randint(0, 9999))

    data = {"ref": ref, "title": title, "content": "It was a dark and stormy night..."}

    with open(path.join("stories", ref + ".json"), "w") as f:
        dump(data, f)

    return {"success": 1}


@app.route("/save", methods=["POST"])
def save():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    ref = request.json.get("ref")
    title = request.json.get("title")
    content = request.json.get("content")

    data = {"ref": ref, "title": title, "content": content}

    with open(path.join("stories", ref + ".json"), "w") as f:
        dump(data, f)

    return {"success": 1}


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file:
        filename = secure_filename(file.filename)
        tmp_path = path.join("static", "tmp", filename)
        for f in listdir(path.join("static", "tmp")):
            remove(path.join("static", "tmp", f))
        file.save(tmp_path)

    return redirect(url_for("menu"))


@app.route("/print", methods=["POST"])
def print_document():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        fd = f.read()
        print("vvv" + fd)
        data = loads(fd)

    content = (
        """<link href="//cdn.quilljs.com/1.3.6/quill.core.css" rel="stylesheet"><div class="ql-editor">"""
        + data["content"]
        + """</div>"""
    )
    pdf = weasyprint.HTML(string=content).write_pdf()
    open(path.join("static", "output.pdf"), "wb").write(pdf)
    return {"success": 1}


@app.route("/print_usb", methods=["POST"])
def print_usb():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        fd = f.read()
        print("vvv" + fd)
        data = loads(fd)

    content = (
        """<link href="//cdn.quilljs.com/1.3.6/quill.core.css" rel="stylesheet"><div class="ql-editor">"""
        + data["content"]
        + """</div>"""
    )
    pdf = weasyprint.HTML(string=content).write_pdf()

    # Determine the printer to use
    default_printer = get_default_printer()
    if default_printer:
        # Use default printer by not specifying -d
        cmd = ["lp", "-t", "Print Job", "-o", "document-format=application/pdf", "-"]
    else:
        available_printers = get_available_printers()
        if available_printers:
            printer_name = available_printers[0]
            cmd = [
                "lp",
                "-d",
                printer_name,
                "-t",
                "Print Job",
                "-o",
                "document-format=application/pdf",
                "-",
            ]
        else:
            print("Error: No printers available.")
            return {"success": 0}

    # Execute the lp command to print the PDF
    subprocess.run(cmd, input=pdf, check=True)

    return {"success": 1}


@app.route("/docx", methods=["POST"])
def print_docx():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)
    content = (
        """<link href="//cdn.quilljs.com/1.3.6/quill.core.css" rel="stylesheet"><div class="ql-editor">"""
        + data["content"]
        + """</div>"""
    )

    document = Document()
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(content, document)
    document.save(path.join("static", "output.docx"))

    return {"success": 1}


@app.route("/text", methods=["POST"])
def print_text():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    sleep(1)
    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        data = load(f)

    content = html2text.html2text(data["content"])

    with open(path.join("static", "output.txt"), "w") as f:
        f.write(content)

    return {"success": 1}


@app.route("/usb-list", methods=["POST"])
def usb_list():
    current_mounts = set(get_usb_mount_points())
    return {"success": 1, "mounts": current_mounts}


@app.route("/copy_to_usb", methods=["POST"])
def copy_to_usb():

    ref = request.json.get("ref")
    with open(path.join("stories", ref + ".json"), "r") as f:
        fd = f.read()
        print("vvv" + fd)
        data = loads(fd)

    current_mounts = set(get_usb_mount_points())

    for mount in current_mounts:
        p = path.join(mount, "stories")
        pp = path.join(p, "raw")
        if not path.exists(p):
            mkdir(p)
        if not path.exists(pp):
            mkdir(pp)
        with open(path.join(p, data["title"] + ".html"), "w", encoding="utf-8") as f:
            f.write(data["content"])
        with open(path.join(pp, ref + ".json"), "w", encoding="utf-8") as f:
            f.write(data)

    return {"success": 1}


@app.route("/wifi-list", methods=["POST"])
def wifi_list():
    result = subprocess.run(
        ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout.strip().split("\n")

    current = "Not Connected"
    for c in output:
        print(c)
        if "yes:" in c:
            current = c.replace("yes:", "")

    return {"success": 1, "current": current, "networks": list_wifi_networks()}


@app.route("/wifi-connect", methods=["POST"])
def wifi_connect():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    ssid = request.json.get("ssid")
    password = request.json.get("password")
    print(["Trying: ", ssid, password])

    cmd = ["sudo", "/etc/gnimble/wifi/connect.sh", ssid]
    if password != "":
        cmd.append(password)

    try:
        subprocess.run(cmd, check=True)
        return {"success": 1}

    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to '{ssid}'.\nError: {e}")

    return {"success": 0}


@app.route("/password", methods=["POST"])
def password():
    if request.remote_addr != "127.0.0.1":
        serial = request.json.get("serial")
        if serial != serial_number:
            return {"success": 401}

    s = request.json.get("serial")
    print([s, serial_number])

    return {"success": 1 if s == serial_number else 0}
