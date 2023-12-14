import cv2
import os
import easyocr
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from googletrans import Translator
from gtts import gTTS
import pygame

def play_mp3_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

def synthesize_and_play_text(text, lang='ko'):
    # 번역된 텍스트를 음성으로 변환
    tts = gTTS(text=text, lang=lang)

    # 음성을 MP3 파일로 저장
    tts.save('output.mp3')

    play_mp3_file('output.mp3')

reader = easyocr.Reader(['de'])
translator = Translator()
cap = cv2.VideoCapture(0)

ocr_result = ''  # 초기화를 반복문 밖으로 이동
trans_result = ''
font = ImageFont.truetype('./LINESeedKR-Rg.ttf', 30)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    result_frame = frame.copy()

    if ocr_result:
        cv2.putText(result_frame, 'German : ' + ocr_result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        korean_text = 'Korean : ' + trans_result

        img_pil = Image.fromarray(result_frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text((10, 70), korean_text, font=font, fill=(255, 0, 0))
        result_frame = np.array(img_pil)
    
    cv2.imshow('WebCam', result_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        # 스페이스바를 누르면 현재 프레임을 저장하고 바로 삭제
        cv2.imwrite('captured_frame.png', frame)
        print("Frame captured and saved!")
        key = cv2.waitKey(0) & 0xFF
        file_path = 'captured_frame.png'

        image = cv2.imread(file_path)
        result = reader.readtext(image)
        ocr_result = ""  # 스페이스바를 눌렀을 때만 초기화
        trans_result = ''
        if result:
            for (bbox, text, prob) in result:
                ocr_result += text
            print(ocr_result)
            tmp = ocr_result.replace(" ", "")
            trans_result = translator.translate(tmp, src='de', dest='ko').text
            print(trans_result)
            synthesize_and_play_text(trans_result)
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

cap.release()
cv2.destroyAllWindows()
