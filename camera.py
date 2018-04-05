try:
    import cscore

    camera1 = cscore.UsbCamera("usbcam1", 0)
    camera1.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    camera1.setBrightness(40)
    mjpegServer1 = cscore.MjpegServer("httpserver", 1187)
    mjpegServer1.setSource(camera1)

    camera2 = cscore.UsbCamera("usbcam2", 1)
    camera2.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    camera2.setBrightness(40)
    mjpegServer2 = cscore.MjpegServer("httpserver", 1188)
    mjpegServer2.setSource(camera2)
except Exception as e:
    print("cscore error (ignore this if you're testing/deploying):", e)
