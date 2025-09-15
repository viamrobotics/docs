<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetLatestTabularData`](/dev/reference/apis/data-client/#getlatesttabulardata) | Gets the most recent tabular data captured from the specified data source, as long as it was synced within the last year. |
| [`ExportTabularData`](/dev/reference/apis/data-client/#exporttabulardata) | Obtain unified tabular data and metadata from the specified data source. |
| [`TabularDataByFilter`](/dev/reference/apis/data-client/#tabulardatabyfilter) | Retrieve optionally filtered tabular data from Viam. |
| [`TabularDataBySQL`](/dev/reference/apis/data-client/#tabulardatabysql) | Obtain unified tabular data and metadata, queried with SQL. Make sure your API key has permissions at the organization level in order to use this. |
| [`TabularDataByMQL`](/dev/reference/apis/data-client/#tabulardatabymql) | Obtain unified tabular data and metadata, queried with MQL. |
| [`BinaryDataByFilter`](/dev/reference/apis/data-client/#binarydatabyfilter) | Retrieve optionally filtered binary data from Viam. |
| [`BinaryDataByIDs`](/dev/reference/apis/data-client/#binarydatabyids) | Retrieve binary data from Viam by `BinaryID`. |
| [`DeleteTabularData`](/dev/reference/apis/data-client/#deletetabulardata) | Delete tabular data older than a specified number of days. |
| [`DeleteBinaryDataByFilter`](/dev/reference/apis/data-client/#deletebinarydatabyfilter) | Filter and delete binary data. |
| [`DeleteBinaryDataByIDs`](/dev/reference/apis/data-client/#deletebinarydatabyids) | Filter and delete binary data by ids. |
| [`AddTagsToBinaryDataByIDs`](/dev/reference/apis/data-client/#addtagstobinarydatabyids) | Add tags to binary data by ids. |
| [`TagsByFilter`](/dev/reference/apis/data-client/#tagsbyfilter) | Get a list of tags using a filter. |
| [`AddBoundingBoxToImageByID`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid) | Add a bounding box to an image specified by its BinaryID. |
| [`RemoveBoundingBoxFromImageByID`](/dev/reference/apis/data-client/#removeboundingboxfromimagebyid) | Removes a bounding box from an image specified by its BinaryID. |
| [`BoundingBoxLabelsByFilter`](/dev/reference/apis/data-client/#boundingboxlabelsbyfilter) | Get a list of bounding box labels using a Filter. |
| [`GetDatabaseConnection`](/dev/reference/apis/data-client/#getdatabaseconnection) | Get a connection to access a MongoDB Atlas Data federation instance. |
| [`ConfigureDatabaseUser`](/dev/reference/apis/data-client/#configuredatabaseuser) | Configure a database user for the Viam organization’s MongoDB Atlas Data Federation instance. |
| [`AddBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids) | Add the `BinaryData` to the provided dataset. |
| [`RemoveBinaryDataFromDatasetByIDs`](/dev/reference/apis/data-client/#removebinarydatafromdatasetbyids) | Remove the BinaryData from the provided dataset. |
| [`GetDataPipeline`](/dev/reference/apis/data-client/#getdatapipeline) | Get the configuration for a data pipeline. |
| [`ListDataPipelines`](/dev/reference/apis/data-client/#listdatapipelines) | List all of the data pipelines in an organization. |
| [`CreateDataPipeline`](/dev/reference/apis/data-client/#createdatapipeline) | Create a data pipeline. |
| [`DeleteDataPipeline`](/dev/reference/apis/data-client/#deletedatapipeline) | Delete a data pipeline, its execution history, and all of its output data. |
| [`ListDataPipelineRuns`](/dev/reference/apis/data-client/#listdatapipelineruns) | Get information about individual executions of a data pipeline. |
| [`RenameDataPipeline`](/dev/reference/apis/data-client/#renamedatapipeline) | Rename a data pipeline. |
