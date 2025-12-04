# Transformer (BERT mamado) Caption Generator
import torch
from .bert_model import BertImageTrainer
from .retriever import CaptionRetriever
from ..data.captions_loader import load_and_clean_captions
from typing import Tuple


def load_caption_model(checkpoint_path: str, caption_embeddings_path: str, captions_path: str, device: str = None) -> CaptionRetriever:
    """
    Load model and create retriever.
    
    Args:
        checkpoint_path: Path to trained model checkpoint
        caption_embeddings_path: Path to caption embeddings .pt
        captions_path: Path to captions dict .pt
        device: 'cuda' or 'cpu'
    
    Returns:
        CaptionRetriever ready to use
    """
    print("Loading model...")
    model = BertImageTrainer.load_from_checkpoint(checkpoint_path)
    
    print("Loading caption data...")
    caption_embeddings_raw = torch.load(caption_embeddings_path)
    caption_embeddings = caption_embeddings_raw["embeddings_by_file"]
    captions = load_and_clean_captions(captions_path)
    
    print("Creating retriever...")
    retriever = CaptionRetriever(
        model=model,
        caption_embeddings_dict=caption_embeddings,
        captions_dict=captions,
        device=device
    )
    
    print("Ready for inference!\n")
    return retriever



def get_caption(image_logits: torch.Tensor, retriever: CaptionRetriever) -> str:
    """
    Get caption for an image.
    
    Args:
        image_logits: Image features tensor (2048,)
        retriever: CaptionRetriever instance
    
    Returns:
        Caption string
    """
    # Get top caption
    results = retriever.retrieve_caption(image_logits, k=1)

    # Unpack the first tuple from the list
    best_caption, score = results[0]
    
    return best_caption