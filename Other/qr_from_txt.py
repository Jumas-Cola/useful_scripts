import qrcode
import os
from PyPDF2 import PdfFileMerger
import shutil
from PIL import ImageDraw
import sys


def file_reader(filename):
    res = ''
    with open(filename) as f:
        for line in f:
            for sign in line:
                res += sign
                if sys.getsizeof(res) >= 1000:
                    yield res
                    res = ''
        yield res


filename = 'Portret_Doriana_Greya.txt'

current_dir = os.path.dirname(os.path.abspath(__file__))
data_list = file_reader(os.path.join(current_dir, filename))
pdf_dir = os.path.join(current_dir, 'pdf_qr')
if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

for n, data_item in enumerate(data_list):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_item)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), str(n + 1))
    img.save(os.path.join(pdf_dir, '{}.pdf'.format(n + 1)), 'PDF')

pdfs = sorted(os.listdir(pdf_dir), key=lambda x: int(
    os.path.splitext(os.path.basename(x))[0]))
merger = PdfFileMerger()
for pdf in pdfs:
    merger.append(os.path.join(pdf_dir, pdf))
merger.write(os.path.join(current_dir, os.path.splitext(filename)[0] + '.pdf'))
merger.close()

shutil.rmtree(pdf_dir)
