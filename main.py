import cv2
import numpy
import time
import copy
import svg_to_gcode.compiler as Compiler
import svg_to_gcode.compiler.interfaces as Interfaces
import svg_to_gcode.svg_parser as Parser

EdgeMin = 150
EdgeMax = 200





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
    compiler = Compiler.Compiler(Interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
    curves = Parser.parse_string(contoursToSVG(contours, width, height))
    compiler.append_curves(curves)
    compiler.compile_to_file(filename)
    print("success!")

def scaleContours(contours, scale):
    result = []
    for contour in contours:
        resultingContour = []
        #print(contour)
        for point in contour:
            x = int(float(point[0][0])*scale)
            y = int(float(point[0][1])*scale)
            resultingPoint = [[x, y]]
            resultingContour.append(resultingPoint)
        result.append(resultingContour)
    #print(result)
    return result

def getMin(a, b):
    if a <= -1:
        return b
    elif b <= -1:
        return a
    elif a < b:
        return a
    else:
        return b
    
def getMax(a, b):
    if a > b:
        return a
    else:
        return b

def calculateDrift(contours, frame):
    xDrift = -1
    yDrift = -1

    for contour in contours:
        for point in contour:
            xDrift = getMin(point[0][0], xDrift)
            yDrift = getMax(point[0][1], yDrift)
    
    yDrift -= frame.shape[1] #idk what james was on but i want some

    return xDrift, yDrift



def correctContours(contours, frame):
    result = []

    x, y = calculateDrift(contours, frame)

    for contour in contours:
        resultingContour = []
        #print(contour)
        for point in contour:
            #print(point)
            resultingX = point[0][0]-x
            resultingY = point[0][1]-y
            resultingPoint = [[resultingX, resultingY]]
            resultingContour.append(resultingPoint)
        result.append(resultingContour)
    #print(result)
    return result


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
            print(contours[0])
            contoursToGCode(contours, frame.shape[0], frame.shape[1], "testBefore.gcode")
            contours = scaleContours(contours, 0.5)
            print(contours[0])
            contoursToGCode(contours, frame.shape[0], frame.shape[1], "testMiddle.gcode")
            contours = correctContours(contours, frame)
            contoursToGCode(contours, frame.shape[0], frame.shape[1], "testAfter.gcode")


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
