"""
This class will holds different crawler functions
for the different tasks 


@Author: ovanov
@Date: 31.08.21
"""
import os
import pathlib

from tqdm.std import tqdm

from .office_to_pdf import MS
from .txt_to_pdf import Conv
from .pdf_to_txt import Pdf


class Crawler():

    @staticmethod
    def crawl(p, output):
        """
        This function takes the path variable "p" and goes over all directories 
        """
        dir_len = len(next(os.walk(p))[1])
        for root, dirs, files in tqdm(os.walk(p), total=dir_len):
            #os.walk yields a 3-tuple of strings, wich can be concatenated
            if len(root) != 0:
                # maybe the directory is empty or yields no files (empty list), we should make sure that there is no error
                for filename in files:

                    ext = pathlib.Path(filename).suffix # get file extension

                    if ext == ".docx" or ext == ".doc":
                        file = os.path.join(root, filename)
                        MS.word_to_pdf(file, ext, filename, output)

                    elif ext == ".xlsx" or ext == ".xls":
                        file = os.path.join(root, filename)
                        MS.excel_to_pdf(file, ext, filename, output)

                    elif ext == ".txt":
                        file = os.path.join(root, filename)
                        Conv.txt_to_pdf(file, filename, output) #TODO add the txt class
                    
                    else:
                        pass
        
            else:
                raise KeyError("The directory is empty")
        return

    @staticmethod
    def pdf_crawl(p, output):
        """
        This function takes the path variable "p" and goes over all directories 
        """
        for root, dirs, files in os.walk(p):
            #os.walk yields a 3-tuple of strings, wich can be concatenated
            if len(root) != 0:
                # maybe the directory is empty or yields no files (empty list), we should make sure that there is no error
                for filename in tqdm(files):

                    ext = pathlib.Path(filename).suffix # get file extension

                    if ext == ".pdf":
                        file = os.path.join(root, filename)
                        Pdf.to_text(file, ext, filename, output)
                    
                    else:
                        pass
        
            else:
                raise KeyError("The directory is empty")
        return