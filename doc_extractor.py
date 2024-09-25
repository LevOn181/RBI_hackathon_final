from gptwrapper import GPTWrapper
from utils import pdf, docx, pdf, txt, xlsx, csv

class DocumentTextExtractor:
    def __init__(self):
        self.wrapper = GPTWrapper()
        return

    def extract_text(self, file):
        print(file.mime)
        file_path = file.path
        #ext = os.path.splitext(file_path)[1].lower()
        if 'application/pdf' in file.mime:
            return pdf.extract_text_from_pdf(self.wrapper, file_path)
        elif 'spreadsheet' in file.mime:
            return xlsx.extract_text_from_excel(file_path)
        elif 'document' in file.mime:
            return docx.extract_text_from_docx(self.wrapper, file_path)
        elif 'text/plain' in file.mime:
            return txt.extract_text_from_txt(file_path)
        elif 'application/vnd.ms-excel' in file.mime:
            return csv.extract_text_from_csv(file_path)
        else:
            raise ValueError("File format is not supported! Upload IMAGE, TXT, CSV, PDF, DOCX or XLS(X).")
        
