<!-- prettier-ignore -->
| Method Name | Description | micro-RDK Support |
| ----------- | ----------- | ----------------- |
| [`GetPosition`](/components/encoder/#getposition) | Get the current position of the encoder in ticks or degrees. | Yes |
| [`ResetPosition`](/components/encoder/#resetposition) | Set the current position of the encoder to be the new zero position. | Yes |
| [`GetProperties`](/components/encoder/#getproperties) | Get a list of all the position types that are supported by a given encoder. | Yes |
| [`GetGeometries`](/components/encoder/#getgeometries) | Get all the geometries associated with the encoder in its current configuration, in the frame of the encoder. | No |
| [`Reconfigure`](/components/encoder/#reconfigure) | Reconfigure this resource. | No |
| [`DoCommand`](/components/encoder/#docommand) | Execute model-specific commands that are not otherwise defined by the component API. | Yes |
| [`GetResourceName`](/components/encoder/#getresourcename) | Get the `ResourceName` for this encoder with the given name. | No |
| [`Close`](/components/encoder/#close) | Safely shut down the resource and prevent further use. | No |
