---
title: Camera Component Documentation
summary: Explanation of camera types, configuration, and usage in Viam.
authors:
    - Matt Dannenberg
date: 2022-05-19
---
# Camera Models

## Transform Model

The Transform Model creates a pipeline for applying transformations to an input image source. 
Transformations get applied in the order they are written in the pipeline. 
Below are the available transformations, and the attributes they need.

**Example**: 
```json
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
## Identity

The Identity transform does nothing to the image. 
You can use this transform to change the underlying camera source's intrinsic parameters or stream type, for example.

```json
{
	"type": "identity",
	"attributes": {
		# no attributes
	}
}
```

## Rotate

The Rotate trasnformation rotates the image by 180 degrees. 
This feature is useful for when the camera is installed upside down on your robot. 

```json
{
	"type": "rotate",
	"attributes": {
		# no attributes
	}
}
```

## Resize

The Resize transform resizes the image to the specified height and width. 

```json
{
	"type": "rotate",
	"attributes": {
		"width": int, 
		"height": int
	}
}
```
## Depth to Pretty

The Depth-to-Pretty transform takes a depth image and turns into a colorful image, with blue indicating distant points and red indicating points nearby points. 
Actual depth information is lost in the transform.

```json
{
	"type": "depth_to_pretty",
	"attributes": {
		# no attributes
	}
}
```

#### Overlay

Overlay overlays the depth and color 2D images. Useful in order to debug the alignment of the two images.

```
{
	"type": "overlay",
	"attributes": {
		# no attributes
	}
}
```

## Undistort

The Undistort transform undistorts the input image according to the intrinsics and distortion parameters specified within the camera parameters. 
Currently only supports a Brown-Conrady model of distortion (25 August 2022). 
For further information, pklease refer to the [OpenCV docs](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a).

```json
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

## Detections

The Detections tramsform takes the input image and overlays the detections from a given detector present within the vision service.

```json
{
	"type": "detections",
	"attributes": {
		"detector_name": string, # the name within the vision service
		"confidence_threshold": float # only display detections above threshold
	}
}
```json

#### depth edges

The Depth Edges transform creates a canny edge detector to detect edges on an input depth map.

```json
{
	"type": "depth_edges",
	"attributes": {
		"high_threshold": float, # between 0.0 - 1.0
		"low_threshold": float, # between 0.0 - 1.0
		"blur_radius": float # smooth image before applying filter 
	}
}
```

## Depth Preprocess

Depth Preprocessing applies some basic hole-filling and edge smoothing to a depth map

```json
{
	"type": "depth_preprocess",
	"attributes": {
		# no attributes
	}
}
```
