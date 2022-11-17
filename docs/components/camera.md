---
title: "Camera Component"
linkTitle: "Camera"
weight: 40
type: "docs"
description: "Explanation of camera configuration and usage in Viam."
# SMEs: Bijan, Maxim
---
A Viam Camera is a source of 2D and/or 3D images (e.g. a webcam, lidar, time-of-flight sensor, etc). A single image is returned from the camera upon request, and images can be streamed continuously from the camera by using systems that do fast, repeated requests. 

There are two basic things you can do with a camera component:

1. Request the next Image (which is a 2D Color(RGB), or Depth(Z) image).
	* A 2D image always has its x,y units in pixels. For Color, the pixel value is a RGB value, and for Depth it is a uint16 representing depth in mm.
2. Request the next Point Cloud (which is a 3D image)
	* A 3D point cloud has all of its (x,y,z) coordinates in units of mm.


## Camera Models

Here are details about each of the fields in the camera config:

* **Type** is the component type, which will always be "camera".
* **Name** is the name of the component. 
* **Model** is how the component will be set up. Some model types are for setting up physical cameras where images and point clouds originate, some are for combining streams from multiple cameras into one, and the `transform` model is for transforming and processing images.
* **Attributes** are the details that the model requires to work. What attributes are required depends on the model selected. There are some common attributes that can be attached to all camera models.
    * `stream`: this can be either "color" or "depth" and specifies which kind of image should be returned from the camera stream.  
    * `debug`: "true" or "false", and enables the debug outputs from the camera.
    * `intrinsic_parameters` : these are the intrinsic parameters of the camera used to do 2D <-> 3D projections.
    * `distortion_parameters` : these are modified Brown-Conrady parameters used to correct for distortions caused by the shape of the camera lens.

```json-viam
"intrinsic_parameters": { # optional field, intrinsic parameters for 2D <-> transforms
    "height_px": 720, # height of the image in pixels
    "width_px": 1280, # width of the image in pixels
    "fx": 900.538000, # focal length in pixels, x direction
    "fy": 900.818000, # focal length in pixels, y direction
    "ppx": 648.934000, # x center point in pixels
    "ppy": 367.736000 # y center point in pixels
}
"distortion_parameters": {  # optional field, distortion parameters
    "rk1": 0.158701,
    "rk2": -0.485405,
    "rk3": 0.435342,
    "tp1": -0.00143327,
    "tp2": -0.000705919
}
```

Follow the instructions for <a href="https://github.com/viam-labs/camera-calibration" target="_blank">camera calibration</a>[^cc] to calibrate a camera and extract the `intrinsic_parameters` and `distortion_parameters`.
[^cc]: Camera calibration: <a href="https://github.com/viam-labs/camera-calibration" target="_blank">ht<span></span>tps://github.com/viam-labs/camera-calibration</a>

### Webcam

`webcam` is a model that streams the camera data from a camera connected to the hardware. The discovery service will help set up this model, usually.

{{% alert title="Note" color="note"%}}
In Viam parlance, webcams are standard, USB camera devices. 

Viam recommends using a standard webcam rather than a "ribbon" cam (typical a bare camera with a ribbon and connector for mating to a Pi) as they can be very unreliable.
{{% /alert %}}

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "webcam",
	"attributes": {
    	"video_path": string, # path to the webcam,
    	"video_path_pattern": string, # if path is not provided, queries the devices on hardware to find the camera,
    	"width_px": int, # camera image width, used with path_pattern to find camera,
    	"height_px": int, # camera image height, used with path_pattern to find camera,
    	"format": string # image format, used with path_pattern to find camera,
	}
}
```
### Fake

Fake is a fake camera that always returns the same image, which is an image of a chess board. This camera also returns a point cloud.

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "fake",
	"attributes": {}
}
```
### File

