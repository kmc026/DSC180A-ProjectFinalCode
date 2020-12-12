#### Autonomous Vehicles Team 5 Computer Vision and ROS Package

Ka Ming Chan
Evan Kim
Joseph Fallon

This package includes the code for both the image processing for path finding on a lane, as well as the ROS code which commands the autonomous vehicle. The ROS code can not be run, while the image processing using OpenCV can. Therefore, run.py will be only executing the modified code for the image processing. The results will go into the directory test/testresults, as output images, to demonstrate our understanding of using computer vision to navigate our robot. Both ai_drive.py and lane_utils.py inside the src folder plainly serve as the demonstration of our group's process, and do not get run in run.py. For a detailed explanation of the code for image processing, access the Jupyter notebook.

The test image data are captured by our robot assembly in the UCSD tent. They are pictures of the track which simulates a race track. 

If the input target is "test", the images for both lane detection and the path of centroids are created inside the directory test/testresults. If the target is "lane", the result image is only the detected lane. If the target is "centroids", the result image is the detected lane with the found centroids plotted on them.