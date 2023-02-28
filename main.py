import cv2
import numpy
import time
import copy
import svg_to_gcode.compiler as Compiler
import svg_to_gcode.compiler.interfaces as Interfaces
import svg_to_gcode.svg_parser as Parser

EdgeMin = 150
EdgeMax = 200

compiler = Compiler.Compiler(Interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)

# code for function by ospider
# https://stackoverflow.com/questions/43108751/convert-contour-paths-to-svg-paths
def saveContoursAsSVG(contours, width, height, filename):
    with open(filename, "w+") as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')

        for c in contours:
            f.write('<path d="M')
            for i in range(len(c)):
                x, y = c[i][0]
                f.write(f"{x} {y} ")
            f.write('" style="stroke:pink"/>')
        f.write("</svg>")

def contoursToSVG(contours, width, height):
    result = ""
    result += '<svg width="' + str(width) + '" height="' + str(height) \
    + '" xmlns="http://www.w3.org/2000/svg">'

    for c in contours:
        result += '<path d="M'
        for i in range(len(c)):
            x, y = c[i][0]
            result += str(x) + " " + str(y) + " "
        result += '" style="stroke:pink"/>'
    result += "</svg>"
    return result

def contoursToGCode(contours, width, height, filename):
    curves = Parser.parse_string(contoursToSVG(contours, width, height))
    compiler.append_curves(curves)
    compiler.compile_to_file(filename)
    print("success!")

# displays a single frame ready to print
def Capture(frame):
    windowName = "Result"
    while True:
        textFrame = copy.deepcopy(frame) # create copy of frame to add text to and display
        cv2.putText(textFrame, "W to take new photo, E to print", (0, 450), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=2)
        cv2.imshow(windowName, textFrame)
        input = cv2.waitKey(1)
        if input == ord('w'):
            cv2.destroyWindow(windowName)
            break
        elif input == ord('e'):
            # Do I really have to save then rewrite the file for this...
            contours, hierachy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contoursToGCode(contours, frame.shape[0], frame.shape[1], "test.gcode")
def main():
    cap = cv2.VideoCapture(0)
    liveCanny = False
    if not cap.isOpened:
        raise RuntimeError("Failed to instantiate VideoCapture object :(")


    while True:
        # take frame from camera
        ret, frame = cap.read()
        if not ret:
            print("##WARNING## - VideoCapture object failed to capture frame")

        cannyFrame = cv2.Canny(frame, EdgeMin, EdgeMax)

        # input
        input = cv2.waitKey(1)
        if input == ord(' '):
            # we need to apply canny first
            Capture(cannyFrame)
        elif input == ord('r'):
            liveCanny = not liveCanny
        elif input == ord('q'):
            break

        # output to screen, optionally applies edge detection
        if liveCanny:
            frame = cannyFrame
        cv2.putText(frame, "Space to take photo | R to show edges | Q to quit", (0, 450), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=2)
        cv2.imshow("Camera", frame)

        
    

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
