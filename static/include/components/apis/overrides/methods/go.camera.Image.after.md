You can also try to directly decode as an `Image.Image` with the camera's `DecodeImageFromCamera` function:

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromProvider(machine, "my_camera")
img, err = camera.DecodeImageFromCamera(context.Background(), utils.MimeTypeJPEG, nil, myCamera)
```

To use either method, be sure to import `"go.viam.com/rdk/utils"` at the beginning of your file.
