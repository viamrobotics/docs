<!-- prettier-ignore -->
Method Name | Description
----------- | -----------
[`TabularDataByFilter`](/program/apis/data-client/#tabulardatabyfilter) | Filter and download tabular data.
[`BinaryDataByFilter`](/program/apis/data-client/#binarydatabyfilter) | Filter and download binary data.
[`BinaryDataByIDs`](/program/apis/data-client/#binarydatabyids) | Download binary data by IDs.
[`TabularDataBySQL`](/program/apis/data-client/#tabulardatabysql) | Obtain unified tabular data and metadata, queried with SQL.
[`TabularDataByMQL`](/program/apis/data-client/#tabulardatabymql) | Obtain unified tabular data and metadata, queried with MQL.
[`DeleteTabularData`](/program/apis/data-client/#deletetabulardata) | Delete tabular data older than a specified number of days.
[`DeleteBinaryDataByFilter`](/program/apis/data-client/#deletebinarydatabyfilter) | Filter and delete binary data.
[`DeleteBinaryDataByIds`](/program/apis/data-client/#deletebinarydatabyids) | Filter and delete binary data by ids.
[`AddTagsToBinaryDataByIds`](/program/apis/data-client/#addtagstobinarydatabyids) | Add tags to binary data by ids.
[`AddTagsToBinaryDataByFilter`](/program/apis/data-client/#addtagstobinarydatabyfilter) | Add tags to binary data by filter.
[`RemoveTagsFromBinaryDataByIds`](/program/apis/data-client/#removetagsfrombinarydatabyids) | Remove tags from binary data by ids.
[`RemoveTagsFromBinaryDataByFilter`](/program/apis/data-client/#removetagsfrombinarydatabyfilter) | Remove tags from binary data by filter.
[`TagsByFilter`](/program/apis/data-client/#tagsbyfilter) | Get tags from data by filter.
[`BoundingBoxLabelsByFilter`](/program/apis/data-client/#boundingboxlabelsbyfilter) | Get a list of bounding box labels using a Filter.
[`GetDatabaseConnection`](/program/apis/data-client/#getdatabaseconnection) | Get a connection to access a MongoDB Atlas Data federation instance.
[`BinaryDataCaptureUpload`](/program/apis/data-client/#binarydatacaptureupload) | Upload binary data collected on your machine through a specific component and the relevant metadata to the Viam app.
[`TabularDataCaptureUpload`](/program/apis/data-client/#tabulardatacaptureupload) | Upload tabular data collected on your machine through a specific component and the relevant metadata to the Viam app.
[`StreamingDataCaptureUpload`](/program/apis/data-client/#streamingdatacaptureupload) | Upload the contents of streaming binary data and the relevant metadata to the Viam app.
[`FileUpload`](/program/apis/data-client/#fileupload) | Upload file data stored on your machine and the relevant metadata to the Viam app.
[`FileUploadFromPath`](/program/apis/data-client/#fileuploadfrompath) | Upload file data stored on your machine from the specified filepath and the relevant metadata to the Viam app.
[`AddBoundingBoxToImageById`](/program/apis/data-client/#addboundingboxtoimagebyid) | Add a bounding box to an image specified by its BinaryID.
[`RemoveBoundingBoxFromImageById`](/program/apis/data-client/#removeboundingboxfromimagebyid) | Removes a bounding box from an image specified by its BinaryID.
[`CreateDataset`](/program/apis/data-client/#createdataset) | Create a new dataset.
[`ListDatasetByIds`](/program/apis/data-client/#listdatasetbyids) | Get a list of datasets using their IDs.
[`ListDatasetByOrganizationId`](/program/apis/data-client/#listdatasetbyorganizationid) | Get the datasets in an organization.
[`RenameDataset`](/program/apis/data-client/#renamedataset) | Rename a dataset specified by the dataset ID.
[`DeleteDataset`](/program/apis/data-client/#deletedataset) | Delete a dataset.
[`AddBinaryDataToDatasetByIds`](/program/apis/data-client/#addbinarydatatodatasetbyids) | Add the BinaryData to the provided dataset. This BinaryData will be tagged with the VIAM_DATASET_{id} label.
[`RemoveBinaryDataFromDatasetByIds`](/program/apis/data-client/#removebinarydatafromdatasetbyids) | Remove the BinaryData from the provided dataset. This BinaryData will lose the VIAM_DATASET_{id} tag.
[`ConfigureDatabaseUser`](/program/apis/data-client/#configuredatabaseuser) | Configure a database user for the Viam organization’s MongoDB Atlas Data Federation instance.
