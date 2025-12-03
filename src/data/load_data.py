# lololololol

from ..final_model.features_extractor import get_logits
from ..final_model.caption_generator import get_caption

def Robocap(img_bytes):

    logits = get_logits(img_bytes)
    print(logits)
    # caption = get_caption(logits)

    # return caption


image = open("raw_data\\images\\test2017\\000000000001.jpg", "rb")
img_bytes = image.read()
# print(img_bytes)

Robocap(img_bytes)
