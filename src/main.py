import numpy as np
import cv2

def find_yellow_lanes(bgr_img, result_dir):
    hls_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HLS)

    #The colors are set because our track's lanes are yellow. In this case, blue.
    lower_yellow = np.array([10, 30, 90])
    upper_yellow = np.array([40, 220, 255])

    yellow_filter = cv2.inRange(hls_img, lower_yellow, upper_yellow)
    yellow_filtered_img = cv2.bitwise_and(bgr_img, bgr_img, mask=yellow_filter)
    
    cv2.imwrite(result_dir, yellow_filtered_img)
    print('%s saved' % 'lane detection image')

def find_n_largest_contours(filtered_img, result_dir, n=2):
    # find contours
    img = filtered_img.copy()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, h = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # sort contours by size
    area_array = []
    for i,c in enumerate(contours):
        area = cv2.contourArea(c)
        area_array.append(area)
    sorted_contours = sorted(zip(area_array, contours), key=lambda x:x[0], reverse=True)
    
    my_contours = []
    # top n size contours
    for i in range(n):
        try:
            my_contours.append(sorted_contours[i][1])
        except IndexError:
            break
    cv2.drawContours(img, my_contours, -1, (0,255,0))

    contour_centroids = []
    excepted = False
    # find center of top n size contours
    for c in my_contours:
        # center of the contour
        M = cv2.moments(c)
        try:
            # cX:row, cY:col, top_left: [0,0]
            cY = int(M["m10"] / M["m00"])
            cX = int(M["m01"] / M["m00"])
        except:
            excepted=True
        # draw the contour and center of the shape on the image
        if excepted:
            cX = int(img.shape[0]*0.7)
            cY = int(img.shape[1]*0.5)
        
        img_center_contours = cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        cv2.circle(img, (cY, cX), 7, (255, 0, 0), -1)
        contour_centroids.append((cX, cY))
        
    # find second lowest positioned contour 
    sorted_centroids = sorted(contour_centroids, key=lambda tup: tup[0], reverse=True)
    
    if len(sorted_centroids)==0:
        cX = int(img.shape[0]*0.7)
        cY = int(img.shape[1]*0.5)
        cv2.circle(img, (cY, cX), 7, (255, 0, 0), -1)

    elif len(sorted_centroids)==1:
        cY, cX = sorted_centroids[0]
    else:
        cY, cX = sorted_centroids[1]
        
    cv2.imwrite(result_dir, img_center_contours)
    print('%s saved' % 'lanes with centroids image')