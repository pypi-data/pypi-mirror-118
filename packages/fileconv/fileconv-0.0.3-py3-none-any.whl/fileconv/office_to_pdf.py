"""
This class will convert .docx or .doc & .xlsx or .xls / .csv to .pdf
It uses 'docx2pdf' & 'win32' to execute this task.


@Author: ovanov
@Date: 26.03.21
"""
import os

import win32com.client
from fpdf import FPDF


class MS():

    @staticmethod
    def word_to_pdf(word, ext, *args):
        """
        converts docx to pdf and uses the filepath from converter
        """
        file_loc_and_name = str(os.path.join(args[1], args[0][:-len(ext)])) + ".pdf" 
        o = win32com.client.Dispatch('Word.Application')
        o.Visible = False
        doc = o.Documents.Open(word)
        o.DisplayAlerts = False
        doc.SaveAs(file_loc_and_name, FileFormat=17)
        o.DisplayAlerts = True
        doc.Close()
        o.Quit()

        return

    @staticmethod
    def excel_to_pdf(excel,ext, *args):
        """
        converts xlsx to pdf and uses the filepath from converter
        """        
        file_loc_and_name = str(os.path.join(args[1], args[0][:-len(ext)])) + ".pdf"
        xlApp = win32com.client.Dispatch("Excel.Application")
        xlApp.Visible = False
        books = xlApp.Workbooks.Open(excel)
        xlApp.DisplayAlerts = False
        books.SaveAs(file_loc_and_name, FileFormat=57)
        xlApp.DisplayAlerts = True
        books.Close()
        xlApp.Quit()

        return