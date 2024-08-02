import os
from aqt import mw
from aqt.qt import QAction, QFileDialog, QMessageBox
import fitz  # PyMuPDF

def search_in_pdf(word, pdf_path):
    doc = fitz.open(pdf_path)
    results = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if word.lower() in text.lower():
            results.append((page_num, text))
    return results

def show_search_dialog():
    word, ok = QFileDialog.getText(mw, "Search Word", "Enter the word to search:")
    if not ok or not word:
        return

    pdf_path, _ = QFileDialog.getOpenFileName(mw, "Select PDF File", "", "PDF files (*.pdf)")
    if not pdf_path:
        return

    results = search_in_pdf(word, pdf_path)
    if results:
        result_text = "\n\n".join([f"Page {page_num+1}:\n{text[:200]}..." for page_num, text in results])
        QMessageBox.information(mw, "Search Results", result_text)
    else:
        QMessageBox.information(mw, "Search Results", "No results found.")

# Create a menu item
action = QAction("Search in PDF", mw)
action.triggered.connect(show_search_dialog)
mw.form.menuTools.addAction(action)

