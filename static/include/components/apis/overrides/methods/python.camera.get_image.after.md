If the `mime_type` of your image is `image/vnd.viam.dep`, pass the returned image data to the Viam Python SDK's [`ViamImage.bytes_to_depth_array()`](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.ViamImage.bytes_to_depth_array) method to decode the raw image data to a standard 2D image representation.

For example:

```python {class="line-numbers linkable-line-numbers"}
# Assume "frame" has a mime_type of "image/vnd.viam.dep"
frame = await my_camera.get_image()

# Convert "frame" to a standard 2D image representation.
# Remove the 1st 3x8 bytes and reshape the raw bytes to List[List[Int]].
standard_frame = frame.bytes_to_depth_array()
```

The Python SDK provides the helper functions `viam_to_pil_image` and `pil_to_viam_image` to decode the `ViamImage` into a [`PIL Image`](https://omz-software.com/pythonista/docs/ios/Image.html) and vice versa.

For example:

```python {class="line-numbers linkable-line-numbers"}
# from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image
# < ADD ABOVE IMPORT TO BEGINNING OF PROGRAM >

# Get the ViamImage from your camera.
frame = await my_camera.get_image()

# Convert "frame" to a PIL Image representation.
pil_frame = viam_to_pil_image(frame)

# Use methods from the PIL Image class to get size.
x, y = pil_frame.size[0], pil_frame.size[1]
# Crop image to get only the left two fifths of the original image.
cropped_pil_frame = pil_frame.crop((0, 0, x / 2.5, y))

# Convert back to ViamImage.
cropped_frame = pil_to_viam_image(cropped_pil_frame)
```

{{% alert title="Tip" color="tip" %}}

Be sure to close the image when finished.

{{% /alert %}}
