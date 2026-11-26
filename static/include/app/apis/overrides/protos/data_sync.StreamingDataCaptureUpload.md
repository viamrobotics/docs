Upload the contents of streaming binary data and the relevant metadata to [Viam](https://app.viam.com).
Uploaded streaming data can be found under the [**Data** tab](https://app.viam.com/data).

{{< alert title="Capture times" color="note" >}}
Viam requires both the time the data was requested and the time it was received (`data_request_times` in Python, `dataRequestTimes` in TypeScript and Flutter), and rejects the upload with an invalid argument error if the received time is more than 24 hours after the requested time.
{{< /alert >}}
