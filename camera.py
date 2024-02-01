import cv2
import matplotlib.pyplot as plt
import time
from registration import registration
from change import delete_all_files
from change import convert_jpg_to_png_pred

DEVICE_ID = 0

SAVE_INTERVAL_SECONDS = 0.1  #　撮影のインターバル
NUM_IMAGES_TO_CAPTURE = 6*5  # 何枚撮影するか 6*5second

intervalSec = 1
numImages = 3

# 画像を切り出して保存する関数
def face_cut_function(path_name, t):

    # 画像のパスを取得
    path = path_name

    # 画像の読み込み
    if (t == 0):
        img = cv2.imread("aki/face/"+ path)
    else:
        img = cv2.imread("aki/face/"+ path)

    # 画像のグレースケール化
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 学習済みモデルの読み込み
    cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

    # 顔を検出する
    lists = cascade.detectMultiScale(img_gray, minSize=(100, 100))

    if len(lists):
        # 顔を検出した場合、forですべての顔を赤い長方形で囲む
        for (x,y,w,h) in lists:
            face_cut = img[y:y+h, x:x+w]
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
            cv2.imwrite("aki/facecut/"+path, face_cut)
            #cv2.imwrite("img/"+path, face_cut)
            print("Finished "+ path)
            cv2.waitKey(1) #　こいつ出来るヤツ　消すと危険
    else:
        print('Nothing')

def douga():

    #open
    cap = cv2.VideoCapture (DEVICE_ID)

    # capture
    for i in range(NUM_IMAGES_TO_CAPTURE):

        _, frame = cap.read()

        if(frame is not None):
            filename = f"image_{i + 1}.jpg"

            # save the image
            cv2.imwrite(f"aki/face/{filename}", frame)
            print(f"Image saved as {filename}")
            face_cut_function(filename, 0)

            time.sleep(SAVE_INTERVAL_SECONDS)

    delete_all_files("aki/face")
    convert_jpg_to_png_pred("aki/facecut")

    cap.release()
