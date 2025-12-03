# Convolutional Network (Resnet101) Feature Extractor

# Imports
from io import BytesIO
from PIL import Image

import torch
import torch.nn as nn
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
import torchvision.models as models
import torchvision.transforms as T

import lightning as L

# Model Structure (Methods)
class RoboCapFeatureExtractor(L.LightningModule):

    def __init__(self, backbone):
        super().__init__()
        self.backbone = backbone

        # Ya que solo se usa para 'feature extracting'; congelamos los pesos
        for param in self.backbone.parameters():
            param.requires_grad = False

    def forward(self, x):
        # Vector de features extraídas
        features = self.backbone(x)
        return features

    def predict_step(self, batch, batch_idx):
        images = batch
        with torch.no_grad():
            feats = self(images)
        return feats


# Function to initialize model architecture
def get_model_architecture():
    # Import ResNet101 pre-trained
    resnet101_model = models.resnet101(weights = models.ResNet101_Weights.IMAGENET1K_V1)

    # Obtain number of input features of the last layer (fc)
    in_features = resnet101_model.fc.in_features

    # Replace last layer (classifier) with a new layer (Identity) to get Logits
    resnet101_model.fc = nn.Identity()

    # Create model object
    feature_extractor = RoboCapFeatureExtractor(backbone = resnet101_model)

    # Transforms
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        # transforms.RandomCrop((128, 128)),
        transforms.RandomHorizontalFlip(p = 0.5),
        transforms.RandomRotation(10),
        # transforms.ColorJitter(brightness = 0.1, contrast = 0.1, saturation = 0.1, hue = 0.1),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])

    return feature_extractor, transform

# Main function to get logits from image bytes with the model
def get_logits(img_bytes):

    # Use GPU if its available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print(f"Using device: {device}")

    model, transform = get_model_architecture()

    # Preprocess image
    image = Image.open(BytesIO(img_bytes)).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)
    image = image.to(device)

    # Evaluation mode
    model.eval()
    # Run in device
    model.to(device)

    # Logits vector storage
    logits = []

    # Sin gradiente
    with torch.no_grad():
        logits = model(image).cpu() # (1, in_features)
    
    return logits
