import datetime

from flask import Flask, jsonify, render_template, request,Response
import sqlite3
import subprocess

import imutils
# face recognition
from imutils.video import VideoStream
from imutils.video import FPS
# face recognize+face encode
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2

import time # Import time
import os #this is used to create a file in our folder using os.mkdir() function
PATH_TO_TEST_IMAGES_DIR = './static/Attendance/'


conn = sqlite3.connect('FaceDatabase.db')


# Create table: registration (First Time Registration)
conn.execute('''CREATE TABLE IF NOT EXISTS registration (
id VARCHAR(15) PRIMARY KEY NOT NULL, 
businessName VARCHAR(50) NOT NULL,
email VARCHAR(30),
userName VARCHAR(15),
password VARCHAR(15),
activationKey VARCHAR(30) 
);''')

# Close database connection
conn.close()

# Flask APP - this is the flask object
app = Flask(__name__)

# START LOGIN PAGE


@app.route('/')
def home():
    return render_template('homePage.html')

@app.route('/aboutUs')
def about():
    return render_template('aboutUs.html')

@app.route('/contactUs')
def contact():
    return render_template('contactUs.html')

@app.route('/sampleContact')
def contactData():
    #  get data from user
     firstname= request.args.get('contact_firstname')
     lastname= request.args.get('contact_lastname')
     mobile= request.args.get('contact_mobile')
     email= request.args.get('contact_email')
     comment= request.args.get('contact_comment') 
     print(firstname)
     

     ret = "Success"
     try:
        #   connect to database
        conn = sqlite3.connect('FaceDatabase.db') 
        
        found=0
        # register now	  
        ret = conn.execute("INSERT into Contact ( first_Name, last_Name,mobile_Number, email,comment )     VALUES (?, ?, ?,?,?)", (firstname, lastname,mobile,email,comment))  
        conn.commit()

        # close database connection
        conn.close()

        # For debugging purpose only
        trace=1
        if trace==1:	
            print ("Contact :\n  First Name(%s)\n Last Name(%s)\n Mobile Number(%s)\n Email(%s)\n Comment(%s)\n"              %(firstname,lastname,mobile,email,comment))

        ret="Success"

     except Exception as e:
         ret = "Error"
         print("Error:",e)
     return jsonify(result=ret)



@app.route('/loginPage')
def login():
    return render_template('loginPage.html')

# @app.route("/sampleT")
# def imageT():
#     print("Inside function imageT.")
#     return render_template("attendance.html")

@app.route('/sample')
def logindata():
    #  get data from user
     login_username= request.args.get('login_username')
     login_password= request.args.get('login_password')
     login_checkbox= request.args.get('login_checkbox')
     print(login_username)

     ret = "Success"
     try:
        #   connect to database
        conn = sqlite3.connect('FaceDatabase.db') 
        # login_ids = conn.execute("SELECT id FROM login")
        found=0
        # register now	  
        ret = conn.execute("INSERT into login ( Username  ,  Password,Checkbox)     VALUES (?, ?, ?)", ( login_username, login_password,login_checkbox))  
        conn.commit()

        # close database connection
        conn.close()

        # For debugging purpose only
        trace=1
        if trace==1:	
            print ("Login :\n  Username(%s)\n Password(%s)\n Checkbox(%s)\n"     %(login_username,login_password,login_checkbox))

        ret="Success"

     except Exception as e:
         ret = "Error"
         print("Error:",e)
     return jsonify(result=ret)


@app.route('/train')
def train():
    return render_template('train.html')



@app.route('/sampleTrain')
def traindata():
    #  get data from user
     train_name= request.args.get('train_name')
     train_class= request.args.get('train_class')
     train_rollno= request.args.get('train_rollno')
     train_branch= request.args.get('train_branch')
     train_college= request.args.get('train_college') 
     train_email= request.args.get('train_email') 
     

     ret = "Success"
     try:
        #   connect to database
        conn = sqlite3.connect('FaceDatabase.db') 
        cursor = conn.cursor()
        
        found=0
        # register now	 
         
        # execute this with the help of cursor
        ret = cursor.execute("INSERT into Train ( Name, Class,Roll_No,Branch,College,Email )     VALUES (?, ?, ?,?,?,?)", (train_name, train_class,train_rollno,train_branch,train_college,train_email))  

        inserted_id = cursor.lastrowid
        # inserted_id=get_last_inserted_id()
        print(inserted_id )


        conn.commit()

        # For debugging purpose only
        trace=1
        if trace==1:	
            print ("Train :\n  Name(%s)\n Class(%s)\n Roll_No(%s)\n Branch(%s)\n College(%s)\n Email-Id(%s)\n"              %(train_name,train_class,train_rollno,train_branch,train_college,train_email))
        # path of directory

        directory_path = os.path.join('C:/Users/Simran/Desktop/Face Recognition Project/static/Attendance', str(inserted_id))
        # Parent Directories
        parent_dir = "C:/Users/Simran/Desktop/Face Recognition Project/static/Attendance"
            
        student_data = cursor.fetchone()
        # Path
        path = os.path.join(parent_dir, directory_path)

        try:
            os.makedirs(path, exist_ok = True)
            print("Directory '%s' created successfully" % directory_path)
            # Retrieve data for the student from the database

            # if not student_data:
            #     return jsonify({"message": "Student not found"}), 404

            # Save the data into a file in the created directory
            
            conn.close()

            return jsonify(inserted_id=inserted_id)


        except OSError as error:
            print("Directory '%s' can not be created" % directory_path)

        ret="Success"

     except Exception as e:
         ret = "Error"
         print("Error:",e)
     return jsonify(result=ret)



