import sys

from pyzbar.pyzbar import decode
import cv2
import numpy as np
import webbrowser

scanned_codes = []

def _decode(frame):
    if frame is not None:
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            if barcode_data:
                if ( barcode_data.startswith("http://") or barcode_data.startswith("https://") ) and barcode_data not in scanned_codes:
                    scanned_codes.append(barcode_data)
                    webbrowser.open(barcode_data)
                else:
                    print(barcode_data)
