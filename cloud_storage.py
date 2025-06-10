from google.cloud import storage
import google.auth

# get creds
credentials, project = google.auth.default()



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

    


#inconclusive test, network too slow
#download_pdf("ocr-pdf-bucket-68", "karpathy_paper", "/Users/yaoruixu/Downloads/download_test1.pdf")

# upload_blob("ocr-pdf-bucket-68", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf", "karpathy_paper")

# list_pdfs("ocr-pdf-bucket-68")