File is a model where the frames for the color and depth images are acquired from a file path. Either file path is optional.

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "dual_stream",
	"attributes": {
    	"color": string, # the file path to the color image,
    	"depth": string # the file path to the depth image,
	}
}
```

### Velodyne
 
The model for using the velodyne lidar. The velodyne must be running locally at address `0.0.0.0`. 

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "velodyne",
	"attributes": {
    	"port": int,  
    	"ttl_ms": int,
	}
}
```

### FFmpeg

FFmpeg is a model that allows you to use a video file or stream as a camera.

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "ffmpeg",
	"attributes": {
		"video_path": string,
		"filters": [ # optional
			{
				"name": string,
				"args": [string, string, ..],
				"kw_args": { ... }
			}	
		],
		"input_kw_args": { ... },
		"output_kw_args": { ... },
	}
}
```


### Align Color Depth

Model "align_color_depth" is if you have registered a color and depth camera already in your config, and want to align them after the fact and create a "third" camera that outputs the aligned image. In this case, rather than putting the URLs to each of the cameras, you just put the names of the color and depth camera in the attribute field, and the "align_color_depth" camera will combine the streams from both of them.  You can specify the intrinsics/extrinsics, or homography parameters to do the alignment between the depth and color frames if they need to be shifted somehow. If they don’t need to be aligned, you can leave those parameters blank. You then specify the stream field to specify which aligned picture you want to stream.

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "align_color_depth",
	"attributes": {
    	"stream": string, # either "color" or "depth" to specify the output stream
    	"color_camera_name": string, # the color camera's name
    	"depth_camera_name": string, # the depth camera's name
    	"width_px": int, # the expected width of the aligned pic
    	"height_px": int, # the expected height of the aligned pic
    	"intrinsic_parameters": {...}, # for projecting RGBD images to 2D <-> 3D 
    	"intrinsic_extrinsic": {}, # the intrinsic/extrinsic parameters that relate the two cameras together in order to align the images.
    	"homography": {} # homography parameters that morph the depth points to overlay the color points and align the images.
	}
}
```

### Join Pointclouds

