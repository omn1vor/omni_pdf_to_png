"""
This is a simple wrapper for PyMuPDF (https://github.com/pymupdf/PyMuPDF)
This utility converts a pdf file to N png files, a png file for each page.
Png files are created in the same directory as the original png, with the same name + N

Parameters:
    - filename, the filename of your pdf, e.g. 'test.pdf'
    - horizontal zoom ratio, e.g. 0.5 or 2
    - vertical zoom ratio, e.g. 0.5 or 2
"""

import fitz
import sys

def main():
    
    if len(sys.argv) < 2:
        print("Program needs at least one parameter - the filename of your pdf, e.g. 'test.pdf'")
        return

    filename = str(sys.argv[1]).strip()
    if filename in(["?", "/help", "-help"]):
        print(__doc__)
        return

    x_zoom = 1
    y_zoom = 1

    if len(sys.argv) > 2:
        try:
            x_zoom = float(sys.argv[2])
        except Exception as err:
            print(f"Second parameter should be a number for horizontal zoom ratio, but we got this: {sys.argv[2]}")
            return
        if x_zoom < 0:
            print(f"Horizontal zoom ratio should be positive, but we got this: {sys.argv[2]}")
            return

    if len(sys.argv) > 3:
        try:
            y_zoom = float(sys.argv[3])
        except Exception as err:
            print(f"Third parameter should be a number for vertical zoom ratio, but we got this: {sys.argv[3]}")
            return
        if y_zoom < 0:
            print(f"Vertical zoom ratio should be positive, but we got this: {sys.argv[3]}")
            return

    zoom_matrix = None
    if not (x_zoom == 1 and y_zoom == 1):
        zoom_matrix = fitz.Matrix(x_zoom, y_zoom)

    try:
        doc = fitz.open(filename)
    except Exception as err:
        print(f"Error while opening the file {filename}: {err}")
        return
    
    if doc.page_count > 999:
        print("the pdf file contains more than 999 pages, our simple program can't handle it")
        return

    for page_num in range(doc.page_count):
        page = doc.loadPage(page_num)  # number of page
        pix = page.getPixmap(matrix=zoom_matrix)       
        output = f"{filename}_{page_num:03d}.png"
        try:
            pix.writePNG(output)
        except Exception as err:
            print(f"Error while writing a result file ({output}): {err}")
            return


if __name__ == "__main__":
    main()


