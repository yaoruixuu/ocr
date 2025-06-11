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
    blob.download_to_filename(pdf_destination)


def pdf_reader(pdf):
    reader = PdfReader(pdf)
    number_of_pages = len(reader.pages)

    
    page = reader.pages[3]
    text = page.extract_text()

    bool_searchable = not(len(text) == 0)

    text_to_csv(text)

    if bool_searchable:
        searchable.append(pdf)

    else:
        non_searchable.append(pdf)
   

def text_to_csv(text):
    text_seperated = text.split(".")
    
    lst=[]
    for item in text_seperated:
        lst.append(item.split())
       
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lst)

def ocr_sorting_pipeline(files):
    log = []
    log.append(["file path", "searchable"])
    for file in files:
        pdf_reader(file)

        if file in searchable:
            log.append([file, "yes"])
        else:
            log.append([file, "no"])

    with open('log.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(log)


#ocr_sorting_pipeline(["/Users/yaoruixu/Downloads/calc2final_answers.pdf", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf",])

#pdf_reader("/Users/yaoruixu/Downloads/calc2final_answers.pdf")

#download_pdf("ocr-pdf-bucket-68", "karpathy_paper", "/Users/yaoruixu/Downloads/download_test1.pdf")

# upload_blob("ocr-pdf-bucket-68", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf", "karpathy_paper")

# list_pdfs("ocr-pdf-bucket-68")