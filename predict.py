from change import convert_jpg_to_png_pred, delete_all_files
from predict_arcface import face_recofnition
from use_email import use_email
import os

TRIGGER = 'trigger@applet.ifttt.com'
SUBJECT_ME_TO_TRIGGER = '#me'
SUBJECT_FRIEND_TO_TRIGGER = '#friend'
MAILBODY_TO_TRIGGER = ''

# パスを指定してその中のファイルの画像から予測する
def predict(directory_path):

    # 予測したい画像ファイルのディレクトリのパス
    directory = directory_path

    # contents = os.listdir(directory_path)

    # if not contents:
    #     return "stop"

    # 画像をPNGに変換して名前をimage_{n}.pngにする
    convert_jpg_to_png_pred(directory)

    # 画像から予測して誰かを判断する
    return_text = face_recofnition(directory)

    # ディレクトリ内のファイルを削除
    delete_all_files(directory)

    if return_text == "atsuto":
        use_email()
        use_email(mail_to=TRIGGER, subject=SUBJECT_ME_TO_TRIGGER, mail_body=MAILBODY_TO_TRIGGER)
    elif return_text == "yuto":
        use_email(subject="友達が来たよ", mail_body="welcome")
        use_email(mail_to=TRIGGER, subject=SUBJECT_FRIEND_TO_TRIGGER, mail_body=MAILBODY_TO_TRIGGER)
    else :
        use_email(subject="誰やねん", mail_body='不審者発見', img_path="FaceImages/image_1.jpg")

    return return_text