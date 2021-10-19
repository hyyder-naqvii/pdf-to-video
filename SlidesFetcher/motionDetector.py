import imutils
from os import path
import cv2


# This function uses the Scene Boundary Transition Detection algorithm


def captureFrames(filename):
    # initialize the background subtractor
    fgbg = cv2.createBackgroundSubtractorMOG2()
    # initialize a boolean used to represent whether or not a given frame
    # has been captured along with two integer counters -- one to count
    # the total number of frames that have been captured and another to
    # count the total number of frames processed
    captured = False
    total = 0
    frames = 0
    capturedFrames = []
    # open a pointer to the video file initialize the width and height of
    # the frame

    vs = cv2.VideoCapture(path.join("videos", filename))
    (W, H) = (None, None)

    # loop over the frames of the video
    while True:
        # grab a frame from the video
        (grabbed, frame) = vs.read()
        # if the frame is None, then we have reached the end of the
        # video file
        if frame is None:
            break
        # clone the original frame (so we can save it later), resize the
        # frame, and then apply the background subtractor
        orig = frame.copy()
        frame = imutils.resize(frame, width=600)
        mask = fgbg.apply(frame)
        # apply a series of erosions and dilations to eliminate noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # if the width and height are empty, grab the spatial dimensions
        if W is None or H is None:
            (H, W) = mask.shape[:2]
        # compute the percentage of the mask that is "foreground"
        p = (cv2.countNonZero(mask) / float(W * H)) * 100

        print("Motion: " + str(int(p)))
        # know that the motion has stopped and thus we should grab the
        # frame
        if p <= 0.0000001 and not captured:
            # show the captured frame and update the captured bookkeeping
            # variable
            cv2.imshow("Captured", frame)
            captured = True
            capturedFrames.append(frame)
            # construct the path to the output frame and increment the
            # total frame counter
            # _filename = "{}.png".format(total)
            # path = os.path.join(fetchedImagesDirectory, _filename)
            # print(path)
            total += 1
            # save the  *original, high resolution* frame to disk
            # print("[INFO] saving {}".format(path))
            # cv2.imwrite(path, orig)
        # otherwise, either the scene is changing or we're still in warmup
        # mode so let's wait until the scene has settled or we're finished
        # building the background model
        elif captured and p > 0.0000012:
            captured = False

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        key = cv2.waitKey(1) & 0xF
        # if the `q` key was pressed, break from the loop

        # increment the frames counter
        frames += 1
    return capturedFrames
