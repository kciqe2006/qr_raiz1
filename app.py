import os
from flask import Flask, render_template, request, send_from_directory
import qrcode

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para generar el QR para SMS
@app.route('/generate_sms_qr', methods=['POST'])
def generate_sms_qr():
    # Obtener el número de teléfono y el mensaje desde el formulario
    phone_number = request.form['phone_number']
    message = request.form['message']

    # Generar el QR
    qr_data = f"SMSTO:{phone_number}:{message}"
    qr = qrcode.make(qr_data)
    
    # Guardar la imagen en la carpeta estática
    qr_path = os.path.join('static', 'sms_qr.png')
    qr.save(qr_path)

    return send_from_directory('static', 'sms_qr.png')

# Ruta para generar el QR para enlace web
@app.route('/generate_url_qr', methods=['POST'])
def generate_url_qr():
    # Obtener la URL desde el formulario
    url = request.form['url']

    # Generar el QR
    qr = qrcode.make(url)
    
    # Guardar la imagen en la carpeta estática
    qr_path = os.path.join('static', 'url_qr.png')
    qr.save(qr_path)

    return send_from_directory('static', 'url_qr.png')

# Ruta para generar el QR para Wi-Fi
@app.route('/generate_wifi_qr', methods=['POST'])
def generate_wifi_qr():
    # Obtener SSID, contraseña y tipo de encriptación desde el formulario
    ssid = request.form['ssid']
    password = request.form['password']
    encryption = request.form['encryption']

    # Crear el QR para la red Wi-Fi
    qr_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    qr = qrcode.make(qr_data)
    
    # Guardar la imagen en la carpeta estática
    qr_path = os.path.join('static', 'wifi_qr.png')
    qr.save(qr_path)

    return send_from_directory('static', 'wifi_qr.png')

# Ruta para generar el QR para ubicación
@app.route('/generate_location_qr', methods=['POST'])
def generate_location_qr():
    # Obtener la latitud y longitud desde el formulario
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Crear el QR para la ubicación
    qr_data = f"geo:{latitude},{longitude}"
    qr = qrcode.make(qr_data)
    
    # Guardar la imagen en la carpeta estática
    qr_path = os.path.join('static', 'location_qr.png')
    qr.save(qr_path)

    return send_from_directory('static', 'location_qr.png')

if __name__ == '__main__':
    app.run(debug=True)
