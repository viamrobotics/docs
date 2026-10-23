Collect tags from binary data with [`BinaryDataByFilter`](/reference/apis/data-client/#binarydatabyfilter), and from tabular data with [`TabularDataByMQL`](/reference/apis/data-client/#tabulardatabymql).
`TagsByFilter` returns the unique tags from both.
For binary data, read each result's `metadata.capture_metadata.tags`.
For tabular data, query the `tags` field of the [`readings` table](/data/schema/).
