# Transformer (BERT mamado) Caption Generator

def get_caption(logits = None):
    print("Generating caption... (dummy function)")
    return None



# Imports
import torch

# Use GPU if its available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")

