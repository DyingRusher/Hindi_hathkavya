import datetime
import pickle
import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
from PIL import Image
import time
import threading
from gtts import gTTS
from playsound import playsound

from fun_crop import imgCrop

# Load your model
# model = pickle.load(open('./modelp.p', 'rb'))
model = pickle.load(open('modelp_3_2_24.p', 'rb'))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.4)

# im = Image.open("D:\Subjects\SGP\RandomForest\icon2.ico")
# st.set_page_config(
#     page_title="Hindi Sign | ML", 
#     page_icon=im,
# )

# Create a Streamlit web app
st.title("Hindi Sign Language Recognition")

# Initialize the webcam capture
cap = cv2.VideoCapture(0)

imgframe = st.empty()
char = st.empty()
sent = st.empty()

# recognized_characters = []
recognized_characters = ""

# def recognize_character():
#     # recognized_characters = []
#     while True:
#         recognized_characters.append(result)
#         time.sleep(5)  # Wait for 5 seconds before recognizing the next character
#         print("RE:",recognized_characters)
#         sentence = ' '.join(recognized_characters)
#         larger_font_text = f'<span style="font-size: 36px;">Sentence : {sentence}</span>'   
#         sent.markdown(larger_font_text,unsafe_allow_html=True)

# while st.checkbox("Run the application", True):

confirmation_timer = 0
is_confirming = False
append = False
aft_val = ""
pre_val = ""

confirmation_timer2 = time.time()

