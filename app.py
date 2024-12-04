import os
import random
import matplotlib.pyplot as plt
import torchvision.transforms as T
from PIL import Image
import torch
import torch.nn as nn
import torchvision
import streamlit as st
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

def load_image(image_path):
    img = Image.open(image_path)  
    transform = T.Compose([
        T.ToTensor(),
    ])
    img = transform(img)  
    return img

def show_image_with_boxes(image, boxes, scores):
    img = image.permute(1, 2, 0).cpu().numpy()  
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(img)

    for i, box in enumerate(boxes):
        ax.add_patch(plt.Rectangle(
            (box[0], box[1]), box[2] - box[0], box[3] - box[1],
            fill=False, edgecolor='red', linewidth=2
        ))
        ax.text(box[0], box[1] - 10, f"{scores[i]:.2f}", color='yellow', fontsize=15,
                bbox=dict(facecolor='black', alpha=.75))

    ax.axis('off')
    st.pyplot(fig)

st.title("Signature Detection")
st.sidebar.header("Settings")

confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.5, 1.0, 0.92)

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)

    num_classes = 2  
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    model.load_state_dict(torch.load('trained_model (2).pth', map_location=device))
    model.to(device)
    model.eval()

    image = load_image(uploaded_file)
    image = image.to(device)
    image = image.unsqueeze(0)  

    with torch.no_grad(): 
        predictions = model(image)

    boxes = predictions[0]['boxes'].cpu().numpy()
    scores = predictions[0]['scores'].cpu().numpy()

    filtered_boxes = boxes[scores >= confidence_threshold]
    filtered_scores = scores[scores >= confidence_threshold]

    if len(filtered_boxes) == 0:
        st.write("No bounding boxes above the confidence threshold!")
    else:
        show_image_with_boxes(image.squeeze(0), filtered_boxes, filtered_scores)
