import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

# URL de donde este alojado 
URL = ""

def rellenar_correo(asunto, email_destino, newsletter):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = SMTP_USER
    msg['To'] = email_destino
    msg.attach(MIMEText(newsletter, 'html'))
    return msg

def enviar_por_SMTP(email_destino, mensaje):
    #with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_USER, email_destino, mensaje.as_string())
    server.quit()

@app.route('/warmup', methods=['GET'])
def despertar_api():
    return jsonify({"ok": True}), 200

@app.route('/enviar-verificacion', methods=['POST'])
def enviar_verificacion():
    # 1. Obtener datos del cuerpo de la petición
    data = request.get_json()
    email_destino = data.get('email')
    token = data.get('token')

    if not email_destino or not token:
        return jsonify({"error": "Faltan datos"}), 400

    # 2. Construir la URL de verificación (apuntando a tu script PHP)
    # Usamos el correo (p1) y el token (p2)
    """
    link_final = f"{URL}/verificar_usuario.php?p1={email_destino}&p2={token}"

    newsletter = render_template(
        'verificacion-correo.html', 
        link_verificacion=link_final
    )

    print("despues de jinja2")

    asunto = "Verifica tu cuenta - Breathe Tracking"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = SMTP_USER
    msg['To'] = email_destino
    msg.attach(MIMEText(newsletter, 'html'))

    #mensaje = rellenar_correo(asunto, email_destino, newsletter)
    #enviar_por_SMTP(email_destino, mensaje)
    print("despues de rellenar correo")
    """
    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("server")
        server.starttls()
        print("ls")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("login")
        server.sendmail(SMTP_USER, email_destino, "hola")
        print("enviar")
        server.quit()

        return jsonify({"mensaje": "Correo enviado correctamente"}), 200
    
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return jsonify({"error": "Fallo interno al enviar correo"}), 500

if __name__ == '__main__':
    app.run(debug=True)