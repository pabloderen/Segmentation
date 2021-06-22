import pclpy
from pclpy import pcl
from random import random
import numpy as np
import os


def splitPointCloud(inputFile, outputFolder, voxelSize):

    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    pts = np.loadtxt(inputFile)

    pts = np.delete(pts, 3, 1)
    pts = np.delete(pts, 3, 1)
    pts = np.delete(pts, 3, 1)

    print(pts[0])
    min = np.amin(pts, axis=0)
    max = np.amax(pts, axis=0)

    X = np.array([x for x in range(int(min[0]), int(max[0]), voxelSize)])
    Y = np.array([x for x in range(int(min[1]), int(max[1]), voxelSize)])
    Z = np.array([x for x in range(int(min[2]), int(max[2]), voxelSize)])

    boundingBoxesMin = []
    for x in X:
        for y in Y:
            for z in Z:
                boundingBoxesMin.append([x, y, z])

    boundingBoxesMin = np.array([np.array(xi) for xi in boundingBoxesMin])

    output = []
    print(boundingBoxesMin[0])
    for bbx in boundingBoxesMin:
        upperbbx = bbx + voxelSize
        condition = np.all(np.logical_and(bbx <= pts, pts <= upperbbx), axis=1)

        b = pts[condition]

        output.append(b)

    for i, e in enumerate(output):
        np.savetxt(
            "{0}/{1}_{2}.txt".format(outputFolder, i, inputFile),
            e,
            delimiter=" ",
            fmt="%1.3f",
        )
