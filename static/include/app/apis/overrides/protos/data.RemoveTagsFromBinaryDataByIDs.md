# Remove tags from binary data by IDs

Remove tags from binary data identified by their binary data IDs.  

Request:
```protobuf
message RemoveTagsFromBinaryDataByIDsRequest {
  // The tags to remove.
  repeated string tags = 1;
   
  // The binary data IDs to remove tags from.
  repeated string binary_data_ids = 2;
}
```

The tags specified in the request will be removed from the binary data with the given IDs.