@app.route("/image",methods=['POST'])
def image():
    inserted_id = request.form.get('inserted_id')
    print(f"Inserted id obtained from myVideo is {inserted_id}")

    i = request.files['image']  # get the image
    f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    print("hello inside image function")
    
    # conn = sqlite3.connect('FaceDatabase.db') 
    # cursor = conn.cursor()
    # inserted_id = cursor.lastrowid
    # conn.commit()
    # conn.close()
    
    i.save('%s/%s' % (PATH_TO_TEST_IMAGES_DIR+str(inserted_id), f))


    return Response("%s saved" % f)



@app.route("/sampleTrainModel")
def buttonTrain():
    # Set up the paths for dataset and encodings
    dataset= "./static/Attendance/"
    encodings_path = "./static/encoding.pickle"

    command = [
        "python",  # Replace with your Python executable path if needed
        "encode_faces.py",  # Replace with the name of your script
        "-i", dataset,
        "-e", encodings_path,
        "-d", "cnn"  # Or specify the desired detection method
    ]

    try:
        subprocess.run(command, check=True)
        return "Training completed."
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

    


# to automatically create a new file with the provided Student_ID

# Python program to explain os.makedirs() method
	
# Leaf directory


@app.route('/attendance')
def attendance():
    
    return render_template('attendance.html')

@app.route("/sampleAttendance")
def attendancedata():
    # date = datetime.date.today()
    dateTime = datetime.datetime.now()
    print(dateTime)
    return "success"



@app.route("/sampleAttendanceModel")
def buttonAttendance():
    # Set up the paths for dataset and encodings
    print("hello inside button attendance model.")
    current_datetime = datetime.datetime.now()

# Define the desired date and time format using strftime
# For example: "%Y-%m-%d %H:%M:%S" for "2023-07-06 15:30:45"
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    trace=1
    try:
        if trace==1:
            print("Recognizer")
        print("[INFO] loading encodings + face detector...")
        dataset= "static/haarcascade_frontalface_default.xml"
        encodings_path = "static/encoding.pickle"
        
        data = pickle.loads(open(encodings_path,"rb").read())
        # data = pickle.loads(open(encodings_path["encodings"], "rb").read())
        detector = cv2.CascadeClassifier(dataset)

        # initialize the video stream and allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        vs = VideoStream(src=1).start()
        # vs = VideoStream(usePiCamera=True).start()
        print("hello after videostream")
        time.sleep(10.0)

        # start the FPS counter
        fps = FPS().start()

        # loop over frames from the video file stream
        while True:
            # grab the frame from the threaded video stream and resize it
            # to 500px (to speedup processing)
            print("inside while loop of button Attendance function")
            frame = vs.read()
            frame = imutils.resize(frame, width=500)
            
            # convert the input frame from (1) BGR to grayscale (for face
            # detection) and (2) from BGR to RGB (for face recognition)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # detect faces in the grayscale frame
            rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                minNeighbors=5, minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)

            # OpenCV returns bounding box coordinates in (x, y, w, h) order
            # but we need them in (top, right, bottom, left) order, so we
            # need to do a bit of reordering
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                    encoding)
                name = "Unknown"
                print("inside encoding for loop in button Attendance")

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)
                
                # update the list of names
                names.append(name)

            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top), (right, bottom),
                    (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 255, 0), 2)

            # display the image to our screen
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        ret ="Success"
        
   

    except Exception as e:
         ret = "Error"
         print("Error:",e)
    return jsonify(result=ret)

    

    

# MAIN Function starts here
if __name__ == '__main__':
	# run! Set multiple Threading to TRUE, Host to 0.0.0.0 (to access outside localhost), Port to 8080, and Dubugging to TRUE
	app.run(threaded=True, host='0.0.0.0', port=2020, debug=True)
