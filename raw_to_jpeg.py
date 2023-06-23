import cv2
import numpy as np

width = 3840
height = 2160
def show(d,w,h):
    cv2.imshow('data', cv2.resize(d, [w//3, h//3]))
    cv2.waitKey()
    cv2.destroyAllWindows()

for i in range(176):
    with open(f"image{i}", "rb") as rawimg:
        data = np.fromfile(rawimg, np.uint8, width * height)
        data = np.reshape(data ,(height, width))
        cv2.imwrite(f"cleangraypics/cleangray{i}.jpeg", data)
        cv2.waitKey()
        cv2.destroyAllWindows()
