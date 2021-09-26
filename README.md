# Hdmi2Csi_Display

HDMI To CSI 変換アダプタを利用してPythonでRaspberryPiにHDMIを取り込み、ディスプレイに表示する。

# 動作確認機器

* Raspberry Pi 4B (その他未確認）

* HDMI To CSI Adapter For Raspberry Pi Series, 1080p@30fps Support
https://www.waveshare.com/hdmi-to-csi-adapter.htm

# Raspberry Pi 設定

* sudo raspi-config でCameraを有効にする
* sudo raspi-config でGPUメモリ量を増やす（環境次第。動作確認は256MB）
  不足の場合は下記エラーが出る
  mmal: mmal_vc_component_enable: failed to enable component: ENOSPC

# メモ

OpenCVのVideoCapture()ではうまく動かず、PiCameraで動いた。

# 参考
https://picamera.readthedocs.io/en/release-1.10/api_camera.html

