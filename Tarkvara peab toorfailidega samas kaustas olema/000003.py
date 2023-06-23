import numpy as np
import cv2

width = 3840
height = 2160
for i in range(176):
    with open(f"image{i}", "rb") as rawimg:
        data = np.fromfile(rawimg, np.uint8, width * height)
        bayer_im = np.reshape(data ,(height, width))
        
    #bgr = cv2.demosaicing(bayer_im, cv2.COLOR_BayerGR2BGR)
    bgr = cv2.cvtColor(bayer_im, cv2.COLOR_BayerBG2BGR)


    cv2.imshow('bgr', bayer_im)
    cv2.imwrite(f"jpeg/image{i}_a.jpeg", bayer_im)

    # "White balance":
    #bgr[:, :, 0] = np.minimum(bgr[:, :, 0].astype(np.float32)*1.8, 255).astype(np.uint16)
    #bgr[:, :, 2] = np.minimum(bgr[:, :, 2].astype(np.float32)*1.67, 255).astype(np.uint16)
    bgr = cv2.cvtColor(bgr, cv2.COLOR_RGB2YCrCb)
    cv2.imshow('bayer_im', bgr)
    cv2.imwrite(f"jpeg/image{i}_b.jpeg", bgr)
    bgr = cv2.cvtColor(bgr, cv2.COLOR_RGB2YCrCb)
    cv2.imshow('bgr WB', bgr)
    cv2.imwrite(f"jpeg/image{i}_c.jpeg", bgr)
    cv2.waitKey()
    cv2.destroyAllWindows()