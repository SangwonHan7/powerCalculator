import login
import imgProcess
import os
import excelProcess
import shutil
import warnings
import cv2
from tqdm import tqdm

warnings.filterwarnings("ignore")

login.loginProcess()

power_max = input('1위 전투력 : ')
power_min = input('꼴지 전투력 : ')

#이미지 리스트 가져오기
image_dir = './img'
error_dir = './error'
file_list = os.listdir(image_dir)

power_list = []

print('Start Process')
for img in tqdm(file_list):
    img_path = image_dir + '/' + img
    process_result = imgProcess.imageProcessing(img_path, power_max, power_min)
    if len(process_result)!=6:
        if not os.path.isdir(error_dir):                                                          
            os.mkdir(error_dir)
        shutil.move(img_path,error_dir+'/'+img)
    
    power_list.extend(process_result)

power_list.sort(reverse=True)
power_list.append("합산:"+str(sum(power_list)))

print('Make ExcelFile')
excelProcess.createExcelFile(power_list)
input('The process is complete. Press enter to exit.')
