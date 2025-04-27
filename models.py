import easyocr
from transformers import BlipProcessor, BlipForConditionalGeneration


PROCESSOR = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
MODEL = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# decided to go for 2 separate description in both languages
READER_RU = easyocr.Reader(["ru"])
READER_EN = easyocr.Reader(["en"])
