import sys
from utilities.imap4 import download_submitted_xml

def batch_acord_xmls_download():
    print("################################################################################")
    print("BATCH STARTING:")
    print("################################################################################")

    try:
        download_submitted_xml(verbose=True)
        print('################################################################################')
        print("BATCH COMPLETED")
        print('################################################################################')
    except Exception as e:
        print('################################################################################')
        print("BATCH FAILED: ", str(e))
        print('################################################################################')
        sys.exit(1)

if __name__ == "__main__":
    batch_acord_xmls_download()