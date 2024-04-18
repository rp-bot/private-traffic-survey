import torch
from PIL import Image
import numpy as np
import sys

from network import modeling
from datasets.cityscapes import Cityscapes

import torch.nn.functional as F
from torchvision import transforms

# Define paths and parameters
MODEL_PATH = r"C:\Users\Jay\Desktop\CSCI 495 Capstone\best_deeplabv3plus_mobilenet_cityscapes_os16.pth"
IMAGE_PATH = r"C:\Users\Jay\Desktop\CSCI 495 Capstone\testImage.jpg"
NUM_CLASSES = 19
OUTPUT_STRIDE = 16

def segment_and_overlay(image_path):
    """
    Segments an intersection image and overlays the segmentation on the original image.

    Args:
        image_path: Path to the input image.

    Returns:
        A PIL Image object with the segmentation overlay.
    """
    # Load the model
    model = modeling.__dict__["deeplabv3plus_mobilenet"](num_classes=NUM_CLASSES, output_stride=OUTPUT_STRIDE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu'))["model_state"])
    model.eval()

    # Open the image and convert it to a tensor
    image = Image.open(image_path).convert("RGB")
    image_tensor = transforms.ToTensor()(image).unsqueeze(0)

    # Segment the image
    with torch.no_grad():
        outputs = model(image_tensor)
    
    # Get the predicted segmentation map
    pred = outputs.argmax(dim=1).squeeze().cpu().numpy()

    # Colorize the segmentation
    colorized_preds = Cityscapes.decode_target(pred).astype('uint8')
    colorized_preds = Image.fromarray(colorized_preds)

    # Resize the colorized segmentation to match the original image size
    colorized_preds = colorized_preds.resize(image.size, resample=Image.BILINEAR)

    # Create an overlayed image with an opaque segmentation
    overlayed_image = Image.blend(image, colorized_preds, 0.5)

    return overlayed_image


# Run the segmentation and overlay
segmented_image = segment_and_overlay(IMAGE_PATH)

# Save or display the result as needed
segmented_image.save("segmented_intersection.png")
segmented_image.show()