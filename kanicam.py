import cv2

# Webカメラをキャプチャするためのビデオキャプチャオブジェクトを作成
# デフォルトカメラは通常デバイスID 0 にありますが、別のカメラを使用する場合は ID を変更します
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラが開けませんでした")
    exit()

while True:
    # フレームをキャプチャする
    ret, frame = cap.read()

    # フレームが正常にキャプチャされたか確認
    if not ret:
        print("フレームを取得できませんでした")
        break

    # キャプチャしたフレームを表示
    cv2.imshow('Webcam', frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャを解放してウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
