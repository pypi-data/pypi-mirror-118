"""
This class will convert .txt to .pdf
It uses 'fpdf' to execute this task.


@Author: ovanov
@Date: 30.08.21
"""
import os

from fpdf import FPDF


class Conv():

    @staticmethod
    def txt_to_pdf(text, *args):
        """
        converts txt to pdf and uses the filepath from converter
        """
        pdf = FPDF()
        pdf.add_page()

        # set style and size of font 
        # that you want in the pdf
        pdf.set_font("Arial", size = 12)

        # open the text file in read mode

        with open(text, "r") as f:
        # insert the texts in pdf
            for x in f:
                pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
        # save the pdf with name .pdf
        file_loc_and_name = str(os.path.join(args[1], args[0][:-4])) + ".pdf" 
        pdf.output(file_loc_and_name) 

        return