import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your SMTP server and port
    server.starttls()
    server.login('rashadbackup11@gmail.com', 'pvvt clfp kshl jgpl')
    print('SMTP connection successful')
    server.quit()
except Exception as e:
    print('SMTP connection failed:', e)
