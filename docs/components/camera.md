---
title: Camera Component Documentation
summary: Explanation of camera types, configuration, and usage in Viam.
authors:
    - Matt Dannenberg
date: 2022-05-19
---
# Coming soon!
This will look similar to the [motor doc](motor.md), but describing how to wire up and configure a camera and our virtual cameras which modify video streams.


## Camera Models

### Transform Model

Create a pipeline for applying transformations to an input image source. transformations get applied in the order they are written in the pipeline. Below are the available transformations, and the attributes they need.

example: 

```
{
	"name": "camera_name",
	"type": "camera",
	"model": "transform",
	"attributes" : {
		"source" : "physical_cam",
		"stream" : "color", # or depth
		"pipeline": [
			{ "type": "rotate", "attributes": {} },
			{ "type": "resize". "attributes": {"width":200, "height" 100} }
		]
	}
}
```
#### identity


The identity transform. Does nothing to the image. You can use this if you want to change the underlying camera source's intrinsic parameters or stream type, for example.

```
{
	"type": "identity",
	"attributes": {
		# no attributes
	}
}
```

#### rotate

Rotates the image by 180 degrees. Useful for when you camera is installed upside down on your robot. 

```
{
	"type": "rotate",
	"attributes": {
		# no attributes
	}
}
```

#### resize

Resizes the image to the specified height and width. 

```
{
	"type": "rotate",
	"attributes": {
		"width": int, 
		"height": int
	}
}
```

#### depth to pretty

Depth-to-Pretty takes a depth image and turns into a colorful image, with blue being points that are far away, and red being points that are close by. Actual depth information is lost in the transform.

```
{
	"type": "depth_to_pretty",
	"attributes": {
		# no attributes
	}
}
```

#### overlay

Overlay overlays the depth and color 2D images. Useful in order to debug the alignment of the two images.

```
{
	"type": "overlay",
	"attributes": {
		# no attributes
	}
}
```

#### undistort

Undistort will undistort the input image according to the intrinsics and distortion parameters specified within the camera parameters. Currently only supports a Brown-Conrady model of distortion. More information within the [OpenCV docs here](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a).

```
{
	"type": "undistort",
	"attributes": {
		"camera_parameters": {
			"width": int,
			"height": int,
			"ppx": float, # the image center x point
			"ppy": float, # the image center y point
			"fx": float, # the image focal x
			"fy": float, # the image focal y
			"distortion": {
				"rk1": float, # radial distortion
				"rk2": float,
				"rk3": float,
				"tp1": float, # tangential distortion
				"tp2": float
			}
		}
	}
}
```

#### detections

Detections takes the input imageand overlays the detections from a given detector present within the vision service.

```
{
	"type": "detections",
	"attributes": {
		"detector_name": string, # the name within the vision service
		"confidence_threshold": float # only display detections above threshold
	}
}
```

#### depth edges

Depth Edges creates a canny edge detector to detect edges on an input depth map.

```
{
	"type": "depth_edges",
	"attributes": {
		"high_threshold": float, # between 0.0 - 1.0
		"low_threshold": float, # between 0.0 - 1.0
		"blur_radius": float # smooth image before applying filter 
	}
}
```

#### depth preprocess

Depth Preprocessing applies some basic hole-filling and edge smoothing to a depth map

```
{
	"type": "depth_preprocess",
	"attributes": {
		# no attributes
	}
}
```
