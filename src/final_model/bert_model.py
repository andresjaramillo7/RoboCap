import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
from transformers import BertModel, BertConfig

class ImageToBertModel(nn.Module):
    """Model that projects image logits through BERT to generate embeddings."""
    
    def __init__(self, image_logit_dim: int, bert_hidden_size: int = 768, dropout: float = 0.1):
        super().__init__()
        
        # Projects input image features to match BERT's hidden size
        self.image_projection = nn.Sequential(
            nn.Linear(image_logit_dim, bert_hidden_size),
            nn.LayerNorm(bert_hidden_size),
            nn.Dropout(dropout)
        )
        
        # Load pre-trained BERT model
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        
        # Final layer to smooth and map output embeddings
        self.output_projection = nn.Sequential(
            nn.Linear(bert_hidden_size, bert_hidden_size),
            nn.Tanh()
        )
        
        self.bert_hidden_size = bert_hidden_size
    
    def forward(self, image_logits: torch.Tensor) -> torch.Tensor:
        """
        Args:
            image_logits: (batch_size, image_logit_dim)
        Returns:
            embeddings: (batch_size, bert_hidden_size)
        """
        batch_size = image_logits.size(0)
        
        # Map inputs to BERT dimension: (Batch, Hidden)
        projected = self.image_projection(image_logits)
        
        # Add sequence dimension for BERT: (Batch, 1, Hidden)
        inputs_embeds = projected.unsqueeze(1)
        
        # Create attention mask (all ones) for the single token
        attention_mask = torch.ones(batch_size, 1, device=image_logits.device)
        
        # Pass inputs through BERT
        bert_output = self.bert(
            inputs_embeds=inputs_embeds,
            attention_mask=attention_mask
        )
        
        # Extract the state of the first token (Batch, Hidden)
        cls_embedding = bert_output.last_hidden_state[:, 0, :]
        
        # Apply final projection
        output_embedding = self.output_projection(cls_embedding)
        
        return output_embedding

class BertImageTrainer(L.LightningModule):
    """Lightning module for training BERT with image logits using Contrastive Loss."""
    
    def __init__(self, image_logit_dim: int, bert_hidden_size: int = 768, learning_rate: float = 2e-5, temperature: float = 10.0):
        super().__init__()
        self.save_hyperparameters()
        
        # Initialize model
        self.model = ImageToBertModel(image_logit_dim=image_logit_dim, bert_hidden_size=bert_hidden_size)
        
        # Learning rate
        self.learning_rate = learning_rate
        
        # Temperature (Scaling factor): 
        self.temperature = temperature
    
    def forward(self, image_logits: torch.Tensor) -> torch.Tensor:
        return self.model(image_logits)
    
    # Helper function to compute contrastive loss
    def compute_contrastive_loss(self, img_emb, txt_emb):
        # Normalize embeddings
        img_emb = F.normalize(img_emb, p=2, dim=1)
        txt_emb = F.normalize(txt_emb, p=2, dim=1)
        
        # Multiply image embeddings with text embeddings transpose
        logits = torch.matmul(img_emb, txt_emb.T) * self.temperature
        
        # Creates labels matching indices
        labels = torch.arange(logits.size(0), device=self.device)
        
        # Calculate Cross Entropy
        loss = F.cross_entropy(logits, labels)
        
        return loss, logits

    def training_step(self, batch, batch_idx):
        image_logits = batch['image_logits']
        target_embeddings = batch['target_embedding']
        
        # Forward pass
        predicted_embeddings = self(image_logits)
        
        # Calculate Loss
        loss, logits = self.compute_contrastive_loss(predicted_embeddings, target_embeddings)
        
        # Monitor Accuracy
        labels = torch.arange(logits.size(0), device=self.device)
        acc = (logits.argmax(dim=1) == labels).float().mean()
        
        # Logging
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        image_logits = batch['image_logits']
        target_embeddings = batch['target_embedding']
        
        # Forward pass
        predicted_embeddings = self(image_logits)
        
        # Calculate Loss
        loss, logits = self.compute_contrastive_loss(predicted_embeddings, target_embeddings)
        
        # Monitor Accuracy
        labels = torch.arange(logits.size(0), device=self.device)
        acc = (logits.argmax(dim=1) == labels).float().mean()

        # Logging
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)
        
        return loss
    
    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.learning_rate)