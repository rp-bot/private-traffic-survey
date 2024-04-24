import os
import torch
from PIL import Image, ImageFilter, ImageOps
from torchvision import transforms
import numpy as np

from NN.network import modeling
from NN.datasets.cityscapes import Cityscapes

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths and parameters relative to the script directory
MODEL_PATH = os.path.join(SCRIPT_DIR, "Model", "best_deeplabv3plus_mobilenet_cityscapes_os16.pth")
IMAGE_PATH = os.path.join(SCRIPT_DIR, "Input", "testImage3.jpg")
NUM_CLASSES = 19
OUTPUT_STRIDE = 16

def segment_and_overlay(image_path):
    # Load the model
    model = modeling.__dict__["deeplabv3plus_mobilenet"](num_classes=NUM_CLASSES, output_stride=OUTPUT_STRIDE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu'))["model_state"])
    model.eval()

    # Open the image and convert it to a tensor
    imageTemp = Image.open(image_path).convert("RGB")
    image = ImageOps.exif_transpose(imageTemp)
    image_tensor = transforms.ToTensor()(image).unsqueeze(0)

    # Segment the image
    with torch.no_grad():
        outputs = model(image_tensor)
    
    # Get the predicted segmentation map
    pred = outputs.argmax(dim=1).squeeze().cpu().numpy()

    # Decoding the segmentation map to colorized image
    colorized_preds = Cityscapes.decode_target(pred).astype('uint8')
    colorized_preds = Image.fromarray(colorized_preds)

    # Resize colorized image to match original image size
    colorized_preds = colorized_preds.resize(image.size, resample=Image.BILINEAR)

    # Overlay colorized image over original image
    overlayed_image = Image.blend(image, colorized_preds, 0.5)

    # Convert colorized image to numpy array
    colorized_array = np.array(colorized_preds)

    # Define the limited colors
    limited_colors = [[0, 0, 142],[244, 35, 232], [128, 64, 128], [250, 170, 30], [220, 220, 0]]

    # Initialize an empty array to store the limited image
    limited_array = np.zeros_like(colorized_array)

    # Iterate over each pixel in the colorized array
    for i in range(colorized_array.shape[0]):
        for j in range(colorized_array.shape[1]):
            # Check if the pixel color matches any of the specified colors
            if np.any(np.all(colorized_array[i, j] == limited_colors, axis=1)):
                limited_array[i, j] = colorized_array[i, j]
            else:
                limited_array[i, j] = [0, 0, 0]  # Set pixel to black

    # Convert limited array back to PIL image
    limited_image = Image.fromarray(limited_array)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=20))  # Adjust radius as needed

    # Create a mask from the limited image (black pixels = 0, others = 255)
    mask = limited_image.convert('L').point(lambda x: 255 if x > 0 else 0)

    # Apply the mask to the blurred image
    blurred_image.paste(image, mask=mask)

    return overlayed_image, colorized_preds, blurred_image
# Run the segmentation and overlay
overlayed_image, masked_image, blurred_image = segment_and_overlay(IMAGE_PATH)

# Save or display the results
output_path_overlay = os.path.join(SCRIPT_DIR, "Output", "segmented_intersection.png")
output_path_masked = os.path.join(SCRIPT_DIR, "Output", "masked_intersection.png")
output_path_blurred = os.path.join(SCRIPT_DIR, "Output", "blurred_intersection.png")

overlayed_image.save(output_path_overlay)
masked_image.save(output_path_masked)
blurred_image.save(output_path_blurred)


overlayed_image.show()
masked_image.show()
blurred_image.show()
