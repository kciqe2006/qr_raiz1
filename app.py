import os
from flask import Flask, render_template
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

# Ruta para generar QR de video (enlace)
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usar el puerto de Render si está disponible
    app.run(host="0.0.0.0", port=port)

