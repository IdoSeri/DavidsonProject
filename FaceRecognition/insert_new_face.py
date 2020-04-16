# import the necessary packages
import imutils
from imutils.video import VideoStream
import time
from imutils import paths
import face_recognition
import pickle
import cv2
import os
import shutil

# create the folder in the dataset
mypath = "FaceRecognition/dataset/"+input("Enter the new face's name: ")
print("[INFO] creating a new folder...")
if not os.path.isdir(mypath):
	os.makedirs(mypath)

# load OpenCV's Haar cascade for face detection from disk
detector = cv2.CascadeClassifier("FaceRecognition/haarcascade_frontalface_default.xml")

# initialize the video stream, allow the camera sensor to warm up,
# and initialize the total number of example faces written to disk
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
total = 0

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, clone it, (just
	# in case we want to write it to disk), and then resize the frame
	# so we can apply face detection faster
	frame = vs.read()
	orig = frame.copy()
	frame = imutils.resize(frame, width=400)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30))

	# loop over the face detections and draw them on the frame
	for (x, y, w, h) in rects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `k` key was pressed, write the *original* frame to disk
	# so we can later process it and use it for face recognition
	if key == ord("k"):
		p = os.path.sep.join([mypath, "{}.png".format(
			str(total).zfill(5))])
		cv2.imwrite(p, orig)
		total += 1

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# cleanup
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()


### encode the face into the disk: ###

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images("FaceRecognition/dataset"))

knownEncodings= []
knownNames= []

# load the known faces and embeddings from the exists disk
filepath= "FaceRecognition/encodings.pickle"
if os.path.isfile(filepath):
	data = pickle.loads(open(filepath, "rb").read())
	knownEncodings= data["encodings"]
	knownNames= data["names"]
	# remove the exists disk
	os.remove(filepath)

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	
	# load the input image and convert it from BGR (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb, model="cnn")
	
	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)
	
	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to new disk
print("[INFO] serializing encodings...")
data1 = {"encodings": knownEncodings, "names": knownNames}
f = open("FaceRecognition/encodings.pickle", "wb")
f.write(pickle.dumps(data1))
f.close()

if os.path.isdir(mypath):
	shutil.rmtree(mypath)

print("---------------------------------------")
print("[INFO] your face has entered the system!")