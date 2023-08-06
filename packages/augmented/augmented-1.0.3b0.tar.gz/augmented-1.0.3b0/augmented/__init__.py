import cv2
import numpy as np
import keyboard
print("""Beta version of ar-python (Copyright (c) 2021, Sarangt123 (Sarang T))
Created by : Sarang T (india,kerala) 
Report bugs and issues at the githubpage
Email : sarangthekkedathpr@gmail.com
Contributers : Sarang""")
"""
Copyright (c) 2021, Sarangt123 (Sarang T)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the augmented-python nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""


class ar():
    def __init__(self, capture: int, targetImage: str, overlayImage: str):
        if not isinstance(capture, int):
            raise TypeError("Expected an int")
        self.capture = capture
        if not isinstance(targetImage, str):
            raise TypeError("Expected a str")
        self.targetImage = targetImage
        if not isinstance(overlayImage, str):
            raise TypeError("Expected a str")
        self.overlayImage = overlayImage
        return None

    def ar_overlay(self, nfeatures: int, debug: bool, confidence: int, displayName: str, exit: str):
        if not isinstance(nfeatures, int):
            raise TypeError('Expected a int')
        if not isinstance(debug, bool):
            raise TypeError
        if not isinstance(confidence, int):
            raise TypeError('Expected an int')
        if not isinstance(displayName, str):
            raise TypeError('Expected a str')
        if not isinstance(displayName, str):
            raise TypeError('Expected a str')
        """
        
        """

        print('Hold exit key upto 10 secs to quit')
        cap = cv2.VideoCapture(self.capture)
        imgTarget = cv2.imread(self.targetImage)
        Overlay = cv2.imread(self.overlayImage)
        self.nfeatures = nfeatures
        imgOverlay = Overlay
        """
        
        """
        """
        """
        height, width, char = imgTarget.shape
        # imgOverlay = cv2.resize(imgOverlay, (height, width))
        """
        
        """
        orb = cv2.ORB_create(nfeatures=nfeatures)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        imgTarget = cv2.drawKeypoints(imgTarget, kp1, None)
        imgAug = []
        while True:
            try:
                success, Webcam = cap.read()
                imgAug = Webcam.copy()
                kp2, des2, = orb.detectAndCompute(Webcam, None)
                Webcam = cv2.drawKeypoints(Webcam, kp1, None)
                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1, des2, k=2)
                good = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append(m)
                if debug:
                    print(len(good))
                imgFeatures = cv2.drawMatches(
                    imgTarget, kp1, Webcam, kp2, good, None, flags=2)
                if len(good) > confidence:
                    srcpt = np.float32(
                        [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                    dstpt = np.float32(
                        [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                    matrix, mask = cv2.findHomography(srcpt, dstpt, cv2.RANSAC, 5)
                    if debug:
                        print(matrix)
                    pts = np.float32([[0, 0], [0, height], [width, height], [
                        width, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, matrix)
                    img2 = cv2.polylines(
                        Webcam, [np.int32(dst)], True, (255, 0, 255), 3)

                    imgWarp = cv2.warpPerspective(
                        imgOverlay, matrix, (Webcam.shape[1], Webcam.shape[0]))
                    maskNew = np.zeros(
                        (Webcam.shape[0], Webcam.shape[1]), np.uint8)
                    cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                    maskInverse = cv2.bitwise_not(maskNew)
                    imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInverse)
                    imgAug = cv2.bitwise_or(imgWarp, imgAug)
                    if debug:
                        cv2.imshow('Debug window', img2)
                        cv2.imshow('Debug window', imgWarp)
                        cv2.imshow('Debug window', maskNew)
                        cv2.imshow('Debug window', mask)
                        cv2.imshow('Debug window', maskInverse)
                if debug:
                    print(len(good))
                    cv2.imshow('Debug window', imgFeatures)

                stacked = np.concatenate((Webcam, imgAug), axis=0)
                cv2.imshow(displayName, stacked)

                cv2.waitKey(0)

                if cv2.waitKey(1) == ord(exit):
                    cap.release()
                    break

                self.cap = cap
            except Exception as e:
                print(e)

    def close(self):
        cap = self.cap()
        cap.release()

    def help(self):
        print('Please check the documentation at the pypi page')
