<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`TabularDataByFilter`](/build/program/apis/data-client/#tabulardatabyfilter) | Filter and download tabular data.
[`BinaryDataByFilter`](/build/program/apis/data-client/#binarydatabyfilter) | Filter and download binary data.
[`BinaryDataByIDs`](/build/program/apis/data-client/#binarydatabyids) | Download binary data by IDs.
[`DeleteTabularData`](/build/program/apis/data-client/#deletetabulardata) | Delete tabular data older than a specified number of days.
[`DeleteBinaryDataByFilter`](/build/program/apis/data-client/#deletebinarydatabyfilter) | Filter and delete binary data.
[`DeleteBinaryDataByIds`](/build/program/apis/data-client/#deletebinarydatabyids) | Filter and delete binary data by ids.
[`AddTagsToBinaryDataByIds`](/build/program/apis/data-client/#addtagstobinarydatabyids) | Add tags to binary data by ids.
[`AddTagsToBinaryDataByFilter`](/build/program/apis/data-client/#addtagstobinarydatabyfilter) | Add tags to binary data by filter.
[`RemoveTagsFromBinaryDataByIds`](/build/program/apis/data-client/#removetagsfrombinarydatabyids) | Remove tags from binary data by ids.
[`RemoveTagsFromBinaryDataByFilter`](/build/program/apis/data-client/#removetagsfrombinarydatabyfilter) | Remove tags from binary data by filter.
[`TagsByFilter`](/build/program/apis/data-client/#tagsbyfilter) | Get tags from data by filter.
[`BoundingBoxLabelsByFilter`](/build/program/apis/data-client/#boundingboxlabelsbyfilter) | Get a list of bounding box labels using a Filter.
[`GetDatabaseConnection`](/build/program/apis/data-client/#getdatabaseconnection) | Get a connection to access a MongoDB Atlas Data federation instance.
[`BinaryDataCaptureUpload`](/build/program/apis/data-client/#binarydatacaptureupload) | Upload binary data collected on your machine through a specific component and the relevant metadata to the Viam app.
[`TabularDataCaptureUpload`](/build/program/apis/data-client/#tabulardatacaptureupload) | Upload tabular data collected on your machine through a specific component and the relevant metadata to the Viam app.
[`StreamingDataCaptureUpload`](/build/program/apis/data-client/#streamingdatacaptureupload) | Upload the contents of streaming binary data and the relevant metadata to the Viam app.
[`FileUpload`](/build/program/apis/data-client/#fileupload) | Upload file data stored on your machine and the relevant metadata to the Viam app.
[`FileUploadFromPath`](/build/program/apis/data-client/#fileuploadfrompath) | Upload file data stored on your machine from the specified filepath and the relevant metadata to the Viam app.
[`AddBoundingBoxToImageById`](/build/program/apis/data-client/#addboundingboxtoimagebyid) | Add a bounding box to an image specified by its BinaryID.
[`RemoveBoundingBoxFromImageById`](/build/program/apis/data-client/#removeboundingboxfromimagebyid) | Removes a bounding box from an image specified by its BinaryID.
[`CreateDataset`](/build/program/apis/data-client/#createdataset) | Create a new dataset.
[`ListDatasetByIds`](/build/program/apis/data-client/#listdatasetbyids) | Get a list of datasets using their IDs.
[`ListDatasetByOrganizationId`](/build/program/apis/data-client/#listdatasetbyorganizationid) | Get the datasets in an organization. 
[`RenameDataset`](/build/program/apis/data-client/#renamedataset) | Rename a dataset specified by the dataset ID.
[`DeleteDataset`](/build/program/apis/data-client/#deletedataset) | Delete a dataset.
[`AddBinaryDataToDatasetByIds`](/build/program/apis/data-client/#addbinarydatatodatasetbyids) | Add the BinaryData to the provided dataset. This BinaryData will be tagged with the VIAM_DATASET_{id} label.
[`RemoveBinaryDataFromDatasetByIds`](/build/program/apis/data-client/#removebinarydatafromdatasetbyids) | Remove the BinaryData from the provided dataset. This BinaryData will lose the VIAM_DATASET_{id} tag.
