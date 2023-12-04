import cv2
import easyocr
from googletrans import Translator

# easyocr 독일어(de)로 설정
reader = easyocr.Reader(['de'])

# 구글 번역 라이브러리
translator = Translator()

# 웹캠 연동 cap-> cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)

# 프레임 설정 : 60
desired_fps = 60
cap.set(cv2.CAP_PROP_FPS, desired_fps)

while True: # 루프 -> 프레임
    # 웹캠에서 프레임을 읽습니다. read함수는 성공적으로 프레임을 읽었는지를 나타내는 bool값 ret과 읽은 프레임 frame을 반환합니다.
    ret, frame = cap.read()
    if not ret: # 만약 프레임 읽기가 실패하면 루프를 종료합니다.
        break

    # easyocr을 사용하여 이미지에서 텍스트를 추출합니다.
    result = reader.readtext(frame)

    # 추출된 텍스트가 있을 때만 독일어로 판단하고 번역합니다.
    if result:
        detected_text = result[0][1]  # 첫 번째로 감지된 텍스트만 사용합니다. 이는 단순히 코드를 간단하게 유지하기 위한 것입니다.

        # 번역된 텍스트를 화면에 출력합니다.
        print("Detected Text (German):", detected_text)


    # 웹캠 비디오 창에 프레임을 표시합니다. 실시간으로 어떤 이미지를 캡처하고 있는지 확인할 수 있게 해줍니다.
    cv2.imshow('WebCam', frame)

    # 'q' 키를 누르면 루프에서 빠져나옵니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠을 닫습니다.
cap.release()
cv2.destroyAllWindows() # 모든 opencv창을 닫습니다.
