from flask import Flask
from datetime import datetime
import re
from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
import io
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from forms import LicensePlateForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\Perry\\Downloads\\VanArtKey.json'

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
global file_name
#update to your path
file_name = os.path.abspath("C:\\Users\\Perry\\Pictures\\License Plates\\car1.jpeg")

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#update to your upload folder
UPLOAD_FOLDER = 'C:\\Users\\Perry\\Documents\\NwHacks\\hello_flask\\Uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)

class UploadForm(FlaskForm):
    file = FileField()

@app.route('/form')
def my_form():
   #return render_template('hello_there.html')
   form = LicensePlateForm()
   return render_template('form.html', title='License Plate Checker', form=form)

@app.route('/form', methods=['POST'])
def my_form_post():
    form = LicensePlateForm()
    if form.validate_on_submit():
        flash('Sumbitting for licensePlate{}'.format(
            form.licensePlate.data))
        return form.licensePlate.data
    return render_template('form.html', title='Sign In', form=form)

@app.route('/form2')
def my_form2():
   return render_template('hello_there.html')

@app.route('/form2', methods=['POST'])
def uploaded_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global file_name 
        file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
        return getData()
    return 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test')
def getData():
    DBDictionary = {"ICYA H8N" : 'false',
                    "YSJAGAN" : 'true',
                    "399 KNF" : 'false',
                    "7UIN148" : 'true',
                    "EVS ROCK": 'true',
                    "WMY-9051": 'true'
                    }

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    objects = client.object_localization(image=image)

    #print(objects)

    response = client.text_detection(image=image)

    strAll = ''
    plate = "\n"

    #print(response.text_annotations[0])

    listText = response.text_annotations[0].description.split('\n')

    print (listText)
    print (type(listText))
    for text in listText: #response.text_annotations:
        
        strAll += "License plate number is: "
        plate += text
        #print (plate[0: len(plate) - 1])
        
        #print(text)
        #print(plate)
        #print(type(plate))

        if plate[0: len(plate) - 2].strip() in DBDictionary:
            return strAll + plate + (' Plate is valid' if DBDictionary[plate[0: len(plate) - 2].strip()] == 'false' else ' Plate is invalid')
        
        if plate[0: len(plate) - 1].strip()  in DBDictionary: 
            return strAll + plate + (' Plate is valid' if DBDictionary[plate[0: len(plate) - 1].strip()] == 'false' else ' Plate is invalid')

        if plate[0: len(plate)].strip()  in DBDictionary:
            return strAll + plate + (' Plate is valid' if DBDictionary[plate[0: len(plate)].strip()] == 'false' else ' Plate is invalid')

        #if plate[len(plate.strip()) - 1] == '\n':
        plate = ''
        strAll = ''

    return 'License plate not found in database'



@app.route("/")
def home():
    return "Hello, Flask2!"
    

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )