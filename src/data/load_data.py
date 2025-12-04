# lololololol

import os
import torch
import matplotlib.pyplot as plt
from io import BytesIO
from pathlib import Path
ROOT = Path(os.getcwd()).parents[0]

from ..final_model.features_extractor import get_logits
from ..final_model.caption_generator import load_caption_model, get_caption
from ..final_model.retriever import CaptionRetriever

checkpoint_path = f"{ROOT}\\RoboCap\\results\\checkpoints\\bert-best-acc-epoch=08-val_acc=0.6972.ckpt"
caption_embeddings_path = f"{ROOT}\\RoboCap\\raw_data\\pt_files\\caption_cache_train.pt"
path_captions_train = f"{ROOT}\\RoboCap\\raw_data\\annotations\\captions_train2017.json"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def Robocap(img_bytes):
    logits = get_logits(img_bytes)
    print(logits)
    caption_retriever = load_caption_model(checkpoint_path, caption_embeddings_path, path_captions_train, device)
    caption = get_caption(logits, caption_retriever)

    return caption

image = open("raw_data\\images\\test2017\\000000478760.jpg", "rb")
img_bytes = image.read()
# print(img_bytes)

cap = Robocap(img_bytes)

print("Generated Caption:", cap)