try:
    import cscore

    camera = cscore.UsbCamera("usbcam", 0)
    camera.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    mjpegServer = cscore.MjpegServer("httpserver", 1187)
    mjpegServer.setSource(camera)
except Exception as e:
    print("cscore error (ignore this if you're testing/deploying):", e)
