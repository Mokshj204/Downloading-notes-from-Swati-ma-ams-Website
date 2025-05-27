import os
import requests
from PyPDF2 import PdfMerger
import time

# Function to download a PDF
def download_pdf(url, temp_path):
    global stop
    retries = 3  # Number of retries
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {temp_path}")
                return  # Exit if download is successful
            else:
                print(f"Failed to download: {url} - Status Code: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
    stop = True

# Function to merge multiple PDFs into one
def merge_pdfs(pdf_files, output_pdf):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_pdf)
    merger.close()
    print(f"Merged PDF saved as: {output_pdf}")

# Main function to download and merge PDFs for unique IDs
def download_and_merge_pdfs(urls_with_ids, max_page_num):
    global stop
    all_pdf_files = []  # List to hold all the PDF paths to be merged into one file
    temp_dir = 'temp_pdfs'
    os.makedirs(temp_dir, exist_ok=True)
    
    for base_url, unique_ids in urls_with_ids.items():
        for unique_id in unique_ids:
            for page_num in range(1, max_page_num + 1):
                # Form the URL for the current PDF
                pdf_url = f"{base_url}/{unique_id}_{page_num}.pdf"
                
                # Define the temp file path for each downloaded page
                temp_path = os.path.join(temp_dir, f"{unique_id}_{page_num}.pdf")
                
                # Download the PDF
                download_pdf(pdf_url, temp_path)
                if stop:
                    stop = False
                    break
                # Add the downloaded PDF file path to the list
                all_pdf_files.append(temp_path)
        
        if stop:  # Stop if there was a failure during downloading
            break
    
    # Define the output path for the merged PDF
    output_pdf = "merged_all_lectures.pdf"
    
    # Merge all downloaded PDFs into one
    merge_pdfs(all_pdf_files, output_pdf)
    
    # Optionally, clean up the temporary PDF files after merging
    for pdf in all_pdf_files:
        os.remove(pdf)
    os.rmdir(temp_dir)  # Remove the temp directory

# Example usage
base_urls_with_ids = {
    "https://www.swatimaurya.in/el/dm/Lecture3.1/files/page/": ["20241003011128277"],
    "https://www.swatimaurya.in/el/dm/Lecture3.2/files/page/": ["20241003011225897"],
    "https://www.swatimaurya.in/el/dm/Lecture3.3/files/page/": ["20241003011256991"],
    "https://www.swatimaurya.in/el/dm/Lecture3.4/files/page/": ["20241003011328119"],
    "https://www.swatimaurya.in/el/dm/Lecture3.5/files/page/": ["20241003011433627"]
}

# Maximum number of pages for each unique ID (adjust based on actual data)
max_page_num = 50

stop = False
# Start the download and merge process
download_and_merge_pdfs(base_urls_with_ids, max_page_num)
