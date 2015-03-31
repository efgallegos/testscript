"""
Many clients will automatically configure the appropriate IMAP connection settings for your account, but confirm that the connection settings your client configures are the same as what's listed below.

If you're using a client that's not listed above, you can also use the following information to configure your IMAP. If you have problems, contact your mail client's customer support department for further instructions.

Incoming Mail (IMAP) Server - Requires SSL
imap.gmail.com
Port: 993
Requires SSL:Yes
Outgoing Mail (SMTP) Server - Requires TLS
smtp.gmail.com
Port: 465 or 587
Requires SSL: Yes
Requires authentication: Yes
Use same settings as incoming mail server
Full Name or Display Name: [your name]
Account Name or User Name: your full Gmail address (username@gmail.com). Google Apps users, please enter username@your_domain.com
Email address: your full Gmail address (username@gmail.com) Google Apps users, please enter username@your_domain.com
Password: your Gmail password
If your client does not support SMTP authentication, you won't be able to send mail through your client using your Gmail address.

Also, if you're having trouble sending mail but you've confirmed that encryption is active for SMTP in your mail client, try to configure your SMTP server on a different port: 465 or 587.
"""

from imaplib import IMAP4_SSL
import email, re, os
from zipfile import ZipFile
from config_entries import config_values

def email_login(verbose = False):
    if verbose:
        print('host: imap.gmail.com')
        print('port=993')
        print('username: ', config_values['email_user'])
        print('password:', config_values['email_pass'])

    try:
        mail = IMAP4_SSL(host='imap.gmail.com', port = 993)
        result, message = mail.login(config_values['email_user'], config_values['email_pass'])
        if result == 'OK':
            print('IMAP4_SSL connection to host was created successfully.')
            if verbose:                
                print('result: ', result)
                print('message:', message[0])
            return mail
    except Exception as e:
        print('failed to create IMAP4_SSL conection to host.')            
        raise e
    

def email_logout(mail, verbose = False):
    # Shutdown connection to server. Returns server BYE response.
    result = mail.logout()
    if verbose:
        if result == 'BYE':
            print('IMAP4_SSL shutdown connection to host successfully.')
        else:
            print('IMAP4_SSL shutdown connection to host failed.')


def save_zip_xml(file_name, file_content, verbose = False):   
    output_path = config_values['base_path'] + \
                  config_values['submitted_xmls'] + \
                  config_values['os_path_separator'] + \
                  file_name
    if verbose:            
        print('output_path: ', output_path)
    
    with open(output_path, 'wb') as f:
        f.write(file_content)

    if verbose:
        print('ZIP file was downloaded successfully.')


def unzip_xml(file_name, verbose = False):
    input_path_folder = config_values['base_path'] + \
                        config_values['submitted_xmls'] + \
                        config_values['os_path_separator'] 

    input_path_file = input_path_folder + file_name

    if verbose:
        print('input file full path: ', input_path_file)

    with ZipFile(input_path_file) as myzip:
        myzip.extractall()
        print('zip file extract successfully')

    if os.getcwd() != input_path_folder:
        os.chdir(input_path_folder)
        if verbose:
            print('changed currect directory to: ', input_path_folder)

    os.remove(input_path_file)
    if verbose:
        print('zip file deleted successfully.')


def rename_xml(file_name, verbose = False):
    old_file_name = file_name.split('.')[0] + '.' + file_name.split('.')[1]

    input_path_folder = config_values['base_path'] + \
                        config_values['submitted_xmls'] + \
                        config_values['os_path_separator'] 

    input_path_file = input_path_folder + old_file_name

    new_file_name = ''     

    with open(input_path_file, 'r') as f:
        for line in f:
            if re.search("PIFullName", line):
                # <Data Name="PIFullName">STC X GR-N320 </Data>
                new_file_name = line[line.find('>') + 1 : line.find('<',line.find('>') + 1)] + '.xml'
                break

    if os.getcwd() != input_path_folder:
        os.chdir(input_path_folder)
        if verbose:
            print('changed currect directory to: ', input_path_folder)

    os.rename(old_file_name, new_file_name)
    
    if verbose:
        print('The file was renamed successfully.')


def download_submitted_xml(verbose=False):
    #log in and select the inbox
    try:
        # number of ACORD xmls downloaded
        xmls_files_downloaded = 0

        m = email_login(verbose)
        
        #Set focus on folder (label): "Bankers/XML"
        m.select('Bankers/XML')

        #get uids of all messages
        r_search, data = m.uid('search', None, 'NEW')
        uids = data[0].split()

        if r_search == 'OK':            
            if verbose:
                print('Search finished successfully.')
                print('r_search: ', r_search)
                print('data: ', data)

            if uids.len() != 0:
                for uid in uids:            
                    #read the lastest message
                    r_fetch, data = m.uid('fetch', uid, '(RFC822)')
                    
                    if r_fetch == 'OK': 
                        # Create email instance
                        em = email.message_from_bytes(data[0][1])

                        if verbose:
                            print('email object created successfully.')

                        if em.get_content_maintype() == 'multipart': #multipart messages only
                            for part in em.walk():
                                # find the attachment part
                                if part.get_content_maintype() == 'multipart': continue
                                if part.get('Content-Disposition') is None: continue
                                # get file name
                                filename = part.get_filename()
                                # save zip file
                                save_zip_xml(filename,part.get_payload(decode=True), verbose)
                                # extract ACORD XML file and delete zip file.
                                unzip_xml(filename, verbose)
                                # remame ACORD XML file
                                rename_xml(filename, verbose)
                        em.close()
                        xmls_files_downloaded += 1
                    else:
                        print('Fetch failed.')
                        if verbose:
                            print('r_fetch: ', r_fetch)
                            print('data: '. data)
                print('Download submitted ACORD xmls completed. Number of files downloaded: ', xmls_files_downloaded)
            else: 
                print('No NEW ACORD xmls to download')
        else:
            print('Search failed.')
            if verbose:                
                print('r_search: ', r_search)
                print('data: ', data)
        email_logout(m)
    except Exception as e:
        if verbose:
            print('download_submitted_xml - Unhandle exception. More details: ' + e.value)
        
