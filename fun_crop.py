import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)
def imgCrop(img):
    
        imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = hands.process(imgs)
        # print(img_path)
        
        if res.multi_hand_landmarks:
            xcor = []
            ycor = []
            
            maxx = 0
            minx = 0
            maxy = 0
            miny = 0
            for hand_landmark in res.multi_hand_landmarks:
                for lm in hand_landmark.landmark:
                    xcor.append(lm.x)
                    ycor.append(lm.y)
                    
                maxx=max(xcor)
                maxy=max(ycor)
                minx = min(xcor)
                miny =min(ycor)
                
                h,w,c = img.shape
                maxx = int(maxx*w) + 35
                minx = int(minx*w) - 35
                maxy = int(maxy*h) + 35
                miny = int(miny*h) - 35
                # print(h,w,c)
                
                # print(maxx)
            # cv2.rectangle(img,(minx,miny),(maxx,maxy),(34,23,134),2)
            crop_img = img[miny:maxy,minx:maxx]
            if np.any(crop_img):
                resize_crop_img = cv2.resize(crop_img,(300,300))
                # return resize_crop_img
                return resize_crop_img, miny, minx, maxx, maxy
            else:
                return [0],0,0,0,0
        else:
            return [0],0,0,0,0
            
                    
