import fitz  # PyMuPDF
import csv

def pdf_to_csv(pdf_path, csv_path, delimiter=','):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Create a CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter)

        for page_num in range(len(pdf_document)):
            # Extract text from each page
            page = pdf_document.load_page(page_num)
            text = page.get_text()

            # Split the text into lines
            lines = text.strip().split('\n')

            # Extract header line
            header = lines[0].strip().split(delimiter)

            # Write header line to CSV (only if it's the first page)
            if page_num == 0:
                csv_writer.writerow(header)

            # Write data lines to CSV
            for line in lines[1:]:
                # Split the line into columns based on the delimiter
                columns = line.strip().split(delimiter)
                # Write the columns to CSV
                csv_writer.writerow(columns)

    # Close the PDF
    pdf_document.close()

# Example usage:
pdf_to_csv(r"C:\Users\HP\OneDrive - iitgn.ac.in\Desktop\EE2.pdf", 'oput.csv')
