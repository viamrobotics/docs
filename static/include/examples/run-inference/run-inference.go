// :snippet-start: run-inference
package main

import (
	"bytes"
	"context"
	"fmt"
	"image"
	"image/jpeg"

	"gorgonia.org/tensor"
	// :remove-start:
	"os"
	// :remove-end:

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/ml"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/components/camera"
	"go.viam.com/rdk/services/mlmodel"
	"go.viam.com/rdk/utils"
	"go.viam.com/utils/rpc"
)

func main() {
	apiKey := ""
	apiKeyID := ""
	machineAddress := ""
	mlModelName := ""
	cameraName := ""

	// :remove-start:
	apiKey = os.Getenv("VIAM_API_KEY")
	apiKeyID = os.Getenv("VIAM_API_KEY_ID")
	machineAddress = "auto-machine-main.pg5q3j3h95.viam.cloud"
	cameraName = "camera-1"
	mlModelName = "mlmodel-1"
	// :remove-end:

	logger := logging.NewDebugLogger("client")
	ctx := context.Background()

	machine, err := client.New(
		context.Background(),
		machineAddress,
		logger,
		client.WithDialOptions(rpc.WithEntityCredentials(
			apiKeyID,
			rpc.Credentials{
				Type:    rpc.CredentialsTypeAPIKey,
				Payload: apiKey,
			})),
	)
	if err != nil {
		logger.Fatal(err)
	}

	// Capture image from camera
	cam, err := camera.FromRobot(machine, cameraName)
	if err != nil {
		logger.Fatal(err)
	}

	imageData, _, err := cam.Image(ctx, utils.MimeTypeJPEG, nil)
	if err != nil {
		logger.Fatal(err)
	}

	// Decode the image data to get the actual image
	img, err := jpeg.Decode(bytes.NewReader(imageData))
	if err != nil {
		logger.Fatal(err)
	}

	// Get ML model metadata to understand input requirements
	mlModel, err := mlmodel.FromRobot(machine, mlModelName)
	if err != nil {
		logger.Fatal(err)
	}

	metadata, err := mlModel.Metadata(ctx)
	if err != nil {
		logger.Fatal(err)
	}

	// Get expected input shape and type from metadata
	var expectedShape []int
	var expectedDtype tensor.Dtype
	var expectedName string

	if len(metadata.Inputs) > 0 {
		inputInfo := metadata.Inputs[0]
		expectedShape = inputInfo.Shape
		expectedName = inputInfo.Name

		// Convert data type string to tensor.Dtype
		switch inputInfo.DataType {
		case "uint8":
			expectedDtype = tensor.Uint8
		case "float32":
			expectedDtype = tensor.Float32
		default:
			expectedDtype = tensor.Float32 // Default to float32
		}
	} else {
		logger.Fatal("No input info found in model metadata")
	}

	// Resize image to expected dimensions
	bounds := img.Bounds()
	width := bounds.Dx()
	height := bounds.Dy()

	// Extract expected dimensions
	if len(expectedShape) != 4 || expectedShape[0] != 1 || expectedShape[3] != 3 {
		logger.Fatal("Unexpected input shape format")
	}

	expectedHeight := expectedShape[1]
	expectedWidth := expectedShape[2]

	// Create a new image with the expected dimensions
	resizedImg := image.NewRGBA(image.Rect(0, 0, expectedWidth, expectedHeight))

	// Simple nearest neighbor resize
	for y := 0; y < expectedHeight; y++ {
		for x := 0; x < expectedWidth; x++ {
			srcX := x * width / expectedWidth
			srcY := y * height / expectedHeight
			resizedImg.Set(x, y, img.At(srcX, srcY))
		}
	}

	// Convert image to tensor data
	tensorData := make([]float32, 1*expectedHeight*expectedWidth*3)
	idx := 0

	for y := 0; y < expectedHeight; y++ {
		for x := 0; x < expectedWidth; x++ {
			r, g, b, _ := resizedImg.At(x, y).RGBA()

			// Convert from 16-bit to 8-bit and normalize to [0, 1] for float32
			if expectedDtype == tensor.Float32 {
				tensorData[idx] = float32(r>>8) / 255.0   // R
				tensorData[idx+1] = float32(g>>8) / 255.0 // G
				tensorData[idx+2] = float32(b>>8) / 255.0 // B
			} else {
				// For uint8, we need to create a uint8 slice
				logger.Fatal("uint8 tensor creation not implemented in this example")
			}
			idx += 3
		}
	}

	// Create input tensor
	var inputTensor tensor.Tensor
	if expectedDtype == tensor.Float32 {
		inputTensor = tensor.New(
			tensor.WithShape(1, expectedHeight, expectedWidth, 3),
			tensor.WithBacking(tensorData),
			tensor.Of(tensor.Float32),
		)
	} else {
		logger.Fatal("Only float32 tensors are supported in this example")
	}

	// Convert tensor.Tensor to *tensor.Dense for ml.Tensors
	denseTensor, ok := inputTensor.(*tensor.Dense)
	if !ok {
		logger.Fatal("Failed to convert inputTensor to *tensor.Dense")
	}

	inputTensors := ml.Tensors{
		expectedName: denseTensor,
	}

	outputTensors, err := mlModel.Infer(ctx, inputTensors)
	if err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Output tensors: %v\n", outputTensors)

	err = machine.Close(ctx)
	if err != nil {
		logger.Fatal(err)
	}
}
// :snippet-end: