import os
from motionDetector import captureFrames
from fpdf import FPDF


import cv2


def videoToPDF(filename):
    pdf = FPDF("L", "in", "A4")

    fetchedImagesDirectory = os.path.join("slides/", filename.split(".")[0])
    if os.path.exists(fetchedImagesDirectory) == False:

        os.mkdir(fetchedImagesDirectory)
    else:
        for file in os.scandir(fetchedImagesDirectory):
            os.unlink(file.path)

    capturedFrames = captureFrames(filename)

    count = 0
    for frame in capturedFrames:
        cv2.imshow("Frame", frame)

        cv2.imwrite("{}/slide{}.jpg".format(fetchedImagesDirectory, count), frame)
        pdf.add_page()
        pdf.image("{}/slide{}.jpg".format(fetchedImagesDirectory, count))
        os.unlink("{}/slide{}.jpg".format(fetchedImagesDirectory, count))
        count += 1
    pdf.output(
        os.path.join(fetchedImagesDirectory, filename.split(".")[0] + ".pdf"), "F"
    )


videoToPDF("lec1.mp4")
