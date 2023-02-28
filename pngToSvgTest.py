import cv2
import copy

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


image = cv2.imread("test.png")
image2 = copy.deepcopy(image) # image to overwrite with contours

# do contour detection WOW
image = cv2.Canny(image, 150, 200)
contours, hierachy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


cv2.drawContours(image2, contours, -1, (255,255,255), 3)

while True:
    cv2.imshow("FUCKSKFKSDG", image2)
    key = cv2.waitKey(1) 
    if key == ord('q'):
        break
    elif key == ord('w'):
        saveContoursAsSVG(contours, image2, "test.svg") ## this is nasty soz

cv2.destroyAllWindows()
