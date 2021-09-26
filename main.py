# -*- coding: utf-8 -*-
#参考
#https://picamera.readthedocs.io/en/release-1.10/api_camera.html
#
#GPUメモリは256で安定動作。不足の場合は下記エラーが出る。
# mmal: mmal_vc_component_enable: failed to enable component: ENOSPC


import sys
import time
import cv2
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera

DEVICE_ID = 0 #v4l2-ctl --list-devices コマンド等で確認

WIDTH = 1280 #720
HEIGHT = 720 #480
FPS = 30

FULLSCREEN = True

def decode_fourcc(v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])


def imshow_fullscreen(winname, img):
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(winname, img)


def init_camera():
    try:
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FPS
        rawCapture = PiRGBArray(camera, size=(WIDTH, HEIGHT))
    except picamera.exc.PiCameraMMALError as e:
        print(type(e))
        print(e)
        print('exit by PiCameraMMALError')
        sys.exit()

    # allow the camera to warmup
    time.sleep(0.1)
    return camera, rawCapture


def main(camera, rawCapture):
    # 画像取得ループ
    while True:
        try:
            camera.capture(rawCapture, format="bgr")
            frame = rawCapture.array

            #ラズパイ公式ディスプレイの解像度に合わせてリサイズ
            ovl = cv2.resize(frame, dsize=(800, 480))

            # 画像表示
            if FULLSCREEN:
                imshow_fullscreen('frame', ovl)
            else:
                cv2.imshow('frame', ovl)

        except KeyboardInterrupt:
            print('exit by ctrl-c')
            break
        except picamera.exc.PiCameraValueError as e:
            #ケーブルが抜けたら出る。Incorrect buffer length
            #刺し直しても復旧しないので抜ける
            print(type(e))
            print(e)
            break
        except picamera.exc.PiCameraRuntimeError as e:
            #ケーブルが抜けたらこれの場合もある。"No data recevied from sensor"
            #刺し直しても復旧しないので抜ける
            print(type(e))
            print(e)
            break
        except Exception as e:
            print(type(e))
            print(e)
            break
            #frame = np.zeros((WIDTH,HEIGHT,3))
            #blank += [0,0,255][::-1] #RGBで青指定


        
        # キュー入力判定(1msの待機)
        # waitKeyがないと、imshow()は表示できない
        # 'q'をタイプされたらループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('exit by keyboard')
            break

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
    
    cv2.destroyAllWindows()
    camera.close()


if __name__ == '__main__':
    camera, rawCapture = init_camera()
    main( camera, rawCapture )
