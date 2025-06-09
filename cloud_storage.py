from google.cloud import storage

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

