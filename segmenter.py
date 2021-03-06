import pclpy
from pclpy import pcl
import random
import logging
import os
import numpy as np
import split
import plane
import subprocess
import glob
import time


os.remove("./debug.log")
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r << 16 | g << 8 | b


# read a las file
logging.info("reading cloud")

fileName = "wall.pts"
folderName = "wall"
clusterFolder = "Cluster"

split.splitPointCloud(fileName, folderName, 3)


for i, f in enumerate(glob.glob("{0}/*.txt".format(folderName))):

    a = np.loadtxt(f)
    # addin rgb placeholders
    r = random.randint(0, 255)
    time.sleep(0.0001)
    g = random.randint(0, 255)
    time.sleep(0.0001)
    b = random.randint(0, 255)
    rgbarray = (
        np.repeat(np.array([r, g, b]), len(a), axis=0,).astype("u1").reshape(-1, 3)
    )
    clusterName = os.path.splitext(os.path.basename(f))[0]
    cloud = pcl.PointCloud.PointXYZRGB.from_array(a, rgbarray)

    logging.info("starting clustering")
    segmentName = "{0}/{1}_{2}.las".format(clusterFolder, i, clusterName)
    plane.segmentPlane(cloud, segmentName)


##################DEBUG###################
command = "/snap/bin/cloudcompare.ccViewer "
dir_path = os.path.dirname(os.path.realpath(__file__))
for f in glob.glob("{0}/*.las".format(clusterFolder)):
    command = command + dir_path + "/" + f + " "

debug = open("debug.sh", "w")
debug.write(command)
debug.close()

subprocess.run(["bash", dir_path + "/debug.sh"])
