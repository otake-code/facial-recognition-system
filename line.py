import requests

def line_notify(message,picture=None):
    line_notify_token = '' #見守りサービス
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    #picture= "image_1.jpg"
    if picture: #画像あり
        try:
            files = {'imageFile': open(f"switchbot/{picture}", "rb")} # 送信画像設定 # バイナリファイルオープン
            requests.post(line_notify_api, data=payload, headers=headers ,files=files)#送信
        except FileNotFoundError as e:
            line_notify(f"Error: {e}")
    else:
        try:
            requests.post(line_notify_api, data=payload, headers=headers)  # 画像なしの場合
        except FileNotFoundError as e:
            line_notify(f"Error: {e}")

    # if picture:
    #     picture_path = f"../aki/facecut/{picture}"
    #     try:
    #         files = {'imageFile': open(picture_path, "rb")}  # 送信画像設定 # バイナリファイルオープン
    #         requests.post(line_notify_api, data=payload, headers=headers, files=files)  # 送信
    #     except FileNotFoundError as e:
    #         line_notify(f"Error: {e}")
    # else:
    #     requests.post(line_notify_api, data=payload, headers=headers)  # 画像なしの場合

def perform_notification(p):
    try:
        text = f"\n高齢者を検知しました。\nドアを施錠しました。"
        print(text)
        #picture= f"image_1.jpg"
        line_notify(text,p)
    except Exception as e:
        line_notify(str(e))

if __name__ == '__main__':
    #p = "image_1.jpg"
    p=""
    perform_notification(p)
