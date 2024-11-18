from flask import Flask, render_template, request

#render_template: renders HTML files for display on web browser
#request: object that contains all data sent from client to the server
# import torch
# from torchvision import transforms
# from PIL import Image
# import matplotlib.pyplot as plt
# import os
# from io import BytesIO

app = Flask(__name__)#this initializes flask app

#loading our trained model:
#device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
# model = torch.load('/content/trained_model.pth')  
# model.to(device) 
# model.eval()  

#returns the template of main page (index.html)
@app.route('/')
def hello_world():
    return render_template('index.html')

#allows user to upload an image
@app.route('/', methods=['POST'])
def predict():
    #takes in image input
    imagefile = request.files['imagefile']
    #saves it
    image_path = "./images" + imagefile.filename
    imagefile.save(image_path)
    #for production: add aditional checks for input validation (only images allowed)
    
    
    #matplotlib screenshot. plt library (screenshots image that is extracted with annotations)-->passed through function to display
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)