import os
from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    qr_type = request.form.get('qr-type')
    img = None
    qr_data = None
    
    # Verifica que los datos necesarios sean enviados para cada tipo de QR
    if qr_type == 'sms':
        phone_number = request.form.get('phone_number')
        message = request.form.get('message')
        if phone_number and message:
            qr_data = f"SMSTO:{phone_number}:{message}"
        else:
            return "Error: SMS data incomplete.", 400
    elif qr_type == 'url':
        qr_data = request.form.get('url')
        if not qr_data:
            return "Error: URL is required.", 400
    elif qr_type == 'wifi':
        ssid = request.form.get('ssid')
        password = request.form.get('password')
        encryption = request.form.get('encryption')
        if ssid and password and encryption:
            qr_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        else:
            return "Error: Wi-Fi data incomplete.", 400
    elif qr_type == 'location':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        if latitude and longitude:
            qr_data = f"geo:{latitude},{longitude}"
        else:
            return "Error: Location data incomplete.", 400
    elif qr_type == 'vcard':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        if name and phone and email and address:
            qr_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nADR:{address}\nEND:VCARD"
        else:
            return "Error: vCard data incomplete.", 400
    elif qr_type == 'email':
        subject = request.form.get('email_subject')
        body = request.form.get('email_body')
        if subject and body:
            qr_data = f"mailto:?subject={subject}&body={body}"
        else:
            return "Error: Email data incomplete.", 400
    elif qr_type == 'video':
        qr_data = request.form.get('video_url')
        if not qr_data:
            return "Error: Video URL is required.", 400
    else:
        return "Error: Tipo de QR no reconocido.", 400

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Crear una imagen del QR
    img = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen en un objeto de bytes
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Enviar la imagen del QR como respuesta
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto proporcionado por Render o 5000 por defecto
    app.run(host='0.0.0.0', port=port, debug=True)

