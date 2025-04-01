import socket
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up logging
logging.basicConfig(filename='honeypot_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')



def send_email_alert(subject, body):   # Email alert function (replace with your own email credentials)

    sender_email = "deoreyash2020@gmail.com"  # Replace with your email
    receiver_email = "deoreyash2020@gmail.com"  # Replace with recipient email
    password = "Deore@yash20"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def handle_connection(client_socket):  # Function to handle the connection from the attacker
    # Log the attacker's IP address
    client_ip = client_socket.getpeername()[0]
    logging.info(f"Connection attempt from: {client_ip}")
    
    # Send fake banner to attacker (mimic vulnerable service)
    client_socket.send(b"SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8\r\n")
    
    # Close the connection
    client_socket.close()


def start_honeypot():   # Set up the honeypot server
    honeypot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    honeypot.bind(('0.0.0.0', 22))  # Listen on port 22 (SSH)
    honeypot.listen(5)
    
    print("Honeypot is running...")

    while True:
        client_socket, addr = honeypot.accept()
        print(f"Connection from {addr}")
        handle_connection(client_socket)

# Start honeypot
if __name__ == "__main__":
    start_honeypot()
