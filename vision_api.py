
from google.cloud import vision
from google.cloud import storage
import json
import re


def async_document_detection(gcs_source_uri, gcs_destination_uri):
    '''async ocr on document gcs_source_uri, output results to gcs_destination_uri'''

    # type
    mime_type = "application/pdf"

    # output file max pages
    batch_size = 1

    # client
    client = vision.ImageAnnotatorClient()

    # feature specification
    feature = vision.Feature(type_ = vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    # configure source
    gcs_source = vision.GcsSource(uri = gcs_source_uri)

    input_config = vision.InputConfig(gcs_source = gcs_source, mime_type = mime_type)

    # configure destination
    gcs_destination = vision.GcsDestination(uri = gcs_destination_uri)

    output_config = vision.OutputConfig(gcs_destination = gcs_destination, batch_size = batch_size)

    # create request
    async_request = vision.AsyncAnnotateFileRequest(features = [feature], input_config = input_config, output_config = output_config)

    operation = client.async_batch_annotate_files(requests = [async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    storage_client = storage.Client()

    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)


    bucket = storage_client.get_bucket(bucket_name)

    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]

    # sort json files numerically
    blob_list.sort(key=lambda blob: extract_page_number(blob.name))

    print("Output files:")
    for blob in blob_list:
        print(blob.name)



    # print and write pages
    page_count = 1
    print("Full text:\n")
    with open("demofile.txt", "w") as f:
            f.write("----------Text After OCR-----------\n\n")
    for blob in blob_list:
        json_string = blob.download_as_bytes().decode("utf-8")
        response = json.loads(json_string)

        first_page_response = response["responses"][0]
        annotation = first_page_response["fullTextAnnotation"]

        with open("demofile.txt", "a") as f:
            f.write(f"\n--------Page {page_count}--------\n")
            f.write(annotation["text"])
            page_count += 1

        #print(annotation["text"])

 


def extract_page_number(blob_name):
    '''extract page number from filename'''
    match = re.search(r'ocr-outputoutput-(\d+)-to-\d+\.json', blob_name)
    if match:
        return int(match.group(1)) # Convert the captured string to an integer
    return 0 # Default if pattern not found (shouldn't happen with valid filenames)

    
def evaluation_script(filepath, ground_truth_filepath):
    '''print and return levenshtein distance between document and ground truth'''

    from Levenshtein import distance

    with open(ground_truth_filepath, 'r') as file:
        ground_truth = file.read()

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    distance = distance(content, ground_truth)

    print("Score:" + str(distance))

    print("Accuracy: "+ str((len(content) - distance)/len(content)*100)+"%")
    
    return distance





