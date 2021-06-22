import pclpy
from pclpy import pcl


def segmentPlane(cloud, path):

    optimize = False
    model = pclpy.pcl.sample_consensus.SACMODEL_PERPENDICULAR_PLANE
    method = pcl.sample_consensus.SAC_RANSAC
    distance = 0.2
    nr_points = cloud.size()
    count = 0
    # compute mls
    while cloud.size() > (0.25 * nr_points):
        pc_type = "PointXYZRGB"
        seg = getattr(pcl.segmentation.SACSegmentation, pc_type)()
        seg.setOptimizeCoefficients(optimize)
        seg.setModelType(model)
        seg.setMethodType(method)
        seg.setDistanceThreshold(distance)
        seg.setInputCloud(cloud)
        coefficients = pcl.ModelCoefficients()
        inliers = pcl.PointIndices()
        seg.segment(inliers, coefficients)

        extract = pcl.filters.ExtractIndices.PointXYZRGB()
        extract.setInputCloud(cloud)
        extract.setIndices(inliers)
        extract.setNegative(False)

        out = pcl.PointCloud.PointXYZRGB()
        extract.filter(out)

        pclpy.write_las(out, path.replace(".las", str(count) + ".las"))
        count = count + 1
        cloud = extract.setNegative(True)
        cloudF = pcl.PointCloud.PointXYZRGB()
        extract.filter(cloudF)
        cloud = cloudF
    print("---------------Done----------------------")
