<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`CreateDataset`](/reference/apis/data-client/#createdataset) | Create a new dataset. |
| [`DeleteDataset`](/reference/apis/data-client/#deletedataset) | Delete a dataset. |
| [`RenameDataset`](/reference/apis/data-client/#renamedataset) | Rename a dataset specified by the dataset ID. |
| [`ListDatasetsByOrganizationID`](/reference/apis/data-client/#listdatasetsbyorganizationid) | Get the datasets in an organization. |
| [`ListDatasetsByIDs`](/reference/apis/data-client/#listdatasetsbyids) | Get a list of datasets using their IDs. |
| [`StartSequenceDatasetExport`](/reference/apis/data-client/#startsequencedatasetexport) | Start an asynchronous export of a sequence dataset. Returns a job ID to poll with GetSequenceDatasetExport. |
| [`GetSequenceDatasetExport`](/reference/apis/data-client/#getsequencedatasetexport) | Get the status of a sequence dataset export job. When the job completes, the response includes a short-lived URL for downloading a zip of Parquet files. |
