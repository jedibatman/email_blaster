#!/usr/bin/python
#imports
import threading
from itertools import izip, chain, repeat

#needs to be set
EMAIL_FILE = ''
#needs to be set
LOG_FILE = ''
#needs to be set
BAD_EMAILS = ''
#needs to be set
NUM_THREADS = 10

def main():
    #Declarations
    #needs to be reset based on which OS the csv file was generated on...
    separator = ',\r\n'
    FH_EMAIL = open(EMAIL_FILE, 'r')
    emailList = FH_EMAIL.read().split(separator)
    FH_EMAIL.close()
    #partition email list into two equal parts
    email_groups = list(grouper((len(emailList) / NUM_THREADS) + 1, emailList))

    lock = threading.Lock()
    jobs = []
    threadNum = 1
    for group in email_groups:
        print 'Thread {} started...'.format(threadNum)
        t = threading.Thread(target = sendEmail, args = (group, threadNum))
        jobs.append(t)
        t.start()
        threadNum += 1

    print 'entering infinity...'
    while 1:
        pass


    # print 'Sending emails started...'
    # sendEmail(emailList)

##
# @param: n is the size of each partition
# @param: iterable is the object to split up
# @param: padvalue is the item to use when the iterable is exhausted
#
def grouper(n, iterable, padvalue=None):
    return izip(*[chain(iterable, repeat(padvalue, n - 1))]*n)

def sendEmail(listToSend, thread_num):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    #function to send actual emails
    #declarations
    #needs to be set
    HTML_SUBJECT = "This is the email subject"
    #needs to be set
    EMAIL_FROM_FIELD = 'senderemail@email.com'
    #needs to be set
    HTML_BODY_INFILE = 'name of html email body here'
    FH_BODY_EMAIL = open(HTML_BODY_INFILE, 'r')
    EMAIL_BODY = FH_BODY_EMAIL.read()
    FH_BODY_EMAIL.close()
    mimeBody = MIMEText(EMAIL_BODY, 'html')

    print 'Greetings from thread {}.'.format(thread_num)

    #smtp account auth info
    #needs to be set
    USERNAME = 'smtp_username_here'
    #needs to be set
    PASSWORD = 'smtp_password_here'
    #needs to be set
    SMTP_SERVER = 'smtp_server_name_here'
    PORT = 25

    lock.acquire()
    #connect to smtp server
    server = smtplib.SMTP(SMTP_SERVER, PORT)

    #if tls is supported
    #server.starttls()

    print 'Thread {} attempting connection to smtp server...'.format(thread_num)
    server.login(USERNAME, PASSWORD)
    print 'Thread {} successfully connected to smtp server!'.format(thread_num)
    lock.release()

    for email_to_field in listToSend:
        #build email
        email_msg = MIMEMultipart()
        mimeBody = MIMEText(EMAIL_BODY, 'html')
        email_msg['Subject'] = HTML_SUBJECT
        email_msg['From'] = EMAIL_FROM_FIELD
        email_msg.attach(mimeBody) 
        email_msg['To'] = email_to_field.strip()
        try:
            server.sendmail(EMAIL_FROM_FIELD, email_to_field, email_msg.as_string())
        except Exception as e:
            print 'Unable to send email. An exception occurred: {} :::: Email address error on: {}'.format(e, email_to_field)
            FH_LOG_FILE = open(LOG_FILE, 'a+')
            FH_BAD_EMAILS = open(BAD_EMAILS, 'a+')
            FH_LOG_FILE.write('Unable to send email. An exception occurred: {}\n'.format(e))
            FH_BAD_EMAILS.write('{}'.format(email_to_field))
            FH_LOG_FILE.close()
            FH_BAD_EMAILS.close()
            continue

        print 'Email sent to {}'.format(email_to_field)
        del email_msg
    
    server.quit()

if __name__ == '__main__':
    main()
