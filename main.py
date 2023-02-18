import cv2
import numpy
import time

EdgeMin = 20
EdgeMax = 200


def showCannyEdge(frame):
    windowName = "Press w to leave" # this feels messy, fix later
    newFrame = cv2.Canny(frame, EdgeMin, EdgeMax)
    while True:
        cv2.imshow(windowName, newFrame)
        if cv2.waitKey(1) == ord('w'):
            cv2.destroyWindow(windowName)
            break;

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened:
        raise RuntimeError("Failed to instantiate VideoCapture object :(")


    while True:
        ret, frame = cap.read()
        if not ret:
            print("##WARNING## - VideoCapture object failed to capture frame")

        cv2.imshow("Press space to take photo", frame)

        if cv2.waitKey(1) == ord(' '):
            showCannyEdge(frame)
        if cv2.waitKey(1) == ord('q'):
            break
    

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
