import os
from flask import Flask, render_template, request, send_from_directory
import qrcode

app = Flask(__name__)

# Ruta principal con método GET
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Ruta para generar QR de WiFi
@app.route('/generate_wifi_qr', methods=['POST'])
def generate_wifi_qr():
    ssid = request.form['ssid']
    password = request.form['password']
    qr = qrcode.make(f"WIFI:T:WPA;S:{ssid};P:{password};;")
    qr.save("static/wifi_qr.png")
    return send_from_directory("static", "wifi_qr.png")

# Ruta para generar QR de enlace a video
@app.route('/generate_video_qr', methods=['POST'])
def generate_video_qr():
    video_url = request.form['video_url']
    qr = qrcode.make(video_url)
    qr.save("static/video_qr.png")
    return send_from_directory("static", "video_qr.png")

# Ruta para generar QR de geolocalización
@app.route('/generate_location_qr', methods=['POST'])
def generate_location_qr():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    location_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    qr = qrcode.make(location_url)
    qr.save("static/location_qr.png")
    return send_from_directory("static", "location_qr.png")

# Ruta para generar QR de texto
@app.route('/generate_text_qr', methods=['POST'])
def generate_text_qr():
    text = request.form['text']
    qr = qrcode.make(text)
    qr.save("static/text_qr.png")
    return send_from_directory("static", "text_qr.png")

# Ruta para generar QR de URL
@app.route('/generate_url_qr', methods=['POST'])
def generate_url_qr():
    url = request.form['url']
    qr = qrcode.make(url)
    qr.save("static/url_qr.png")
    return send_from_directory("static", "url_qr.png")

# Ruta para generar QR de correo electrónico
@app.route('/generate_email_qr', methods=['POST'])
def generate_email_qr():
    email = request.form['email']
    subject = request.form.get('subject', '')
    body = request.form.get('body', '')
    qr = qrcode.make(f"mailto:{email}?subject={subject}&body={body}")
    qr.save("static/email_qr.png")
    return send_from_directory("static", "email_qr.png")

# Ruta para generar QR de SMS
@app.route('/generate_sms_qr', methods=['POST'])
def generate_sms_qr():
    phone_number = request.form['phone_number']
    message = request.form['message']
    qr = qrcode.make(f"SMSTO:{phone_number}:{message}")
    qr.save("static/sms_qr.png")
    return send_from_directory("static", "sms_qr.png")

# Ruta para generar QR de contacto vCard
@app.route('/generate_vcard_qr', methods=['POST'])
def generate_vcard_qr():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
    qr = qrcode.make(vcard)
    qr.save("static/vcard_qr.png")
    return send_from_directory("static", "vcard_qr.png")

# Ruta para generar QR de eventos de calendario (iCalendar)
@app.route('/generate_event_qr', methods=['POST'])
def generate_event_qr():
    event_name = request.form['event_name']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    location = request.form['location']
    description = request.form['description']
    
    event = f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART:{start_time}\nDTEND:{end_time}\nLOCATION:{location}\nDESCRIPTION:{description}\nEND:VEVENT"
    
    qr = qrcode.make(event)
    qr.save("static/event_qr.png")
    return send_from_directory("static", "event_qr.png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usar el puerto de Render si está disponible
    app.run(host="0.0.0.0", port=port)
