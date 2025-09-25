import cv2
import pytesseract
import os
import logging
from helpers.config import get_settings
import numpy as np

logger = logging.getLogger(__name__)

class Pytesseract:

    def __init__(self):

        self.settings = get_settings()
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        logger.info(f"Using Tesseract OCR Engine at: {self.settings.PATH_TO_OCR_ENGINE}")
        self.config = r'--psm 6'


    def read_image(self, image_bytes: bytes) -> str:

        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            logger.error("Failed to decode image from bytes")
            raise ValueError("Failed to decode image from bytes")
        
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        adaptive_thresh = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 67, 7
        )


        text = pytesseract.image_to_string(adaptive_thresh,lang="ara")
        logger.info(f"Extracted Text: {text}")

        cv2.imshow("OCR Input - Grayscale", adaptive_thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return text