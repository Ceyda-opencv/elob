import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time
import mediapipe as mp
from pymata4 import pymata4
import open

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

saniye = 0
hepsı = 0

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

coff = np.polyfit(x, y, 3)  # y = Ax^3 + Bx^2 + Cx + D bu bir 3.dereceden denklem çift el olduğu için de 3 değeri var.
ilk = time.time()
sol = 0
sag = 0
an = 0
TespıtSayısı = 0
SolKilit = False
KabaAyar = False
InceAyar = False
SagSol = False
Kilitlenme = True

IMAGE_FILES = []
while True:
    with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5) as hands:
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.flip(cv2.imread(file), 1)
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            print('Handedness:', results.multi_handedness)
            if not results.multi_hand_landmarks:
                continue
            image_height, image_width, _ = image.shape
            annotated_image = image.copy()
            for hand_landmarks in results.multi_hand_landmarks:
                cvzone.putTextRect(img, f'CALISIYORUM', (50, 100))
                x12, y12 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y
                x11, y11 = hand_landmarks.landmark[11].x, hand_landmarks.landmark[11].y
                if y12 > y11:
                    cvzone.putTextRect(img, f'CALISIYORUM', (50, 100))  # burası deneme
                print('hand_landmarks:', hand_landmarks)
                print(
                    f'Index finger tip coordinates: (',
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                )
                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
            cv2.imwrite(
                '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

    success, img = cap.read()
    hands, img = detector.findHands(img)
    son = time.time()
    if son - ilk >= 1 and SolKilit == False:
        ilk = son
        saniye = saniye + 1
    if hands:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']  # yandaki cm yi gösteren x,y,genişlik yükseklik değerleri verildi.
        x1, y1, z1 = lmList[5]  # 5.noktanın yeri
        x2, y2, z2 = lmList[17]  # 17.noktanın yeri

        distance = int(abs(math.sqrt(abs(y2 - y1) * 2 + abs(x2 - x1) * 2)))
        A1, B1, C1, D1 = coff  # burada 3.dereceden denklemin katsayılarını coff'a eşitliyoruz.
        distanceCM = A1 * distance * 3 + B1 * distance * 2 + C1 * distance + D1  # denklem oluşturuldu.
        cvzone.putTextRect(img, f'{int(distanceCM)} cm',(x, y))  # puttextrect ile hem dikdörtegen hem de yazı birleştirildi.
        durumsag = False
        durumsol = False

        font = cv2.FONT_HERSHEY_PLAIN
        if hands[0]["type"] == "Sol El":
            sol = 1

            if TespıtSayısı == 0:
                saniye = 0
            if TespıtSayısı == 2:
                saniye = 9
            x3, y3, z3 = lmList[12]
            x4, y4, z4 = lmList[9]
            if TespıtSayısı == 1:
                if y3 > y4:
                    # for i in range(0, m):
                    #     board.stepper_write(30, -512)
                    #     time.sleep(0.5)
                    durumsol = True
                    SolKilit = True
                    saniye = 3
                    DistanceSol = distanceCM
                    cv2.putText(img, f'SOL EL KILITLENDI', (100, 100), font, 4, (255, 0, 0), 6)
                    cv2.putText(img, str(durumsol), (500, 50), font, 4, (255, 0, 0), 6)
                else:
                    durumsol = False
                    SolKilit = False
                    cv2.putText(img, f'SOL EL TESPIT', (20, 50), font, 4, (255, 0, 0), 6)
                    cv2.putText(img, str(durumsol), (500, 50), font, 4, (255, 0, 0), 6)

        if hands[0]["type"] == "Sag El":
            sag = 1
            x9, y9, z9 = lmList[9]
            x6, y6, z6 = lmList[6]
            x7, y7, z7 = lmList[7]
            x8, y8, z8 = lmList[8]
            x16, y16, z16 = lmList[16]
            x13, y13, z13 = lmList[13]
            x12, y12, z12 = lmList[12]
            x15, y15, z15 = lmList[15]


            if SolKilit == True:
                durumsol = True
                cv2.putText(img, str(durumsol), (500, 50), font, 4, (255, 0, 0), 6)
                if y12 > y9 and not y16 < y15 and y8 < y7 :
                    InceAyar = True
                    KabaAyar = False
                    Kilitlenme = False
                elif y8 > y6 and y12 > y9 and y16 > y15:
                    SagSol = True
                    Kilitlenme = True
                elif y8 < y6 and y15 < y16 :
                    KabaAyar = True
                    InceAyar = False
                    Kilitlenme = True
                elif y15 > y16 or y8 > y7 or y9 > y12:
                    InceAyar = False
                    KabaAyar = False
                    Kilitlenme = True
                else:
                    KabaAyar = False
                    InceAyar = False
                    SagSol = False
                    Kilitlenme = True






            else:

                cv2.putText(img, f'SAG EL TESPIT', (800, 50), font, 4, (255, 0, 0),6)  # puttextrect ile hem dikdörtegen hem de yazı birleştirildi
                cv2.putText(img, str(durumsol), (500, 50), font, 4, (255, 0, 0), 6)



        else:
            sag = 0
            durumsag = 0

        if sol == 1 and sag == 1:

            an = an + 1
            cv2.putText(img, f'{str(saniye)}sn', (850, 150), font, 4, (0, 0, 0), 6)
            cv2.putText(img, f'SAG ve SOL TESPIT', (20, 150), font, 4, (255, 0, 0),6)  # puttextrect ile hem dikdörtegen hem de yazı birleştirildi
            if 20 > saniye > 3 and hepsı == 0 and durumsol == False:
                cv2.putText(img, str(durumsol), (500, 50), font, 4, (255, 0, 0), 6)
                cv2.putText(img, f'AYARLAR ACILDI', (20, 100), font, 4, (0, 255, 0), 6)
                TespıtSayısı = 1
                if saniye > 8:
                    hepsı = 1


            elif saniye > 20 and hepsı == 1:
                cv2.putText(img, f'AYARLAR KAPANDI', (20, 100), font, 4, (0, 0, 255), 6)
                TespıtSayısı = 2
                if saniye > 13:
                    hepsı = 0
                    saniye = 0
            elif durumsol == True:
                saniye = 3
                cv2.putText(img, f'Kilit noktasi {int(DistanceSol)} cm', (20, 700), font, 4, (255, 0, 0), 6)
                if KabaAyar == True:
                    cv2.putText(img, f'Kaba Ayar', (20, 300), font, 4, (255, 0, 0), 6)
                    if DistanceSol < distanceCM:
                        cv2.putText(img, f'Zoom Out', (20, 200), font, 4, (255, 0, 0), 6)
                        cv2.putText(img, f'{str(int((DistanceSol - distanceCM)))}cm', (20, 100), font, 4, (255, 0, 0),6)
                    elif DistanceSol > distanceCM:
                        cv2.putText(img, f'Zoom In', (20, 200), font, 4, (255, 0, 0), 6)
                        cv2.putText(img, f'{str(int((DistanceSol - distanceCM)))}cm', (20, 100), font, 4, (255, 0, 0),6)
                elif InceAyar == True:
                    cv2.putText(img, f'Ince Ayar', (20, 300), font, 4, (255, 0, 0), 6)
                    if DistanceSol < distanceCM:
                        cv2.putText(img, f'INCE Zoom Out', (20, 200), font, 4, (255, 0, 0), 6)
                        cv2.putText(img, f'{str(int((DistanceSol - distanceCM)))}cm', (20, 100), font, 4, (255, 0, 0),6)
                    elif DistanceSol > distanceCM:
                        cv2.putText(img, f'INCE Zoom In', (20, 200), font, 4, (255, 0, 0), 6)
                        cv2.putText(img, f'{str(int((DistanceSol - distanceCM)))}cm', (20, 100), font, 4, (255, 0, 0),6)


                elif SagSol == True:
                    x4, y4, z4 = lmList[4]
                    x20, y20, z20 = lmList[20]
                    x15, y15, z15 = lmList[15]
                    x8, y8, z8 = lmList[8]
                    x9, y9, z9, = lmList[9]

                    x,y,z=x9,y9,z9
                    # cv2.putText(img, f'{x9},{y9}', (20, 250), font, 4, (255, 0, 0), 6)
                    # cv2.putText(img, f'.', id(x + 50, y + 50), font, 10, (255, 0, 0), 6)
                    # cv2.putText(img, f'.', id(x + 50, y - 50), font, 10, (255, 0, 0), 6)
                    # cv2.putText(img, f'.', id(x - 50, y + 50), font, 10, (255, 0, 0), 6)
                    # cv2.putText(img, f'.', id(x - 50, y - 50), font, 10, (255, 0, 0), 6)

                    yon = False
                    cv2.putText(img, f'SAG-SOL', (20, 300), font, 4, (255, 0, 0), 6)



                    if x9 > 540 and x9 < 740 and y9 < 260:
                        cv2.putText(img, f'YUKARI,{int(abs(y9 - 260))}br', (20, 200), font, 4, (255, 0, 0), 6)

                        yon = True
                    elif x9 > 540 and x9 < 740 and y9 > 460:
                        cv2.putText(img, f'ASAGI,{int(abs(y9-460))}br', (20, 200), font, 4, (255, 0, 0), 6)
                        yon = True
                    elif 260 < y9 < 460 and x9 > 740:
                        cv2.putText(img, f'SAGA,{int(abs(x9-740))}br', (20, 200), font, 4, (255, 0, 0), 6)
                        yon = True
                    elif 260 < y9 < 460 and x9 < 540:
                        cv2.putText(img, f'SOLA,{int(abs(x9-540))}br', (20, 200), font, 4, (255, 0, 0), 6)
                        yon = True
                    elif x9 > 740 and y9 < 260:
                        yon = True
                        cv2.putText(img, f'SAGA,YUKARI,{int(math.sqrt(abs(abs(x9-740)*2) + abs(y9 - 260)*2))}br', (20, 200), font, 4, (255, 0, 0), 6)
                    elif x9 < 540 and y9 < 260:
                        yon = True
                        cv2.putText(img, f'SOLA,YUKARI,{int(math.sqrt(abs(abs(x9-540)*2) + abs(y9 - 260)*2))}br', (20, 200), font, 4, (255, 0, 0), 6)
                    elif x9 > 740 and y9 > 460:
                        cv2.putText(img, f'SAGA,ASAGI, {int(math.sqrt(abs(abs(x9-740)*2) + abs(y9 - 460)*2))}br', (20, 200), font, 4, (255, 0, 0), 6)
                        yon = True
                    elif x9 < 540 and y9 > 460:
                        yon = True
                        cv2.putText(img, f'SOLA,ASAGI, {int(math.sqrt(abs(abs(x9-540)*2) + abs(y9 - 460)*2))}br', (20, 200), font, 4, (255, 0, 0), 6)
                    elif yon == False:
                        cv2.putText(img, f'KILITLENDI', (20, 200), font, 4, (255, 0, 0), 6)
                    else:
                        cv2.putText(img, f'', (20, 200), font, 4, (255, 0, 0), 6)
                elif Kilitlenme == True:
                    cv2.putText(img, f'', (20, 200), font, 4, (255, 0, 0), 6)



    else:
        saniye = 0
        sol = 0
        sag = 0
        an = 0
        font = cv2.FONT_HERSHEY_PLAIN
        if sol == 0 and sag == 0 and TespıtSayısı == 1:
            hepsı = 0
            saniye = 3

            cv2.putText(img, f'AYARA DEVAM EDEBILIRSINIZ.', (20, 150), font, 4, (0, 255, 0), 6)

        if TespıtSayısı == 0:
            hepsı = 0
            saniye = 0
            cv2.putText(img, f'AYARI BASLATIN.', (20, 150), font, 4, (255, 0, 0), 6)
        if TespıtSayısı == 2:
            hepsı = 1
            saniye = 8
            cv2.putText(img, f'AYARI BASLATIN.', (20, 150), font, 4, (255, 0, 0), 6)
    # for i in range(0, 8):
    #     board.stepper_write(30, -512)
    #     time.sleep(0.5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)