Combine the point clouds from multiple camera sources and project them to be from the point of view of target_frame

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "join_pointclouds",
	"attributes": {
    	"source_cameras": ["cam1", "cam2", "cam3"], # camera sources to combine
    	"target_frame": "arm1", # the frame of reference for the points in the merged point cloud.
    	"merge_method": "", # [opt] either "naive" or "icp"; defaults to "naive".
    	"closeness_mm": 1 # [opt] defines how close 2 points should be together to be considered the same point when merged.
	}
}
```

### Transform 

The Transform model creates a pipeline for applying transformations to an input image source. 
Transformations get applied in the order they are written in the pipeline. 
Below are the available transformations, and the attributes they need.

**Example**: 
```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model": "transform",
	"attributes" : {
		"source" : "physical_cam",
		"stream" : "color", # or depth
		"pipeline": [
			{ "type": "rotate", "attributes": {} },
			{ "type": "resize", "attributes": {"width_px":200, "height_px" 100} }
		]
	}
}
```
##### _Identity_

The Identity transform does nothing to the image. 
You can use this transform to change the underlying camera source's intrinsic parameters or stream type, for example.

```json-viam
{
	"type": "identity",
	"attributes": {
		# no attributes
	}
}
```

##### _Rotate_

The Rotate transformation rotates the image by 180 degrees. 
This feature is useful for when the camera is installed upside down on your robot. 

```json-viam
{
	"type": "rotate",
	"attributes": {
		# no attributes
	}
}
```

##### _Resize_

The Resize transform resizes the image to the specified height and width. 

```json-viam
{
	"type": "resize",
	"attributes": {
		"width_px": int, 
		"height_px": int
	}
}
```
##### _Depth to Pretty_

The Depth-to-Pretty transform takes a depth image and turns it into a colorful image, with blue indicating distant points and red indicating nearby points. 
Actual depth information is lost in the transform.

```json-viam
{
	"type": "depth_to_pretty",
	"attributes": {
		# no attributes
	}
}
```

##### _Overlay_

Overlay overlays the depth and color 2D images. Useful in order to debug the alignment of the two images.

```json-viam
{
	"type": "overlay",
	"attributes": {
		"intrinsic_parameters": {
			"width_px": int,
			"height_px": int,
			"ppx": float, # the image center x point
			"ppy": float, # the image center y point
			"fx": float, # the image focal x
			"fy": float, # the image focal y
        }
	}
}
```

##### _Undistort_

The Undistort transform undistorts the input image according to the intrinsics and distortion parameters specified within the camera parameters. 
Currently only supports a Brown-Conrady model of distortion (20 September 2022). 
For further information, please refer to the <a href="https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a" target="_blank">OpenCV docs[^ocvd].
[^ocvd]: OpenCV docs: <a href="https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a" target="_blank">ht<span></span>tps://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a</a>

```json-viam
{
	"type": "undistort",
	"attributes": {
		"intrinsic_parameters": {
			"width_px": int,
			"height_px": int,
			"ppx": float, # the image center x point
			"ppy": float, # the image center y point
			"fx": float, # the image focal x
			"fy": float, # the image focal y
        },
        "distortion_parameters": {
            "rk1": float, # radial distortion
            "rk2": float,
            "rk3": float,
            "tp1": float, # tangential distortion
            "tp2": float
		}
	}
}
```

##### _Detections_

The Detections transform takes the input image and overlays the detections from a given detector present within the vision service.

```json-viam
{
	"type": "detections",
	"attributes": {
		"detector_name": string, # the name within the vision service
		"confidence_threshold": float # only display detections above threshold
	}
}
```

##### _Depth Edges_

The Depth Edges transform creates a canny edge detector to detect edges on an input depth map.

```json-viam
{
	"type": "depth_edges",
	"attributes": {
		"high_threshold_pct": float, # between 0.0 - 1.0
		"low_threshold_pct": float, # between 0.0 - 1.0
		"blur_radius_px": float # smooth image before applying filter 
	}
}
```

##### _Depth Preprocess_

Depth Preprocessing applies some basic hole-filling and edge smoothing to a depth map

```json-viam
{
	"type": "depth_preprocess",
	"attributes": {
		# no attributes
	}
}
```


### HTTP server cameras

If you have an http endpoint that is streaming images, you can create a VIAM camera from that URL. If you want to create a camera for 2D images, use a `single_stream` server. If you have two endpoints, one for color images and one for depth images, you can use `dual_stream` so that you can also directly generate point clouds.

#### Single Stream

single_stream is a model where there is a camera server streaming image data. You must specify if it is streaming "color", "depth" data. Single_stream can only output a point cloud if a "depth" stream is selected. Color streams will fail at producing point clouds.

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "single_stream",
	"attributes": {
    	"url": string # the camera server url,
    	"stream": string # options are "color", "depth",
	}
}
```

#### Dual Stream

dual_stream is a model where there are two camera servers streaming data, one is the color stream, and the other is the depth stream. This is useful for generating colorful point clouds.

```json-viam
{
	"name": "camera_name",
	"type": "camera",
	"model" : "dual_stream",
	"attributes": {
    	"color": string, # the color stream url,
    	"depth": string, # the depth stream url,
    	"stream": string # "color" or "depth" image will be returned when calling Next(). NextPointCloud() returns the full colorful point cloud.
	}
}
```

## Camera Servers

If you have a camera that uses its own SDK to access its images and point clouds (e.g. an Intel RealSense camera), you can attach a camera server as a remote component to your robot. These remote cameras will show up just like regular cameras on your robot.

For more details, check out [this link to our camera server repository](https://github.com/viamrobotics/camera-servers).

## Troubleshooting

If you are getting "timeout" errors from GRPC when adding a `webcam` model, make sure the webcam port is enabled on the Pi (common if you are using a fresh Pi right out of the box): 

```
$ sudo raspi-config
Interface Options -> Camera -> Enable Camera
Restart the Pi
```

## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/camera/index.html)
