# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import cv2

def recognize_face():

	# load the known faces and embeddings
	data = pickle.loads(open("FaceRecognition/encodings.pickle", "rb").read())

	# initialize the video stream
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

	name =""

	# loop over frames from the video file stream
	while name=="":

		# grab the frame from the threaded video stream
		frame = vs.read()
		
		# convert the input frame from BGR to RGB then resize it to have
		# a width of 750px (to speedup processing)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		rgb = imutils.resize(frame, width=750)
		r = frame.shape[1] / float(rgb.shape[1])

		# detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the frame
		boxes= face_recognition.face_locations(rgb, model="cnn")
		# compute the facial embeddings for each face
		encodings = face_recognition.face_encodings(rgb, boxes)
		

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known encodings
			matches = face_recognition.compare_faces(data["encodings"], encoding)

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
			
		
	# cleanup
	cv2.destroyAllWindows()
	vs.stop()
	# send the recognized name
	return name