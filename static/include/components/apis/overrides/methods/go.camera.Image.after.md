You can also directly decode as an `Image.Image` with the camera's `DecodeImageFromCamera` function:

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(machine, "my_camera")
img, err = camera.DecodeImageFromCamera(context.Background(), utils.MimeTypeJPEG, nil, myCamera)
```

If you use this method, be sure to import `"go.viam.com/rdk/utils"` at the beginning of your file.
