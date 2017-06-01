import os
from io import StringIO
import pyqrcode
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from restapi.models import Ticket
import psycopg2

#Keep this as a class so its object holds onto the smtp connection (don't have to reconnect)
class TicketConfirmation:

	#EDIT THIS STUFF TO YOUR SPECIFICATIONS
	SMTP_SERVER = "smtp.mail.yahoo.com"
	SMTP_PORT = "587" #try 465 if not working
	USERNAME = "joekitongasux@yahoo.com"
	PASSWORD = "420blazeit"
	########################################

	def __init__(self):
		self.SMTP = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
		self.SMTP.starttls()
		self.SMTP.login(self.USERNAME, self.PASSWORD)	
		print('authenticated')
                conn = pyscopg2.connect("dbname=pop user=super")
                self.cur = conn.cursor()


	#Check for confirmation num in db
	#if exists, check confirmed
		#if not confirmed, return named, set to confirmed
		#else return already confirmed
	#if not, return no entry	
	def confirm(self, confirmation_num):
                
                self.cur.execute("SELECT * FROM tickets WHERE confirmation_num = %s" %confirmation_num)
                try:
                        t = self.cur.fetchone()[0]
                        if t[3] == 'confirmed':
                                return 'already confirmed'
                        else:
                                self.cur.execute("UPDATE tickets SET confirmed = 'confirmed' WHERE confirmation_num = %s" %confirmation_num)
                                return 'confirmed'
                except:
                        return 'invalid'


	#Generates a confirmation number and sends an email
	def generate_confirmation(self, to_address, event_name):
		confirmation_num = str(uuid.uuid4()).replace('-', '')[0:10] #uses a uuid for confirmation number
		try:
			_generate_qr(confirmation_num)
		except:
			print('could not generate qr code')
			pass
		email = _generate_email(self.USERNAME, to_address, event_name, confirmation_num)
		try:
			self.SMTP.sendmail(self.USERNAME, to_address, email.as_string())
			print('sent email')
			os.remove('%s.png' % confirmation_num)
		except:
			print('could not send email')
		self.cur.execute("INSERT INTO tickets (email, event_name, confirmation_num, confirmed) VALUES (%s, %s, %s, %s)", (to_email, event_name, confirmation_num, 'unconfirmed'))
		return confirmation_num



###############################################
# HELPER METHODS FOR TicketConfirmation
###############################################


###
#Email HTML template; change to include more information, fancify it, etc.
###
message_template = '''
Hello! <br><br>
You're all set to attend <i>{0}</i>! <br>
Your confirmation number is <b>{1}</b> <br><br>
Have fun!<br><br>
Sincerely,<br>
What's Poppin'<br><br>
<img src="cid:{2}"><br><br>
<i>Please present your QR Code to your event host</i>
'''


#Generates QR png
def _generate_qr(confirmation_num):
	img = pyqrcode.create(confirmation_num)
	img.png('%s.png' %confirmation_num, scale=10)


#Generates an email with the qr code, based on the format of the template message
#Add additional attributes if needed
def _generate_email(from_address, to_address, event_name, confirmation_num):
	email = MIMEMultipart()
	email['Subject'] = 'Confirming Attendance to %s' % event_name
	email['From'] = from_address
	email['To'] = to_address

	#attaching message
	text = MIMEText(message_template.format(event_name, confirmation_num, confirmation_num), 'html')
	email.attach(text)
	
	#attaching qr image
	fp = open('%s.png' % confirmation_num, 'rb')
	qrimg = MIMEImage(fp.read(), name=os.path.basename('%s.png' % confirmation_num))
	fp.close()
	qrimg.add_header('Content-ID', '<%s>' % confirmation_num)
	email.attach(qrimg)
	
	return email




#For testing
if __name__ == '__main__':
	emailer = TicketConfirmation()
	emailer.generate_confirmation('a.patin96@gmail.com', 'Joe Kitonga Roast')
