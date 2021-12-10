from flask import *
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
from keras.layers.core import Dense,Flatten
from keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import os  
from PIL import Image
import cv2
from tensorflow.keras.models import load_model
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
# class_names = ["Card", "NoCard"]
class_names = ["Freekick", "Cards", "Center", "Corner", "Tackle", "Subs", "Pens"]

client = MongoClient("mongodb+srv://<username>:<password>@cluster0.utu0m.mongodb.net/<dbName>?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority")
collection = db["overall-model"]
# print(collection.find_one())

time_stamps = []

def get_model():
    global model
    model = load_model('new_model_overall_1500.h5')
    print("Model loaded!")

get_model()

def predict_video(filename):
    count = 0
    img_height,img_width=64,64
    test_video_file = 'D:/FootballDetection/{}.mp4'.format(filename)
    #test_video_file = filename
    cap = cv2.VideoCapture("D:/FootballDetection/cards-corners.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))    
    print(fps)
    while (cap.isOpened()):
        frame_exists, frame = cap.read()
        if frame_exists == False:
            break
        if frame_exists:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            image_resized= cv2.resize(frame, (img_height,img_width))
            image=np.expand_dims(image_resized,axis=0)
            pred=model.predict(image)
            print(pred)
            s = class_names[np.argmax(pred)]
            if(s == "Cards" or s == "Corner"):
                framec = cap.get(cv2.CAP_PROP_POS_FRAMES)
                time_stamp = {"id": s, "frame": framec, "timestamp": timestamp}
                time_stamps.append(time_stamp)
    #         if(pred[0][0] > 0.9):
    #             framec = cap.get(cv2.CAP_PROP_POS_FRAMES);
    #             print("{}, {}".format(framec, timestamp))
    #             time_stamp = {"id": 2, "frame": framec, "timestamp": timestamp}
    #             time_stamps.append(time_stamp) 
    #             # count+=framec+fps/2
    #             # cap.set(cv2.CAP_PROP_POS_FRAMES, count)
    #             # cv2.imwrite('D:/FootballDetection/Vid2-Model3/{}.jpg'.format(framec), frame)
    # result = collection.insert_many(time_stamps)
    # print(result)
    cap.release()
    cv2.destroyAllWindows() 

# predict_video("cards-corners.mp4")

# img_height,img_width=64,64
# image=cv2.imread("D:/FootballDetection/Vid1-Model3/1576.0.jpg")
# image_resized= cv2.resize(image, (img_height,img_width))
# image=np.expand_dims(image_resized,axis=0)
# print(image.shape)

# pred=model.predict(image)
# print(pred)
# print(class_names[np.argmax(pred)])

# @app.route('/uploads/<output_class>')
# def download_file(output_class):
#   return render_template('index.html', output_class=output_class)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
          # print(file.filename)
          # s = "drive/MyDrive/Train/NonCorner/{}".format(file.filename)
          # image=cv2.imread(str(s))       
        #   image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)   
        #   print(image)
        #   image_resized= cv2.resize(image, (180,180))
        #   image=np.expand_dims(image_resized,axis=0)
        #   pred=model.predict(image)
        #   output_class=class_names[np.argmax(pred)]
          file.save("D:/FootballDetection/{}.mp4".format(file.filename))
          predict_video(file.filename)
          return redirect(url_for('download_file', output_class="corner"))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/corners')
def get_corners():
    prev = 0
    time_stamps=[]
    corners = "Corner"
    for frame in collection.find({"id": corners}):
        if(frame["timestamp"]/1000 - prev > 1):
            time_stamps.append(frame["timestamp"]/1000)
            prev = frame["timestamp"]/1000
    final_ret = {"timestamps": time_stamps}
    return final_ret

@app.route('/cards')
def get_cards():
    prev = 0
    time_stamps=[]
    cards = "Cards"
    for frame in collection.find({"id": cards}):
        if(frame["timestamp"]/1000 - prev > 1):
            if(frame["timestamp"]/1000 > 44):
                break
            time_stamps.append(frame["timestamp"]/1000)
            prev = frame["timestamp"]/1000
    final_ret = {"timestamps": time_stamps}
    return final_ret




# @app.route('/')
# def return_json():
#    final_ret = {"status": "Success", "message": "Helloe world!"}
#    return final_ret


# length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# print( length )



app.run()