while True:
    confidence = True
    data = []
    x_ =[]
    y_ =[]
    succes , img = cap.read()
    img = cv2.flip(img, 1)
    
    # validImg = imgCrop(img) 
    validImg, miny, minx, maxx, maxy = imgCrop(img)
    # print("Index:",miny, minx,maxx,maxy)
    if np.any(validImg):
        # validImg= remove(validImg)
        # cv2.imshow("Crop Img and background remove",validImg)
        imgb = cv2.cvtColor(validImg,cv2.COLOR_BGR2RGB)
        # img = validImg
        h,w,c = img.shape
        res = hands.process(imgb)
        # cv2.imshow("Crop Img",validImg)
        # cv2.imshow("Crop Img",validImg)
        ap = []
        if res.multi_hand_landmarks:
            for lm in res.multi_hand_landmarks:
                # mp_drawing.draw_landmarks(img,lm,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
                lm = lm.landmark
                for i in lm:
                    ap.append(i.x)
                    ap.append(i.y)
                    x_.append(i.x)
                    y_.append(i.y)
            map_char = {
                'w(blank)':"blank",
                'K(k)':"\u0915",
                'f(dha)':"\u0927",
                's(da)':"\u0924",
                'h(na)':"\u0928",
                'k(kha)':"\u0916",
                'l(tha)':"\u0925",
                'C(ca)':"\u091A",
                'D(d)':"\u0921",
                'q(nga)':"\u0919",
                'r(T)':"\u0924",
                'E(ee)':"\u0908",
                'P(p)':"\u092A",
                'H(ha)':"\u0939",
                'c(chha)':"\u091B",
                'j(jha)':"\u091D",
                'T(ta)':"\u091F",
                't(thh)':"\u0920",
                'I(i)':"\u0907",
                'B(b)':"\u092C",
                'G(g)':"\u0917",
                'g(gha)':"\u0918",
                'O(oo)':"\u090A",
                'N(n)':"\u0923",
                'R(r)':"\u0930",
                'M(ma)':"\u092E",
                'J(ja)':"\u091C",
                'u(au)':"\u0914",
                'd(dh)':"\u0922",
                'Y(y)':"\u092F",
                ';(re)':"\u090B",
                'U(u)':"\u0909",
                'z(sa)':"\u0938",
                'e(e)':"\u090F",
                'i(ai)':"\u0910",
                'p(fa)':"\u092B",
                'L(la)':"\u0932",
                '_(shha)':"\u0937",
                'b(bha)':"\u092D",
                'V(v)':"\u0935",
                '](sha)':"\u0936",
                'a(aa)':"\u0906",
                'o(o)':"\u0913",
                'A(a)':"\u0905",

            }
            map_matra = {
                "\u0906":"\u093E",
                "\u0907":"\u093F",
                "\u0908":"\u0940",
                "\u0909":"\u0941",
                "\u090A":"\u0942",
                "\u090B":"\u0943",
                "\u090F":"\u0947",
                "\u0910":"\u0948",
                "\u0913":"\u094B",
                "\u0914":"\u094C",
            }
            # map = {
            #     'K(k)':'क',
            #     'f(dha)':'घ',
            #     's(da)':'द',
            #     'h(na)':'न',
            #     'k(kha)':'ख',
            #     'l(tha)':'थ',
            #     'C(ca)':'च',
            #     'D(d)':'ड',
            #     'q(nga)':'ङ',
            #     'r(T)':'ट',
            #     'E(ee)':'ई',
            #     'P(p)':'प',
            #     'H(ha)':'ह',
            #     'c(chha)':'छ',
            #     'j(jha)':'झ',
            #     'T(ta)':'ट',
            #     't(thh)':'ठ',
            #     'I(i)':'इ',
            #     'B(b)':'ब',
            #     'G(g)':'ग',
            #     'g(gha)':'घ',
            #     'O(oo)':'ऊ',
            #     'N(n)':'ण',
            #     'R(r)':'र',
            #     'M(ma)':'म',
            #     'J(ja)':'ज',
            #     'u(au)':'औ',
            #     'd(dh)':'ढ',
            #     'Y(y)':'य',
            #     ';(re)':'ऋ',
            #     'U(u)':'उ',
            #     'z(sa)':'स',
            #     'e(e)':'ए',
            #     'i(ai)':'ऐ',
            #     'p(fa)':'फ',
            #     'L(la)':'ल',
            #     '_(shha)':'ष',
            #     'b(bha)':'भ',
            #     'V(v)':'व',
            #     '](sha)':'श',
            #     'a(aa)':'आ',
            #     'o(o)':'ओ',
            #     'A(a)':'अ',
            # }

            # if len(ap)==42:
            #     data.append(ap)
            #     data = np.array(data)
            #     result = model.predict(data)
            # print(result[0])
            # print(data[0])
            # print("A:",str(result))
            # result = map['O(oo)']
            # result = map[result[0]]
            
            if len(ap) == 42:
                pre_val = aft_val
                data.append(ap)
                data = np.array(data)
                result = model.predict(data)
                aft_val = result

                pro_res = model.predict_proba(data)
                confi = max(pro_res[0])

                result = map_char[result[0]]

                if confi < 0.3:
                    result = "Could not find"
                    confidence = False
                    append = False
                    confirmation_timer = time.time()
                if confidence:
                # print("Result:",result)
                    if not is_confirming:
                        # print("not")
                        is_confirming = True
                        confirmation_timer = time.time()
                    # print(is_confirming)
                    # Check if 5 seconds have passed since the character recognition
                    # print("C1",time.time()-confirmation_timer)
                    if pre_val != aft_val:
                        append = False
                        is_confirming = False
                        confirmation_timer = time.time()
                    
                    if time.time() - confirmation_timer >= 2 and not append:
                        # recognized_characters.append(result)
                        recognized_characters = recognized_characters + result
                        print("1:",recognized_characters)
                        append = True
                        # Reset confirmation flag and timer
                        # is_confirming = False
                        # confirmation_timer = 0
                    # result = "aa"
                    # print("A:",append)
                    if append and time.time() - confirmation_timer >= 4:
                        recognized_characters = recognized_characters[:-1]
                        print("2:",recognized_characters)
                        # recognized_characters.append(map_matra[result])
                        recognized_characters = recognized_characters + map_matra[result]
                        print("3:",recognized_characters)
                        append = False
                        is_confirming = False
                        confirmation_timer = 0
            else:
                is_confirming = False  # Reset confirmation flag if no hand detected

            # if not is_confirming:
            #     # print("not")
            #     is_confirming = True
            #     confirmation_timer = time.time()
            # # print(is_confirming)
            # # Check if 5 seconds have passed since the character recognition
            # if time.time() - confirmation_timer >= 3:
            #     print("INSIDE 3")
            #     if len(ap) == 42:
            #         data.append(ap)
            #         data = np.array(data)
            #         result = model.predict(data)
            #         result = map[result[0]]
            #         print("Result:",result)
            #     else:
            #         print('else')
            #         is_confirming = False 
            #     # Reset confirmation flag and timer
            #     recognized_characters.append(result)
            #     is_confirming = False
            #     confirmation_timer = 0

            # print("Confirm:",is_confirming)
            # result="blank"
            # if time.time() - confirmation_timer >= 5 and is_confirming==True:
            #     recognized_characters.append("blank")
            #     is_confirming = False 
            #     confirmation_timer = 0
             # Reset confirmation flag if no hand detected

            x1 = int(min(x_)*w)
            y1 = int(min(y_)*h)
            x2 = int(max(x_)*w)
            y2 = int(max(y_)*h)
            cv2.rectangle(img,(minx,miny),(maxx,maxy),(0,0,0),3)
            # cv2.putText(img,str(result[0]),(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
            confirmation_timer2=time.time()
    else:
        # cv2.putText(img,str("Unknow"),(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
        result='blank'
        # print("C2",time.time()-confirmation_timer2)
        if time.time() - confirmation_timer2 >= 5:
            # recognized_characters.append("_")
            recognized_characters = recognized_characters + "\u0020"+"\u0020"

            #for text to speech
            last_word = ""
            len_rc = len(recognized_characters) - 1


            # while(len_rc>0):
            #     last_word += recognized_characters[len_rc]
            #     len_rc = len_rc-1
                
            # if(last_word!=''):
            #     date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            #     filename = "hindi" + date_string + ".mp3"
            #     obj = gTTS(text= last_word,slow=False, lang='hi')
            #     obj.save(filename)

            #     playsound(filename)

            print("4:",recognized_characters)
            confirmation_timer2 = time.time()
        confirmation_timer = time.time()
        append = False
            
    imgframe.image(img, channels="BGR", use_column_width=True)  
    b = "\u0941"
    larger_font_text = f'<span style="font-size: 36px;">Character : {result}</span>'   
    # a = "\u0936"
    # b = "\u093F"
    # b = "\u0941"
    # result = a + b
    char.markdown(larger_font_text,unsafe_allow_html=True)

    # time.sleep(5)
    
    # sentence = ' '.join(recognized_characters)
    larger_font_text = f'<span style="font-size: 36px;">Sentence : {recognized_characters}</span>'   
    # larger_font_text = f'<span style="font-size: 36px;">Sentence : {sentence}</span>'   
    sent.markdown(larger_font_text,unsafe_allow_html=True)
    # recognize_character()



# Release the webcam when the app is closed
cap.release()