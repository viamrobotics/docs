<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`TabularDataByFilter`](/appendix/apis/data-client/#tabulardatabyfilter) | Filter and download tabular data.
[`BinaryDataByFilter`](/appendix/apis/data-client/#binarydatabyfilter) | Filter and download binary data.
[`BinaryDataByIDs`](/appendix/apis/data-client/#binarydatabyids) | Download binary data by IDs.
[`TabularDataBySQL`](/appendix/apis/data-client/#tabulardatabysql) | Obtain unified tabular data and metadata, queried with SQL.
[`TabularDataByMQL`](/appendix/apis/data-client/#tabulardatabymql) | Obtain unified tabular data and metadata, queried with MQL.
[`DeleteTabularData`](/appendix/apis/data-client/#deletetabulardata) | Delete tabular data older than a specified number of days.
[`DeleteBinaryDataByFilter`](/appendix/apis/data-client/#deletebinarydatabyfilter) | Filter and delete binary data.
[`DeleteBinaryDataByIds`](/appendix/apis/data-client/#deletebinarydatabyids) | Filter and delete binary data by ids.
[`AddTagsToBinaryDataByIds`](/appendix/apis/data-client/#addtagstobinarydatabyids) | Add tags to binary data by ids.
[`AddTagsToBinaryDataByFilter`](/appendix/apis/data-client/#addtagstobinarydatabyfilter) | Add tags to binary data by filter.
[`RemoveTagsFromBinaryDataByIds`](/appendix/apis/data-client/#removetagsfrombinarydatabyids) | Remove tags from binary data by ids.
[`RemoveTagsFromBinaryDataByFilter`](/appendix/apis/data-client/#removetagsfrombinarydatabyfilter) | Remove tags from binary data by filter.
[`TagsByFilter`](/appendix/apis/data-client/#tagsbyfilter) | Get tags from data by filter.
[`BoundingBoxLabelsByFilter`](/appendix/apis/data-client/#boundingboxlabelsbyfilter) | Get a list of bounding box labels using a Filter.
[`GetDatabaseConnection`](/appendix/apis/data-client/#getdatabaseconnection) | Get a connection to access a MongoDB Atlas Data federation instance.
[`BinaryDataCaptureUpload`](/appendix/apis/data-client/#binarydatacaptureupload) | Upload binary data collected on your machine through a specific component and the relevant metadata to the Viam app.
[`TabularDataCaptureUpload`](/appendix/apis/data-client/#tabulardatacaptureupload) | Upload tabular data collected on your machine through a specific component and the relevant metadata to the Viam app.
[`StreamingDataCaptureUpload`](/appendix/apis/data-client/#streamingdatacaptureupload) | Upload the contents of streaming binary data and the relevant metadata to the Viam app.
[`FileUpload`](/appendix/apis/data-client/#fileupload) | Upload file data stored on your machine and the relevant metadata to the Viam app.
[`FileUploadFromPath`](/appendix/apis/data-client/#fileuploadfrompath) | Upload file data stored on your machine from the specified filepath and the relevant metadata to the Viam app.
[`AddBoundingBoxToImageById`](/appendix/apis/data-client/#addboundingboxtoimagebyid) | Add a bounding box to an image specified by its BinaryID.
[`RemoveBoundingBoxFromImageById`](/appendix/apis/data-client/#removeboundingboxfromimagebyid) | Removes a bounding box from an image specified by its BinaryID.
[`CreateDataset`](/appendix/apis/data-client/#createdataset) | Create a new dataset.
[`ListDatasetByIds`](/appendix/apis/data-client/#listdatasetbyids) | Get a list of datasets using their IDs.
[`ListDatasetByOrganizationId`](/appendix/apis/data-client/#listdatasetbyorganizationid) | Get the datasets in an organization.
[`RenameDataset`](/appendix/apis/data-client/#renamedataset) | Rename a dataset specified by the dataset ID.
[`DeleteDataset`](/appendix/apis/data-client/#deletedataset) | Delete a dataset.
[`AddBinaryDataToDatasetByIds`](/appendix/apis/data-client/#addbinarydatatodatasetbyids) | Add the BinaryData to the provided dataset. This BinaryData will be tagged with the VIAM_DATASET_{id} label.
[`RemoveBinaryDataFromDatasetByIds`](/appendix/apis/data-client/#removebinarydatafromdatasetbyids) | Remove the BinaryData from the provided dataset. This BinaryData will lose the VIAM_DATASET_{id} tag.
[`ConfigureDatabaseUser`](/appendix/apis/data-client/#configuredatabaseuser) | Configure a database user for the Viam organization’s MongoDB Atlas Data Federation instance.
