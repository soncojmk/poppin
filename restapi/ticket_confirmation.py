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
                self.conn = psycopg2.connect("dbname=pop user=super host=soncojmk-178.postgres.pythonanywhere-services.com password=Munyao25# port=10178")
                self.cur = self.conn.cursor()


	#Check for confirmation num in db
	#if exists, check confirmed
		#if not confirmed, return named, set to confirmed
		#else return already confirmed
	#if not, return no entry	
	def confirm(self, confirmation_num): 
                try:
                        self.cur.execute("""SELECT * FROM "restapi_ticket" WHERE "confirmation_num"=%s;""", (confirmation_num,))
                        t = self.cur.fetchone()
                        if t[3] == 'confirmed':
                                return 'already confirmed'
                        else:
                                self.cur.execute("""UPDATE "restapi_ticket" SET "confirmed" = %s WHERE "confirmation_num" = %s;""", ('confirmed', confirmation_num,))
                                self.conn.commit()
                                return 'confirmed'
                except:
                        return 'invalid'


	#Generates a confirmation number and sends an email
	def generate_confirmation(self, to_address, event_name, user_id, username, charge_id):
		confirmation_num = str(uuid.uuid4()).replace('-', '')[0:10] #uses a uuid for confirmation number
		try:
			_generate_qr(confirmation_num)
		except:
			print('could not generate qr code')
		email = _generate_email(username, self.USERNAME, to_address, event_name, confirmation_num)
		try:
			self.SMTP.sendmail(self.USERNAME, to_address, email.as_string())
			print('sent email')
			os.remove('%s.png' % confirmation_num)
		except:
			print('could not send email')
		self.cur.execute("""INSERT INTO "restapi_ticket" ("email", "event_name", "confirmation_num", "confirmed", "user_id", "charge_id") VALUES (%s, %s, %s, %s, %s, %s)""",(to_address, event_name, confirmation_num, 'unconfirmed', user_id, charge_id))
		self.conn.commit()
                return confirmation_num

        def resend_confirmation(self, to_address, event_name, user_id, username):
                try:
                        self.cur.execute("""SELECT * FROM "restapi_ticket" WHERE "user_id"=%s AND "event_name"=%s;""", (user_id,event_name,))
                        t = self.cur.fetchone()
                        _generate_qr(t[1])
                        email = _generate_email(username, self.USERNAME, to_address, t[2], t[1])
                        self.SMTP.sendmail(self.USERNAME, to_address, email.as_string())
                        os.remove('%s.png' % t[1])
                        return t[1]
                except:
                        print('could not send email')


###############################################
# HELPER METHODS FOR TicketConfirmation
###############################################


###
#Email HTML template; change to include more information, fancify it, etc.
###
message_template = '''
Hey, {0}! <br><br>
You're all set to attend <i>{1}</i>! <br>
Your confirmation number is <b>{2}</b> <br><br>
Have fun!<br><br>
Sincerely,<br>
What's Poppin'<br><br>
<img src="cid{3}"><br><br>
<i>Please present your QR Code to your event host</i>
'''


#Generates QR png
def _generate_qr(confirmation_num):
	img = pyqrcode.create(confirmation_num)
	img.png('%s.png' %confirmation_num, scale=10)


#Generates an email with the qr code, based on the format of the template message
#Add additional attributes if needed
def _generate_email(name, from_address, to_address, event_name, confirmation_num):
	email = MIMEMultipart()
	email['Subject'] = 'Confirming Attendance to %s' % event_name
	email['From'] = from_address
	email['To'] = to_address

	#attaching message
	text = MIMEText(message_template.format(name, event_name, confirmation_num, confirmation_num), 'html')
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
