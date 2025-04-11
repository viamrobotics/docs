# Add tags to binary data by IDs

Add tags to binary data identified by their binary data IDs.

Request:
```protobuf
message AddTagsToBinaryDataByIDsRequest {
  // The tags to add.
  repeated string tags = 1;

  // The binary data IDs to add tags to.
  repeated string binary_data_ids = 2;
}
```

The binary data IDs in the request will have the specified tags added to them.
