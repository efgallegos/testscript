"""
Incoming Mail (IMAP) Server - Requires SSL
imap.gmail.com
Port: 993
Requires SSL:Yes
Outgoing Mail (SMTP) Server - Requires TLS
smtp.gmail.com
Port: 465 or 587
Requires SSL: Yes
Requires authentication: Yes
"""

from imaplib import IMAP4_SSL
from bs4 import BeautifulSoup as Soup
import email, os
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
    if verbose:
        print('***************************************************')
        print('save_zip_xml - STARTED')
        print('***************************************************')
    output_file_path = config_values['base_path'] + \
                  config_values['submitted_xmls'] + \
                  config_values['os_path_separator'] + \
                  file_name
    if verbose:            
        print('output_file_path: ', output_file_path)
        #print('file_content', file_content)
    
    try:
        with open(output_file_path, 'wb') as f:
            f.write(file_content)
        
        if verbose:
            print('***************************************************')
            print('save_zip_xml - COMPLETED: ZIP file was downloaded.')
            print('***************************************************')
    except Exception as e:
        if verbose:
            print('***************************************************')
            print('save_zip_xml - FAILED: ', str(e))
            print('***************************************************')
        raise e

    if verbose:
        print('ZIP file was downloaded successfully.')


def unzip_xml(file_name, verbose = False):
    if verbose:
        print('***************************************************')
        print('unzip_xml - STARTED')
        print('***************************************************')

    input_path_folder = config_values['base_path'] + \
                        config_values['submitted_xmls']

    if verbose:
        print('input_path_folder: ', input_path_folder)
        print('input_file_name: ', file_name)

    if os.getcwd() != input_path_folder:
        if verbose:
            print('Current directory: ', os.getcwd())
        os.chdir(input_path_folder)
        if verbose:
            print('Changed currect directory to: ', input_path_folder)

    if os.path.isfile(file_name):
        if verbose:
            print('Zip file exists and it is at: ', input_path_folder+config_values['os_path_separator']+file_name) 

        with ZipFile(file_name) as myzip:
            myzip.extractall()

        xml_filename = file_name.split('.')[0] + '.' + file_name.split('.')[1]
        
        if os.path.isfile(xml_filename):
            if verbose:
                print('ACORD xml file was successfully extracted.') 
                print('full_path: ', input_path_folder+config_values['os_path_separator']+xml_filename)
            os.remove(file_name)
            if verbose:
                print('Zip file deleted successfully.')
                print('***************************************************')
                print('unzip_xml - COMPLETED')
                print('***************************************************')
        else:
            if verbose:
                print('ACORD xml file extraction failed.')                 
                print('***************************************************')
                print('unzip_xml - FAILED')
                print('***************************************************')
            raise Exception('ACORD xml file extraction failed.')
    else:
        if verbose:
            print("Zip file doesn't exist in patch specified: ", input_path_folder+config_values['os_path_separator']+file_name) 
            print('***************************************************')
            print('unzip_xml - FAILED')
            print('***************************************************')
        raise Exception("Zip file doesn't exist in patch specified: ", input_path_folder+config_values['os_path_separator']+file_name) 


def rename_xml(file_name, verbose = False):
    if verbose:
        print('***************************************************')
        print('rename_xml - STARTED')
        print('***************************************************')

    input_path_folder = config_values['base_path'] + \
                        config_values['submitted_xmls']

    old_xml_name = file_name.split('.')[0] + '.' + file_name.split('.')[1]

    if verbose:
        print('input_path_folder: ',input_path_folder)
        print('os.getcwd():', os.getcwd())
        print('old_xml_name: ',old_xml_name)

    if os.getcwd() != input_path_folder:
        if verbose:
            print('Current directory: ', os.getcwd())
        os.chdir(input_path_folder)
        if verbose:
            print('changed currect directory to: ', input_path_folder)

    """
    clientid en UI     : e8b5eca9-6063-425b-bde4-3ef7971816b8
    entity_id en el PDF: e8b5eca9-6063-425b-bde4-3ef7971816b8
    <TrackingID>       : e8b5eca9-6063-425b-bde4-3ef7971816b8
    """

    with open(old_xml_name,'r') as handler:
        soup = Soup(handler)
        if soup.find(id="Primary_Insured"):
            element = soup.find(id="Primary_Insured")
            firstname = element.find('firstname').get_text()
            lastname = element.find('lastname').get_text()
        else:
            firstname = 'firstname'
            lastname = 'lastname'
        new_xml_name = lastname + '_' + firstname + '.xml'

    if verbose:
        print('new_xml_name: ',new_xml_name)

    os.rename(old_xml_name, new_xml_name)

    if os.path.isfile(new_xml_name):
    
        if verbose:
            print('**********************************************************')
            print('rename_xml - COMPLETED: The file was renamed successfully.')
            print('**********************************************************')
    else:
        if verbose:
            print('**********************************************************')
            print("rename_xml - FAILED: The file wasn't renamed.")
            print('**********************************************************')
        raise Exception("rename_xml - FAILED: The file wasn't renamed.")


def search(target='CASE_MANAGER', verbose=False):
    pass



def download_submitted_xml(verbose=False):
    #log in and select the inbox
    try:
        # number of ACORD xmls downloaded
        xmls_files_downloaded = 0

        m = email_login(verbose)
        
        #Set focus on folder (label): "Bankers/XML"
        m.select('Bankers/XML')

        #get uids of all messages
        r_search, data = m.uid('search', None, 'UNSEEN')
        uids = data[0].split()

        if r_search == 'OK':            
            if verbose:
                print('Search finished successfully.')
                print('r_search: ', r_search)
                print('data: ', data)

            if len(uids) != 0:
                for uid in uids:            
                    #read the lastest message
                    r_fetch, data = m.uid('fetch', uid, '(RFC822)')
                    
                    if r_fetch == 'OK': 
                        # Create email instance
                       
                        try:
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
                                    xmls_files_downloaded += 1
                        except Exception as e:
                            print('Error: ', str(e))
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
            print('download_submitted_xml - Unhandle exception. More details: ' + str(e))
        raise e
        
