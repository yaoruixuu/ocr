from google.cloud import storage
import google.auth

from pypdf import PdfReader
import csv

# get creds
credentials, project = google.auth.default()

# searchable and non-searchable PDFs
searchable = []
non_searchable = []



def upload_blob(bucket_name,  source_file_name, destination_blob_name):
    '''Uploads a local file to the bucket'''

    # create client
    storage_client = storage.Client()
    # get bucket
    bucket = storage_client.bucket(bucket_name)
    # get blob
    blob = bucket.blob(destination_blob_name)

    #  generation-match precondition
    generation_match_precondition = 0

    # upload to blob
    blob.upload_from_filename(source_file_name, if_generation_match = generation_match_precondition)

    print(f"File {source_file_name} uploaded to {bucket_name}")


def list_pdfs(bucket_name):
    '''Lists out pdfs in specified bucket'''

    # create client
    storage_client = storage.Client()
    # get bucket
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs()
    print("PDFs:")

    for blob in blobs:
        print(blob.name)

def download_pdf(bucket_name, pdf_name, pdf_destination):
    '''Downloads specified pdf from bucket_name'''

    # create client
    storage_client = storage.Client()
    # get bucket
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(pdf_name)

    # download bucket
    blob.download_to_filename(pdf_destination)

    print(f"File {pdf_name} downloaded to {pdf_destination}")


def pdf_reader(pdf):
    '''Pdf reader which determines if searchable or not and appends to correct list'''

    # create Reader obj
    reader = PdfReader(pdf)

    text = ""
   
    # extract text
    for page in reader.pages:
        text = text + page.extract_text()

    bool_searchable = not(len(text) == 0)

    # write text to output.csv
    text_to_csv(text)

    if bool_searchable:
        searchable.append(pdf)

    else:
        non_searchable.append(pdf)
   

def text_to_csv(text):
    '''Writes text to output.csv file, each sentence is a new row'''

    text_seperated = text.split(".")
    
    lst=[]
    for item in text_seperated:
        lst.append(item.split())
    
    # write to csv file
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lst)

def ocr_sorting_pipeline(files):
    ''' OCR pipeline which logs searchable pdfs'''

    log = []
    log.append(["file path", "searchable"])
    for file in files:
        pdf_reader(file)

        if file in searchable:
            log.append([file, "yes"])
        else:
            log.append([file, "no"])

    # write to csv file
    with open('log.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(log)


