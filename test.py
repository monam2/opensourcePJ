import cv2
import easyocr
from googletrans import Translator

reader = easyocr.Reader(['de'])
translator = Translator()
cap = cv2.VideoCapture(0)
desired_fps = 60
cap.set(cv2.CAP_PROP_FPS, desired_fps)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = reader.readtext(frame)

    if result:
        detected_text = result[0][1]
        translated_text = translator.translate(detected_text, src='de', dest='ko').text

        print("Detected Text (German):", detected_text)
        print("Translated Text (Korean):", translated_text)

    cv2.imshow('WebCam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
