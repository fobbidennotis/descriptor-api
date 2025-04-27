from io import BytesIO
from typing import Dict
import cv2
import numpy as np
import easyocr
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


class Img:
    def __init__(
        self,
        processor: BlipProcessor,
        model: BlipForConditionalGeneration,
        en_reader: easyocr.Reader,
        ru_reader: easyocr.Reader,
        image_bytes,
    ) -> None:
        self.en_reader = en_reader
        self.ru_reader = ru_reader
        self.processor = processor
        self.model = model

        self.image_bytes = image_bytes

        self.ru_text = self._read_image_text(self.ru_reader)
        self.en_text = self._read_image_text(self.en_reader)
        self.caption = self._captionize_image()

    def __preprocess_image(self) -> np.ndarray:
        img = cv2.imdecode(np.frombuffer(self.image_bytes, np.uint8), cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
        img_masked = cv2.bitwise_and(img, img, mask=thresh)

        return img_masked

    def _read_image_text(self, reader: easyocr.Reader) -> str:
        img_array = self.__preprocess_image()
        pil_img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
        result = reader.readtext(np.array(pil_img))

        return " ".join(item[1] for item in result)

    def _captionize_image(self) -> str:
        image = Image.open(BytesIO(self.image_bytes)).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs, max_length=100, num_beams=5, early_stopping=True
            )

        return self.processor.decode(output_ids[0], skip_special_tokens=True)

    async def describe_image(self) -> Dict[str, str]:
        return {
            "ru_text": self.ru_text,
            "en_text": self.en_text,
            "caption": self.caption,
        }
