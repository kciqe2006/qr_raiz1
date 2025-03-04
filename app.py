import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Esto obtiene el puerto desde la variable de entorno
    app.run(host="0.0.0.0", port=port)  # Asegúrate de que esté escuchando en 0.0.0.0
import qrcode

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        if data:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img.save('static/qr_code.png')
            return render_template('index.html', img_url='static/qr_code.png')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
