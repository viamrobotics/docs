Upload binary data collected on your machine through a specific component and the relevant metadata to [Viam](https://app.viam.com).
Uploaded binary data can be found under the **Images**, **Point clouds**, or **Files** subtab of the [**Data** tab](https://app.viam.com/data), depending on the type of data that you upload.

{{< alert title="Capture times" color="note" >}}
Viam requires both the time the data was requested and the time it was received (`data_request_times` in Python, `dataRequestTimes` in TypeScript and Flutter), and rejects the upload with an invalid argument error if the received time is more than 24 hours after the requested time.
{{< /alert >}}
