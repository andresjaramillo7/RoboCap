import torch
import torch.nn.functional as F
from typing import List, Tuple, Dict

class CaptionRetriever:
    """Retrieve captions for images using trained BERT model and Cosine Similarity."""
    
    def __init__(
        self,
        model,
        caption_embeddings_dict: Dict[str, torch.Tensor],
        captions_dict: Dict[str, List[str]],
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        self.model = model.to(device)
        self.model.eval()
        self.model.float() 
        
        self.device = device
        
        self.all_captions = []
        self.all_filenames = []
        embeddings_list = []
        
        print("Building caption database...")
        for filename, embeds in caption_embeddings_dict.items():
            if filename not in captions_dict:
                continue
            
            captions = captions_dict[filename]
            num_captions = min(embeds.size(0), len(captions))
            
            for i in range(num_captions):
                embeddings_list.append(embeds[i])
                self.all_captions.append(captions[i])
                self.all_filenames.append(filename)
        
        # Stack all embeddings
        self.all_embeddings = torch.stack(embeddings_list).to(device)
        self.all_embeddings = self.all_embeddings.float()
        
        # Normalize
        self.all_embeddings = F.normalize(self.all_embeddings, p=2, dim=1)
        
        print(f"Database ready: {len(self.all_captions)} captions loaded.")
    
    def retrieve_caption(
        self, 
        image_logits: torch.Tensor, 
        k: int = 1
    ) -> List[Tuple[str, float]]:
        
        with torch.no_grad():
            if image_logits.dim() == 1:
                image_logits = image_logits.unsqueeze(0)
            
            image_logits = image_logits.to(self.device).float()
            
            # Get embedding
            image_embedding = self.model(image_logits)
            image_embedding = F.normalize(image_embedding, p=2, dim=1)
            
            # Calculate Scores
            scores = torch.matmul(image_embedding, self.all_embeddings.T).squeeze(0)
            
            # Get Top-K
            top_k_values, top_k_indices = torch.topk(scores, k=min(k, len(scores)))
            
            results = []
            for idx, score in zip(top_k_indices.cpu(), top_k_values.cpu()):
                results.append((self.all_captions[idx], float(score)))
            
            return results