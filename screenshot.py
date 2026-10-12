import cv2
import mss
import numpy as np

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    x, y, w, h = cv2.selectROI("Select Chat", img)

    if w > 0 and h > 0:
        roi = img[y:y + h, x:x + w]
    else:
        return None
    cv2.destroyAllWindows()
    return roi