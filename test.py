import cv2
import easyocr
from googletrans import Translator

# easyocr 독일어(de)로 설정
reader = easyocr.Reader(['de'])

# 구글 trans 선언 및 초기화
translator = Translator()

# 웹캠 연동 cap-> cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)

# 프레임 설정 : 60
desired_fps = 60
cap.set(cv2.CAP_PROP_FPS, desired_fps)

while True: # 루프 -> 프레임 단위
    # 웹캠에서 프레임을 읽습니다. read함수는 성공적으로 프레임을 읽었는지를 나타내는 bool값 ret과 읽은 프레임 frame을 반환
    # 프레임이 정상 로드 -> ret : True, frame : 단위 프레임
    ret, frame = cap.read()
    if not ret: # 프레임x -> 루프를 종료
        break

    # easyocr 텍스트 추출(
    result = reader.readtext(frame)

    # 텍스트가 있으면 독일어 문자열로 받아와 출력
    if result:
        detected_text = result[0][1]
        print("Detected Text (German):", detected_text)


    # 실시간 웹캠 영상 출력(프레임 단위)
    cv2.imshow('WebCam', frame)

    # 'q' 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
