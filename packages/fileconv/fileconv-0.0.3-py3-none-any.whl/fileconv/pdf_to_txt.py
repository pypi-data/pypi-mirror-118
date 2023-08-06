"""
This class will convert .pdf's back to .txt
It uses 'PyPDF2' to execute this task.


@Author: ovanov
@Date: 30.08.21
"""

import os

import PyPDF2


class Pdf():

    @staticmethod
    def to_text(text, *args):
        """
        converts pdf to txt and uses filepath from converter
        """
        content = ''
        with open(text, "rb") as f:
            #create reader variable that will read the pdf_obj
            pdfreader = PyPDF2.PdfFileReader(f)
            
            for num in range(pdfreader.numPages):
                content += pdfreader.getPage(num).extractText()

        file_loc_and_name = str(os.path.join(args[2], args[1][:-4])) + ".txt" 
        with open(file_loc_and_name, "w", encoding='utf-8') as T:
            T.writelines(content)

        return