import cv2
import numpy
import time

EdgeMin = 0
EdgeMax = 200


def showCannyEdge(frame):
    windowName = "Result"
    newFrame = cv2.Canny(frame, EdgeMin, EdgeMax)
    while True:
        cv2.putText(newFrame, "W to close this window", (0, 450), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=2)
        cv2.imshow(windowName, newFrame)
        if cv2.waitKey(1) == ord('w'):
            cv2.destroyWindow(windowName)
            break;

def main():
    cap = cv2.VideoCapture(0)
    liveEdge = False
    if not cap.isOpened:
        raise RuntimeError("Failed to instantiate VideoCapture object :(")


    while True:
        ret, frame = cap.read()
        if not ret:
            print("##WARNING## - VideoCapture object failed to capture frame")


        input = cv2.waitKey(1)
        if input == ord(' '):
            showCannyEdge(frame)
        elif input == ord('r'):
            liveEdge = not liveEdge
        elif input == ord('q'):
            break


        if liveEdge:
            frame = cv2.Canny(frame, EdgeMin, EdgeMax)
        cv2.putText(frame, "Space to take photo | R to show edges | Q to quit", (0, 450), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=2)
        cv2.imshow("Camera", frame)

        
    

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
