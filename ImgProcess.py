import cv2
import cv2.cv as cv

# draw rectangle in the image
def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

# spilt image into hei * wid block
def splitImg(img, wid = 3, hei = 2):
    height, width = img.shape[0], img.shape[1]
    widStep = width / wid
    heiStep = height / hei
    split_info = []
    for j in range(hei):
        for i in range(wid):
            split_info.append([j*heiStep, (j+1)*heiStep, i*widStep, (i+1)*widStep])
    return split_info

def getBlockImg(img, wid = 3, hei = 2):
    split_info = splitImg(img, wid, hei)
    rects = map(lambda x : (x[2], x[0], x[3], x[1]), split_info)
    vis = img.copy()
    idx = 0
    for rect in rects:
        draw_rects(vis, [rect], (128, 0, 0))
        border = min(rect[3] - rect[1], rect[2] - rect[0])
        cv2.putText(vis, str(idx), ((rect[0]+rect[2]) / 2, (rect[3]+rect[1]) / 2), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0 ,0), thickness = 8, lineType = 8) 
        idx += 1
    return vis

# de-color for the entire image
def deColor(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(img)
    height, width = img.shape[0], img.shape[1]
    min_a, max_a = a.min(), a.max()
    thread = min_a + 1 * (max_a - min_a) / 3.0
    for h in range(height):
        for w in range(width):
            if a[h][w] > thread:
                img[h][w][1] -= 50 * float(a[h][w] - thread) / (max_a - thread)
    img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
    return img

def process(Full_img, select = 0, wid = 3, hei = 2):
    split_info = splitImg(Full_img, wid, hei)
    hs, he, ws, we = split_info[select]
    img = Full_img[hs:he, ws:we]
    Full_img[hs:he, ws:we] = deColor(img)
    return Full_img
