from PIL import Image
import cv2
import pytesseract
import numpy as np

def imageProcessing(img_path, power_max, power_min):
    
    result_power_list = []

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'
 
    img = cv2.imread(img_path)
   
    #이미지 크기 선언
    height, width , _ = img.shape

    #이미지 사이즈 조정
    resize_img = cv2.resize(img, dsize=(int(width/1.15), int(height/1.15)), interpolation=cv2.INTER_AREA)

    #GrayScale
    gray_img = cv2.cvtColor(resize_img,cv2.COLOR_BGR2GRAY)
    
    blur_img = cv2.GaussianBlur(gray_img, ksize=(5,5), sigmaX=0)
    ret, thresh1 = cv2.threshold(blur_img, 127, 255, cv2.THRESH_BINARY)
    edged_img = cv2.Canny(blur_img, 10, 250)

    contours, _ = cv2.findContours(edged_img.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_xy = np.array(contours)
    contours_xy.shape

    # x의 min과 max 찾기
    x_min, x_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][0]) #네번째 괄호가 0일때 x의 값
            x_min = min(value)
            x_max = max(value)
    
    # y의 min과 max 찾기
    y_min, y_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1]) #네번째 괄호가 0일때 x의 값
            y_min = min(value)
            y_max = max(value)

    # image trim 하기
    x = x_min
    y = y_min
    w = x_max-x_min
    h = y_max-y_min



    # power 영역  trim
    power_x = 0.8*x_max+0.2*x_min
    power_y = 0.25*y_max+0.75*y_min
    power_w = x_max-power_x
    power_h = y_max-power_y

    img_trim = resize_img[y:y+h, x:x+w]
    power_list_img_trim = gray_img[int(power_y):int(power_y+power_h), int(power_x):int(power_x+power_w)]
    
    #숫자 영역 가져오기
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    grad = cv2.morphologyEx(power_list_img_trim, cv2.MORPH_GRADIENT, kernel)
    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros(bw.shape, dtype=np.uint8)
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
        if r > 0.45 and w > 8 and h > 8:
            power_img = power_list_img_trim[y:y+h,x:x+w]
            power_binary_img = cv2.threshold(power_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]     
            power = pytesseract.image_to_string(power_binary_img,lang=None,config='--psm 6 --oem 3  -c tessedit_char_whitelist=0123456789').strip()

            # print(power)
            # cv2.imshow("power_trim"+str(idx),power_binary_img)
            # cv2.rectangle(power_list_img_trim, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)

            if(power!='' and int(power)<=int(power_max) and int(power)>=int(power_min)):
                result_power_list.append(int(power))

            
    
    # cv2.imshow("img_trim", power_list_img_trim)
    # cv2.waitKey(0)

    return result_power_list
