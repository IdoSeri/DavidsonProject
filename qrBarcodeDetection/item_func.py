from pyzbar import pyzbar
import imutils
import cv2


def item_name_qrcode():
	cap = cv2.VideoCapture(0)
	barcodeData = ""
	while barcodeData == "":
	
		ret, frame = cap.read()
		frame = imutils.resize(frame, width=400)
		barcodes = pyzbar.decode(frame)
		# loop over the detected barcodes
		for barcode in barcodes:
			
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
			if barcodeType is not "QRCODE":
				break
			
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		
		cv2.imshow("Barcode Scanner", frame)
	
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cap.release()
	cv2.destroyAllWindows()
	return barcodeData