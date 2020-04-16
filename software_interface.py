from sqlLiteCode.sqlite_table import *
from qrBarcodeDetection.item_func import *
from FaceRecognition.recognize_specific_face_def import *
from pyzbar import pyzbar
import imutils
import cv2
import sqlite3

key =''
while key!='q':
	print(" --------------------------------")
	print("| HOMEPAGE:                      |")
	print("| 1) for a new client:   press n |")
	print("| 2) to show the table:  press s |")
	print("| 2) to clear the table: press d |")
	print("| 3) to quit the system: press q |")
	print(" --------------------------------")
	key= input("press: ")
	
	if key == 'n':
		
		while key!='h':
			
			print("[INFO] Recognizing The Face...")
			name1= recognize_face()
			print("[INFO] " + name1 + " recognized!")
			
			while key!='h':
				
				print(" ---------------------------------")
				print("| INSTRUCTIONS:                     |")
				print("| 1) back to homepage:      press h |")
				print("| 2) for insert equipment:  press i |")
				print("| 3) for delete equipment:  press d |")
				print("| 4) check if all returned: press c |")
				print(" ---------------------------------")
				
				key= input("press: ")
				
				if key == 'i':
					item= item_name_qrcode()
					print("[INFO] inserting to table: " + name1 + " took a " + item)
					insert(name1,item)
					print("[INFO] inserted!")
				
				if key == 'd':
					item= item_name_qrcode()
					print("[INFO] deleting from table: " + name1 + " returned a " + item)
					delete(name1,item)
					print("[INFO] item deleted!")

				if key == 'c':
					
					if check(name1)==True:
						print(name1 + " returned everything")
					else:
						print(name1 + " didnt return everything")
						print("items that left to return:")
						items_left(name1)
	
	if key == 's':
		print_table()

	if key == 'd':
		print("[INFO] Clearing The Table...")
		delete_all()

print("[INFO] Disconnecting The System...")