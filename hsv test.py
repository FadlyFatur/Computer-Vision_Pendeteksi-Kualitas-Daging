
import cv2
import numpy as np

def nothing(x):
    pass
## Read
img_in = cv2.imread("busuk3.jpg")

r = cv2.selectROI(img_in)
img = img_in[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
# Creating a window for later use
# cv2.namedWindow('result')


# Starting with 100's to prevent error while masking
# Creating track bar
# cv2.createTrackbar('h',  'result', 0, 179, nothing)
# cv2.createTrackbar('s', 'result', 0, 255, nothing)
# cv2.createTrackbar('v', 'result', 0, 255, nothing)
# cv2.createTrackbar('U - H', 'result', 179, 179, nothing)
# cv2.createTrackbar('U - S', 'result', 255, 255, nothing)
# cv2.createTrackbar('U - V', 'result', 255, 255, nothing)

    #converting to HSV
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result

    # mask1 = cv2.inRange(img_hsv, (0, 50, 20), (5, 255, 255))
    # mask2 = cv2.inRange(img_hsv, (175, 50, 20), (180, 255, 255))

    # Normal masking algorithm
    # lower_blue = np.array([h, s, v])
    # upper_blue = np.array([u_h,u_s,u_v])

lower_blue = np.array([1, 50, 150])
upper_blue = np.array([40,215,255])

mask = cv2.inRange(hsv,lower_blue, upper_blue)

result = cv2.bitwise_and(img,img,mask = mask)

cv2.imshow("mask", mask)
cv2.imshow("result", result)



r,g,b= cv2.split(result)
print(r)

mean = np.mean(result)
print(mean)

# cv2.imshow("target.png", target)
cv2.waitKey(0)
cv2.destroyAllWindows()