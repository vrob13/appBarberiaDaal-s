import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st


def send(email, nombre, fecha, hora, servicio, empleado):

    # Create the email message
    msg = MIMEMultipart()

    # Alternative css
    css_style_alternative = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #222222;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header img {
            max-width: 200px;
            height: auto;
        }

        .content {
            background-color: #333333;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .content h1 {
            color: #ffffff;
            font-size: 24px;
            margin-bottom: 20px;
        }

        .content p {
            color: #cccccc;
            font-size: 16px;
            line-height: 1.5;
        }

        .cta-button {
            display: inline-block;
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            margin-top: 20px;
        }
    </style>
    """

    html_mensaje = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Daal's Barber shop</title>
        {css_style_alternative}
    </head>
    <body>
        <div style="background-color: #f2f2f2; padding: 20px;">
            <h1 style="text-align: center;">Daal's Barber shop</h1>
            <hr>
            <p>Estimado {nombre},</p>
            <p>Esperamos que se encuentre bien. Queremos confirmar la cita que ha solicitado en nuestra barbería. Agradecemos la confianza que ha depositado en nuestros servicios y estamos encantados de atenderle.</p>

            <p>Detalles de la cita:</p>

            <p>Fecha: {fecha}</p>
            <p>Hora: {hora}</p>
            <p>Servicio Solicitado: {servicio}</p>
            <p>Barbero(a) Asignado(a): {empleado}</p>
            <p>Ubicación: Av. Alameda 482, Región Metropolitana, Santiago de Chile</p>
            <p>Por favor, recuerde llegar unos minutos antes de su cita para que podamos ofrecerle el mejor servicio posible. Si necesita cancelar o reprogramar la cita por alguna razón, le agradeceríamos que nos lo hiciera saber con anticipación.</p>

            <p>Si tiene alguna pregunta o inquietud antes de la cita, no dude en ponerse en contacto con nosotros a través de +56 9 9724 3140 o vrobdev.pruebas@gmail.com. Estamos aquí para ayudarle.</p>

            <p>¡Esperamos poder brindarle una experiencia excepcional en nuestra barbería!</p>

            <p>Atentamente,</p>
            <p>El Equipo de Daal's Barber shop</p>
            <p>+56 9 9724 3140</p>
            <p>vrobdev.pruebas@gmail.com</p>

            <hr>
            <p>Saludos cordiales,</p>
            <p>Daal's Barber shop</p>
        </div>
    </body>
    </html>
    """

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_mensaje, 'html'))

    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    smtp_username = st.secrets["db_credentials"]["smtp_username"]
    smtp_password = st.secrets["db_credentials"]["smtp_password"]

    # Email configuration
    sender_email = smtp_username
    subject = f'Cita {nombre}'
    msg['From'] = f"Daal's Barber shop <{smtp_username}>"
    msg['Subject'] = subject
    msg['To'] = email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

    except smtplib.SMTPException as e:
        st.warning("Ha habido un error con el envío de correo de confirmación de cita.")
        print("Error envío de correo: ", e)