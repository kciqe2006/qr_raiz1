from flask import Flask, render_template, request, jsonify
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2c3e50", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    qr_type = request.json['type']
    fields = request.json['fields']
    
    qr_data = ""
    if qr_type == 'wifi':
        qr_data = f"WIFI:S:{fields['ssid']};T:{fields['encryption']};P:{fields['password']};;"
    elif qr_type == 'vcard':
        qr_data = f"BEGIN:VCARD\nVERSION:3.0\nN:{fields['apellido']};{fields['nombre']}\nTEL:{fields['telefono']}\nEMAIL:{fields['email']}\nEND:VCARD"
    elif qr_type == 'geo':
        qr_data = f"geo:{fields['latitud']},{fields['longitud']}"
    elif qr_type == 'sms':
        qr_data = f"SMSTO:{fields['telefono']}:{fields['mensaje']}"
    elif qr_type == 'email':
        qr_data = f"MATMSG:TO:{fields['destinatario']};SUB:{fields['asunto']};BODY:{fields['mensaje']};;"
    elif qr_type == 'url':
        qr_data = fields['url']
    elif qr_type == 'video':
        qr_data = fields['url_video']
    
    qr_image = generate_qr_code(qr_data)
    return jsonify({'qr_image': qr_image})

if __name__ == '__main__':
    app.run(debug=True)
