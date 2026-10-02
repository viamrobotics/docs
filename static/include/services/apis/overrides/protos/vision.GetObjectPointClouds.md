Get a list of 3D point cloud objects and associated metadata in the latest picture from a 3D camera (using a specified [segmenter](/reference/apis/services/vision/#segmentations)).

Objects come back in the frame of the camera that was read, with geometry centers in millimeters and point clouds in meters. Convert a center to another frame with the machine client's `TransformPose`.
