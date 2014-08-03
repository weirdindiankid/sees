SEES
====

### Türkçe

http://www.galkan.net/2014/01/sees-ile-sosyal-muhendislik-saldirisi-icin-eposta-oltalama-araci.html

### English

http://www.galkan.net/2014/02/sees-social-engineering-email-sender.html

A Social Engineering Attack/Audit Tool for Spear Phishing

 What is SEES?

 Most of the companies nowadays have their firewalls, threat monitoring and prevention security appliances setup. With these mechanisms in place, security precautions are taken and incidents are monitored. Inbound traffic being restricted, SEES on the other hand is developed for sending targeted phishing emails in order to carry sophisticated social engineering attacks/audits.

 SEES aims to increase the success rate of phishing attacks by sending emails to company users as if they are coming from the very same company’s domain. The attacks become much more sophisticated if an attacker is able to send an email, which is coming from ceo@example.org email address, to a company with domain example.org. 

 Example SMTP Service Configuration

 It is possible to send emails with or without attachments with SEES. But first, a working SMTP service is needed to send an email. Here, postfix service will be used as an example. On Kali linux this can easily be achieved by using the package management system;


 # apt-get install postfix

 After the installation the configuration of SMTP server is needed. An example configuration file is shown below. Other configurational alternatives are possible, too. 

 # cat /etc/postfix/main.cf  | grep -Ev "^#|^$"
smtpd_banner = See you soon
biff = no
append_dot_mydomain = no
readme_directory = no
smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_use_tls=yes
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
myhostname = mail.example.com
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
myorigin = /etc/mailname
mydestination = mail.example.com, localhost.example.com, , localhost
relayhost =
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mailbox_size_limit = 0
recipient_delimiter = +
message_size_limit = 314572800
inet_interfaces = 127.0.0.1

 After the installation and configuration postfix is re/started.

 # /etc/init.d/postfix start

 A simple netstat command can be executed to check if the service is up and running.

 # netstat -nlput | grep 25
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      13707/master

 Downloading & Configuring SEES

 The source code and downloadables can be reach at https://github.com/galkan/sees. First of all, the dependencies should be resolved for Backtrack installations (for Kali there’s no need to execute this step).

 # apt-get install python-argparse
# wget https://github.com/galkan/sees/archive/master.zip
# unzip master.zip

 SEES configuration file includes the domain parameter under the [mail] section, server and time parameters under the [smtp] section. config.cfg file under the config/ directory that comes with the SEES installation can be analyzed.

 domain: This parameter notes the source domain names that the target SMTP server will get the phishing emails. 

 SEES produces emails using random domain names in order to prevent target system to classify original phishing emails as spam. The function that implements this behaviour is shown below;

 def random_email(self):
                """
                        Create random string for sending email so that target email server doesn't recognize that this is a spam email ...
                """
                chars_1 = "".join( [random.choice(string.letters) for i in xrange(self.num1)] )
                chars_2 = "".join( [random.choice(string.letters) for i in xrange(self.num2)] )
                return  chars_1 + "." + chars_2

 server: This parameter notes the source SMTP server that the phishing emails will be sent from. Server living on 127.0.0.1 will be used easily preventing any authorization & authentication mechanisms.

 time: This parameter notes the time differences between sent emails. With this behaviour target SMTP servers are tried to be fooled in order not to classify the original phishing emails as spam. Two options are possible to determine the time differences. One of them is a fixed time period and this is the easy one. The other alternative is using a time range with a comma between, such as 1,3. This denotes waiting a random time difference between 1 and 3 seconds each time before sending a  phishing email.

 An example configuration file is shown below;

 # cat config/config.cfg
[mail]
domain = example.com
[smtp]
server = 127.0.0.1
time = 1,3

 Structure of Emails sent by SEES

 The structure of emails are represented in the following way;

 From Email:From Name Surname:Email Subject:Target Email

 Name, surname and the subject parts are obvious. The From Email parameter denotes the from email address, such as, mail_from@example.com. And Target Email parameter denotes the target email address, such as, mail_to@example.com.

 The below file includes two definitions of emails that are wanted to be sent. In order program to stop, and exit command should be entered. The definitions after the exit statement will be discarded.

 # cat config/mail.user
MANAGER@example.com:Gökhan ALKAN:About Salary:mail_to@gmail.com
MANAGER2@example.com:Gökhan ALKAN:About Salary:mail_to@gmail.com
exit

 --text parameter denotes that the email will not have an attachment but will only include a text message. If the email should include HTML text then the HTML file name should be indicated after the --html_file parameter.

 # cat data/html.text
<html>
        example content
</html>

 --attach parameter denotes the file names of attachments. More than one file names can be attached with a space between. Moreover, if the email should include text then the file name should be indicated after the --html_file parameter. But the file content shouldn’t be in HTML. If the mail message should be empty then the file should be empty. An example content is shown below;

 # cat data/attach.text
example content

 SEES Use Cases

 Scenario 1: Emails with no attachment

 An example of sending emails with message content only is shown below.

 # ./sees.py --text --config_file config/config.cfg --mail_user config/mail.user --html_file data/html.text -v
Using SEES for malicious purposes is illegal. USE AT YOUR OWN RISK, Agree (Y|n)
Y
[+] MANAGER@example.com -> mail_to@gmail.com
[+] MANAGER2@example.com -> mail_to@gmail.com


 -v parameter prints the sent email on the screen for debugging purposes. The targeted user’s  email client will show MANAGER@example.com as the sender for the first email but the target SMTP server will process the same email as it is coming from tUniKSr.fPrAin@example.com. As it was pointed out before, the random email addresses are formed in order the target SMTP server to classify these emails as spam.

 ...
Return-Path: <tUniKSr.fPrAin@example.com>
From: MANAGER@example.com
..
Scenario 2: Emails with attachments

 An example of sending emails with attachments is shown below.
# ./sees.py --attach data/sample.pdf data/sample.docx --config_file config/config.cfg --mail_user config/mail.user --html_file data/attach.text -v


Using SEES for malicious purposes is illegal. USE AT YOUR OWN RISK, Agree (Y|n)
Y
[+] MANAGER@example.com -> mail_to@gmail.com
[+] MANAGER2@example.com -> mail_to@gmail.com


 The attached files are pointed with file names after the --attach parameter with a single space in between. sample.pdf and sample.docx are used as attachments with the example above.

 -v parameter prints the sent email on the screen for debugging purposes. The targeted user’s  email client will show MANAGER@example.com as the sender for the first email but the target SMTP server will process the same email as it is coming from PfFYyS.YtODLA@example.cpm. As it was pointed out before, the random email addresses are formed in order the target SMTP server to classify these emails as spam.

 ...
Return-Path: <PfFYyS.YtODLA@example.com>
From: MANAGER2@example.com
…

 Disclaimer

Using SEES for malicious purposes is illegal. USE AT YOUR OWN RISK
