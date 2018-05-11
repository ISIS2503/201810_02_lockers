import socket
import sys
import time
import smtplib
from email.mime.text import MIMEText

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
num=0

   
def enviarCorreo(sender,address,mensaje,asunto):
	mime_message = MIMEText(mensaje, "plain")
	mime_message["From"] = sender
	mime_message["To"] = address
	mime_message["Subject"] = asunto

	try:
		print("enviar correo")
		smtp = smtplib.SMTP('smtp.gmail.com:587')
		print("server connect")
		smtp.ehlo()
		smtp.starttls()
		print("before login")
		smtp.login(sender, 'tatiana vanessa98')
		print("after login")
		smtp.send_message(mime_message)
		print('Correo enviado')
		smtp.quit()
	except e:
		print('Error: el mensaje no pudo ser enviado.')
		print(e)

		
while True:
	connection, client_address = sock.accept()
	accepted=True
	print("inicio de comunicacion")
	try:
		while accepted:
			data = connection.recv(20)
			print(type(data))
			if data:
				print(data)
				ms="heartBeat"
				hub="hub"
				if data == ms.encode():
					print("done Comparing")
				elif data == hub.encode():
					print("Send message lock")
				time.sleep(5)
				num=0
			elif num>=5:
				time.sleep(2)
				sender = 'arquisoftprueba@gmail.com'
				receivers = 'arquisoftprueba@gmail.com'
				message = "un mensaje"
				enviarCorreo(sender,receivers,message,"asunto")
				num=0
				accepted=False
			else:
			    time.sleep(5)
			    num+=1
			    print(num)
	except:
	    print("lost connection")
	    connection, client_address=socket.accept()
	    continue
	finally:
		# Clean up the connection
		connection.close()

		




			