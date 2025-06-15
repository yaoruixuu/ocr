Example usage:

Pass document to sorting pipeline:
ocr_sorting_pipeline(["/Users/yaoruixu/Downloads/calc2final_answers.pdf", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf",])

To determine if document is searchable: 
pdf_reader("/Users/yaoruixu/Downloads/calc2final_answers.pdf")

To download file from bucket:
download_blob("ocr-pdf-bucket-68", "karpathy_paper", "/Users/yaoruixu/Downloads/download_test1.pdf")

To to upload local file to bucket:
upload_blob("ocr-pdf-bucket-68", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf", "karpathy_paper")

To list all PDFs to a bucket:
list_pdfs("ocr-pdf-bucket-68")

To evaluate Levenshtein distance between two documents:
evaluation_script("/Users/yaoruixu/dev/orc/demofile.txt", "/Users/yaoruixu/dev/orc/ground_truth.txt")
    
OCR on file:
async_document_detection("gs://ocr-pdf-bucket-68/gadget", "gs://ocr-output-1/ocr-output")
