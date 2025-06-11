Example usage:

ocr_sorting_pipeline(["/Users/yaoruixu/Downloads/calc2final_answers.pdf", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf",])

pdf_reader("/Users/yaoruixu/Downloads/calc2final_answers.pdf")

download_pdf("ocr-pdf-bucket-68", "karpathy_paper", "/Users/yaoruixu/Downloads/download_test1.pdf")

upload_blob("ocr-pdf-bucket-68", "/Users/yaoruixu/Downloads/LargeScale_paper.pdf", "karpathy_paper")
list_pdfs("ocr-pdf-bucket-68")
