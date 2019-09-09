import sys
import dlib
import cv2 as cv


# Detectorul => asta trebuie antrenat --> aici folosit din dlib
detector = dlib.get_frontal_face_detector()


print("[INFO] camera sensor warming up...")
vs = VideoStream().start()
time.sleep(2.0)

for f in sys.argv[1:]:
    print("Processing file: {}".format(f))
    image = cv.imread(f)
    img = dlib.load_rgb_image(f)

    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    dets = detector(img, 2)
    for k, d in enumerate(dets):
        x = d.left()
        y = d.top()
        w = d.right()
        h = d.bottom()
        # print ("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(k, d.left(), x, y, w, h))
        cv.rectangle(image, (x,y), (w,h), (255, 0, 0), 2)
    while(1):
        cv.imshow('image', image)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

cv.destroyAllWindows()
    # dlib.hit_enter_to_continue()
