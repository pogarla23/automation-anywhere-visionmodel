from flask import Flask, render_template, request

app = Flask(__name__)

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
    
    #load model
    #pending!
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)