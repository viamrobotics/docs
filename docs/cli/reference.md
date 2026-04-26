---
title: "CLI reference"
linkTitle: "CLI reference"
weight: 90
type: "docs"
description: "Complete command reference for the Viam CLI: every command, subcommand, flag, and alias."
date: "2026-04-25"
# updated: ""  # When the content was last entirely checked
---

This page documents every command, subcommand, flag, and alias in the Viam CLI.
For installation, authentication, and task-oriented guides, see the [Viam CLI overview](/cli/overview/).

All commands use this format:

```sh {class="command-line" data-prompt="$"}
viam [global options] command [command options] [arguments...]
```

You can pass global options after the `viam` CLI keyword with any command.

<!-- prettier-ignore -->
| Global option | Description |
| ------------- | ----------- |
| `--debug` | Enable debug logging. Default: `false`. |
| `--disable-profiles`, `disable-profile` | Disable usage of [profiles](#profiles), falling back to default (false) behavior. Default: `false`. |
| `--help`, `-h` | Show help. Default: `false`. |
| `--profile` | Specify a particular [profile](#profiles) for the current command. |
| `--quiet`, `-q` | Suppress warnings. Default: `false` |

## `data`

The `data` command allows you to manage machine data.
With it, you can export data in a variety of formats, delete data, add or remove tags from all data that matches a given filter, or configure a database user to enable querying synced data directly in the cloud.

```sh {class="command-line" data-prompt="$"}
viam data export binary filter --destination=<output path> [...named args]
viam data export binary ids --destination=<output path> [...named args]
viam data export tabular --destination=<destination> --part-id=<part-id> --resource-name=<resource-name> --resource-subtype=<resource-subtype> --method=<method> [other options]
viam data delete binary --org-ids=<org-ids> --start=<timestamp> --end=<timestamp> [...named args]
viam data delete tabular --org-id=<org-id> --delete-older-than-days=<N>
viam data database configure --org-id=<org-id> --password=<db-user-password>
viam data database hostname --org-id=<org-id>
viam data tag ids add --tags=<tags> --binary-data-ids=<binary_ids>
viam data tag ids remove --tags=<tags> --binary-data-ids=<binary_ids>
viam data tag filter add --tags=<tags> [...named args from filter]
viam data tag filter remove --tags=<tags> [...named args from filter]
viam data index create --collection-type=<type> --index-path=<file> [--org-id=<org-id>] [--pipeline-name=<name>]
viam data index delete --collection-type=<type> --index-name=<name> [--org-id=<org-id>] [--pipeline-name=<name>]
viam data index list --collection-type=<type> [--org-id=<org-id>]
```

### `data export tabular`

Export tabular or sensor data to a specified location in the <file>.ndjson</file> output format. You can copy this from the UI with a filter. See [Copy `export` command](#copy-export-command).

```sh {class="command-line" data-prompt="$"}
# export tabular data to /home/robot/data for specified part id with resource name my_movement_sensor, subtype movement_sensor and method Readings
viam data export tabular --part-id=e1234f0c-912c-1234-a123-5ac1234612345 --resource-name=my_movement_sensor --resource-subtype=rdk:component:movement_sensor --method=Readings --destination=/home/robot/data
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--destination` | Output directory for downloaded data. | **Required** |
| `--part-id` | Filter by specified part ID. | **Required** |
| `--resource-name` | Resource name. Sometimes called "component name". | **Required** |
| `--resource-subtype` | Resource {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet" >}}. | **Required** |
| `--method` | Filter by specified method. | **Required** |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |

### `data export binary filter`

Export binary or image data matching a filter to a specified location. Binary data will be downloaded in the original output it was specified as. You can copy this from the UI with a filter. See [Copy `export` command](#copy-export-command).

```sh {class="command-line" data-prompt="$"}
# export binary data from the specified org with mime types image/jpeg and image/png to /home/robot/data
viam data export binary filter --mime-types=image/jpeg,image/png --org-ids=12345678-eb33-123a-88ec-12a345b123a1 --destination=/home/robot/data
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--destination` | Output directory for downloaded data. | **Required** |
| `--bbox-labels` | String labels corresponding to bounding boxes within images. | Optional |
| `--component-name` | Filter by specified component name. | Optional |
| `--component-type` | Filter by specified component type. | Optional |
| `--location-ids` | Filter by specified location ID (accepts comma-separated list). See [Using the `ids` argument](#using-the-ids-argument) for instructions on retrieving these values. | Optional |
| `--machine-id` | Filter by specified machine ID. | Optional |
| `--machine-name` | Filter by specified machine name. | Optional |
| `--method` | Filter by specified method. | Optional |
| `--mime-types` | Filter by specified MIME type (accepts comma-separated list). | Optional |
| `--org-ids` | Filter by specified organizations ID (accepts comma-separated list). See [Using the `ids` argument](#using-the-ids-argument) for instructions on retrieving these values. | Optional |
| `--parallel` | Number of download requests to make in parallel. Default: `100`. | Optional |
| `--part-id` | Filter by specified part ID. | Optional |
| `--part-name` | Filter by specified part name. | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |
| `--tags` | Filter by specified tag (accepts comma-separated list). | Optional |
| `--timeout` | Number of seconds to wait for file downloads. Default: `30`. | Optional |

### `data export binary ids`

Export binary or image data by binary data ID to a specified location.

```sh {class="command-line" data-prompt="$"}
viam data export binary ids --destination=<output path> --binary-data-ids=<binary-data-ids>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--destination` | Output directory for downloaded data. | **Required** |
| `--binary-data-ids` | Binary data IDs to download. | **Required** |
| `--parallel` | Number of download requests to make in parallel. Default: `100`. | Optional |
| `--timeout` | Number of seconds to wait for file downloads. Default: `30`. | Optional |

### `data delete binary`

Delete binary data from the Viam Cloud.

```sh {class="command-line" data-prompt="$"}
# delete binary data of mime type image/jpeg in an organization between a specified timestamp
viam data delete binary --org-ids=123 --mime-types=image/jpeg --start 2024-08-20T14:10:34-04:00 --end 2024-08-20T14:16:34-04:00
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-ids` | Filter by specified organizations ID (accepts comma-separated list). | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |
| `--component-name` | Filter by specified component name. | Optional |
| `--component-type` | Filter by specified component type. | Optional |
| `--location-ids` | Filter by specified location ID (accepts comma-separated list). | Optional |
| `--machine-id` | Filter by specified machine ID. | Optional |
| `--machine-name` | Filter by specified machine name. | Optional |
| `--method` | Filter by specified method. | Optional |
| `--mime-types` | Filter by specified MIME type (accepts comma-separated list). | Optional |
| `--parallel` | Number of download requests to make in parallel. Default: `100`. | Optional |
| `--part-id` | Filter by specified part ID. | Optional |
| `--part-name` | Filter by specified part name. | Optional |
| `--tags` | Filter by specified tag (accepts comma-separated list). | Optional |

Viam currently only supports deleting approximately 500 files at a time.
To delete more data iterate over the data with a shell script:

```sh {class="command-line" data-prompt="$"}
# deleting one hour of image data
for i in {00..59}; do
  viam data delete binary --org-ids=<org-id> --mime-types=image/jpeg,image/png --start=2024-05-13T11:00:00.000Z --end=2024-05-13T11:${i}:00.000Z
done
```

### `data delete tabular`

Delete tabular data from the Viam Cloud.

```sh {class="command-line" data-prompt="$"}
viam data delete tabular --org-id=<org-id> --delete-older-than-days=<N>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID. | **Required** |
| `--delete-older-than-days` | Number of days, 0 means all data will be deleted. | **Required** |

### `data database configure`

Create a new database user for the Viam organization's MongoDB Atlas Data Federation instance, or change the password of an existing user. See [Configure data query](/data/query-data/).

```sh {class="command-line" data-prompt="$"}
# configure a database user for the Viam organization's MongoDB Atlas Data
# Federation instance, in order to query tabular data
viam data database configure --org-id=abc --password=my_password123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID. Uses default org if set. | Optional |
| `--password` | Password for the database user being configured. | **Required** |

### `data database hostname`

Get the MongoDB Atlas Data Federation instance hostname and connection URI. See [Configure data query](/data/query-data/).

```sh {class="command-line" data-prompt="$"}
# get the hostname to access a MongoDB Atlas Data Federation instance
viam data database hostname --org-id=abc
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID. Uses default org if set. | Optional |

### `data tag ids add`

Add tags to all data that matches the given binary data IDs.

```sh {class="command-line" data-prompt="$"}
# add tags to all data that matches the given ids in the current organization
viam data tag ids add --tags=new_tag_1,new_tag_2,new_tag_3 --binary-data-ids=123,456
```

See [Using the `ids` argument](#using-the-ids-argument) for details on retrieving the IDs.

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--binary-data-ids` | Binary data IDs to add tags to. | **Required** |
| `--tags` | Tags to add (accepts comma-separated list). | Optional |

### `data tag ids remove`

Remove tags from all data that matches the given binary data IDs.

```sh {class="command-line" data-prompt="$"}
# remove tags from all data that matches the given ids in the current organization
viam data tag ids remove --tags=new_tag_1,new_tag_2,new_tag_3 --binary-data-ids=123,456
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--binary-data-ids` | Binary data IDs to remove tags from. | **Required** |
| `--tags` | Tags to remove (accepts comma-separated list). | Optional |

### `data tag filter add`

Add tags to all data that matches a given filter. See [Using the `filter` argument](#using-the-filter-argument).

```sh {class="command-line" data-prompt="$"}
# add tags to all data that matches a given filter
viam data tag filter add --tags=new_tag_1,new_tag_2 --location-ids=012 --machine-name=cool-machine --org-ids=84842  --mime-types=image/jpeg,image/png
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--tags` | Tags to add (accepts comma-separated list). | Optional |
| `--filter-tags` | Filter tags. Options: `'tagged'`, `'untagged'`, or a comma-separated list of tags for all data matching any of the tags. | Optional |
| `--bbox-labels` | String labels corresponding to bounding boxes within images. | Optional |
| `--component-name` | Filter by specified component name. | Optional |
| `--component-type` | Filter by specified component type. | Optional |
| `--location-ids` | Filter by specified location ID (accepts comma-separated list). | Optional |
| `--machine-id` | Filter by specified machine ID. | Optional |
| `--machine-name` | Filter by specified machine name. | Optional |
| `--method` | Filter by specified method. | Optional |
| `--mime-types` | Filter by specified MIME type (accepts comma-separated list). | Optional |
| `--org-ids` | Filter by specified organizations ID (accepts comma-separated list). | Optional |
| `--part-id` | Filter by specified part ID. | Optional |
| `--part-name` | Filter by specified part name. | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |

### `data tag filter remove`

Remove tags from all data that matches a given filter. See [Using the `filter` argument](#using-the-filter-argument).

```sh {class="command-line" data-prompt="$"}
# remove tags from all data that matches a given filter
viam data tag filter remove --tags=new_tag_1 --location-ids=012 --machine-name=cool-machine --org-ids=84842  --mime-types=image/jpeg,image/png
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--tags` | Tags to remove (accepts comma-separated list). | Optional |
| `--filter-tags` | Filter tags. Options: `'tagged'`, `'untagged'`, or a comma-separated list of tags for all data matching any of the tags. | Optional |
| `--bbox-labels` | String labels corresponding to bounding boxes within images. | Optional |
| `--component-name` | Filter by specified component name. | Optional |
| `--component-type` | Filter by specified component type. | Optional |
| `--location-ids` | Filter by specified location ID (accepts comma-separated list). | Optional |
| `--machine-id` | Filter by specified machine ID. | Optional |
| `--machine-name` | Filter by specified machine name. | Optional |
| `--method` | Filter by specified method. | Optional |
| `--mime-types` | Filter by specified MIME type (accepts comma-separated list). | Optional |
| `--org-ids` | Filter by specified organizations ID (accepts comma-separated list). | Optional |
| `--part-id` | Filter by specified part ID. | Optional |
| `--part-name` | Filter by specified part name. | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |

### `data index create`

Create a custom index on a data collection.

```sh {class="command-line" data-prompt="$"}
viam data index create --collection-type=<type> --index-path=<file> [--org-id=<org-id>] [--pipeline-name=<name>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--collection-type` | Data collection type for index operations. Options: `hot-storage`, `pipeline-sink`. | **Required** |
| `--index-path` | Path to a JSON file defining the index using MongoDB index specification format. | **Required** |
| `--org-id` | The organization ID. Uses default org if set. | Optional |
| `--pipeline-name` | Name of the data pipeline (required when `--collection-type` is `pipeline-sink`). | Conditional |

### `data index delete`

Delete a custom index from a data collection.

```sh {class="command-line" data-prompt="$"}
viam data index delete --collection-type=<type> --index-name=<name> [--org-id=<org-id>] [--pipeline-name=<name>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--collection-type` | Data collection type for index operations. Options: `hot-storage`, `pipeline-sink`. | **Required** |
| `--index-name` | Name of the index to delete. | **Required** |
| `--org-id` | The organization ID. Uses default org if set. | Optional |
| `--pipeline-name` | Name of the data pipeline (required when `--collection-type` is `pipeline-sink`). | Conditional |

### `data index list`

List all custom indexes for a data collection.

```sh {class="command-line" data-prompt="$"}
viam data index list --collection-type=<type> [--org-id=<org-id>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--collection-type` | Data collection type for index operations. Options: `hot-storage`, `pipeline-sink`. | **Required** |
| `--org-id` | The organization ID. Uses default org if set. | Optional |

## `datapipelines`

The `datapipelines` command provides access to data pipelines for processing machine data with {{< glossary_tooltip term_id="mql" text="MQL" >}} queries.
Data pipelines help you optimize query performance for frequently accessed complex data transformations.

```sh {class="command-line" data-prompt="$"}
viam datapipelines create --org-id=<org-id> --name=<name> --schedule=<schedule> --mql=<mql-query> --data-source-type=<type> --enable-backfill=False
viam datapipelines rename --id=<pipeline-id> --name=<new-name>
viam datapipelines list --org-id=<org-id>
viam datapipelines describe --id=<pipeline-id>
viam datapipelines enable --id=<pipeline-id>
viam datapipelines disable --id=<pipeline-id>
viam datapipelines delete --id=<pipeline-id>
```

### `datapipelines create`

Create a new data pipeline.

```sh {class="command-line" data-prompt="$"}
# create a new data pipeline with standard data source type (default)
viam datapipelines create --org-id=123 --name="Daily Sensor Summary" --schedule="0 9 * * *" --data-source-type=standard --mql='[{"$match": {"component_name": "sensor-1"}}]' --enable-backfill=False

# create a data pipeline with hot storage data source type for faster access
viam datapipelines create --org-id=123 --name="Real-time Analytics" --schedule="*/5 * * * *" --data-source-type=hotstorage --mql='[{"$match": {"component_name": "camera-1"}}]' --enable-backfill=False
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--name` | Name of the data pipeline. | **Required** |
| `--schedule` | Cron schedule that expresses when the pipeline should run, for example `0 9 * * *` for daily at 9 AM. | **Required** |
| `--enable-backfill` | Enable the data pipeline to run over organization's historical data. Default: `false`. | **Required** |
| `--org-id` | ID of the organization that owns the data pipeline. Uses default org if set. | Optional |
| `--mql` | MQL (MongoDB Query Language) query as a JSON string for data processing. You must specify either `--mql` or `--mql-path` when creating a pipeline. | Optional |
| `--mql-path` | Path to a JSON file containing the MQL query for the data pipeline. You must specify either `--mql` or `--mql-path` when creating a pipeline. | Optional |
| `--data-source-type` | Data source type for the pipeline. Options: `standard` (default), `hotstorage`. | Optional |

### `datapipelines rename`

Rename a data pipeline.

```sh {class="command-line" data-prompt="$"}
viam datapipelines rename --id=<pipeline-id> --name=<new-name>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | ID of the data pipeline. | **Required** |
| `--name` | New name for the data pipeline. | **Required** |

### `datapipelines list`

List all data pipelines in an organization.

```sh {class="command-line" data-prompt="$"}
viam datapipelines list --org-id=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | ID of the organization that owns the data pipelines. Uses default org if set. | Optional |

### `datapipelines describe`

Get detailed information about a specific data pipeline.

```sh {class="command-line" data-prompt="$"}
viam datapipelines describe --id=abc123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | ID of the data pipeline. | **Required** |

### `datapipelines enable`

Resume executing a disabled data pipeline.

```sh {class="command-line" data-prompt="$"}
viam datapipelines enable --id=abc123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | ID of the data pipeline. | **Required** |

### `datapipelines disable`

Stop executing a data pipeline without deleting it.

```sh {class="command-line" data-prompt="$"}
viam datapipelines disable --id=abc123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | ID of the data pipeline. | **Required** |

### `datapipelines delete`

Delete a data pipeline.

```sh {class="command-line" data-prompt="$"}
viam datapipelines delete --id=abc123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | ID of the data pipeline. | **Required** |

## `dataset`

The `dataset` command allows you to manage machine data in datasets.
With it, you can add or remove images from a dataset, export data from a dataset, or filter a dataset by tags.

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=<name>
viam dataset rename --dataset-id=<dataset-id> --name=<name>
viam dataset list --org-id=<org-id>
viam dataset list --dataset-ids=<dataset-ids>
viam dataset delete --dataset-id=<dataset-id>
viam dataset export --destination=<output-directory> --dataset-id=<dataset-id>
viam dataset merge --name=<new-dataset-name> --dataset-ids=<dataset-id-1>,<dataset-id-2> [--org-id=<org-id>]
viam dataset data add filter --dataset-id=<dataset-id> [...named args]
viam dataset data remove filter --dataset-id=<dataset-id> [...named args]
viam dataset data add ids --dataset-id=<dataset-id>  --binary-data-ids=<binary-data-ids>
viam dataset data remove ids --dataset-id=<dataset-id> --binary-data-ids=<binary-data-ids>
```

### `dataset create`

Create a new dataset.

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=123 --name=MyDataset
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | Organization ID of the organization the dataset belongs to. | **Required** |
| `--name` | The name of the dataset to create. | **Required** |

### `dataset rename`

Rename an existing dataset.

```sh {class="command-line" data-prompt="$"}
viam dataset rename --dataset-id=123 --name=MyCoolDataset
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to rename. To retrieve the ID, navigate to your dataset's page, click **…** in the left-hand menu, and click **Copy dataset ID**. | **Required** |
| `--name` | The new name for the dataset. | **Required** |

### `dataset list`

List dataset information from specified IDs or for an org ID.

```sh {class="command-line" data-prompt="$"}
# show dataset information for all datasets within a specified org
viam dataset list --org-id=123

# show dataset information for the specified dataset IDs
viam dataset list --dataset-ids=123,456
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | Organization ID of the organization the dataset belongs to. | Optional |
| `--dataset-ids` | Dataset IDs of datasets to be listed (comma-separated list). To retrieve these IDs, navigate to your dataset's page, click **…** in the left-hand menu, and click **Copy dataset ID**. | Optional |

### `dataset delete`

Delete a dataset.

```sh {class="command-line" data-prompt="$"}
viam dataset delete --dataset-id=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to delete. | **Required** |

### `dataset export`

Download all the data from a dataset to a specified output directory in two folders called "data" and "metadata".

```sh {class="command-line" data-prompt="$"}
viam dataset export --destination=./dataset/example --dataset-id=abc
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to export. | **Required** |
| `--destination` | Output directory for downloaded data. | **Required** |
| `--only-jsonl` | Include only the JSON Lines files for local testing. No binary data is downloaded. | Optional |
| `--force-linux-path` | Force the use of Linux-style paths in the dataset.jsonl file. | Optional |
| `--parallel` | Number of download requests to make in parallel, with a default value of 100. | Optional |

### `dataset merge`

Merge multiple datasets into a new dataset.

```sh {class="command-line" data-prompt="$"}
viam dataset merge --name=CombinedDataset --dataset-ids=123,456 --org-id=789
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--name` | The name of the new merged dataset. | **Required** |
| `--dataset-ids` | Dataset IDs of datasets to merge (comma-separated list). | **Required** |
| `--org-id` | Organization ID of the organization the dataset belongs to. | **Required** |

### `dataset data add ids`

Add new images to an existing dataset by binary data ID. See [Using the `ids` argument](#using-the-ids-argument) for details on retrieving the IDs.

```sh {class="command-line" data-prompt="$"}
viam dataset data add ids --dataset-id=abc --binary-data-ids=aaa,bbb
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to add images to. To retrieve the ID, navigate to your dataset's page, click **…** in the left-hand menu, and click **Copy dataset ID**. | **Required** |
| `--binary-data-ids` | The binary data IDs of the images to add. | **Required** |
| `--org-id` | Organization ID of the organization the dataset belongs to. | Optional |

### `dataset data add filter`

Add to an existing dataset images that match a specified [filter](#using-the-filter-argument).

```sh {class="command-line" data-prompt="$"}
viam dataset data add filter --dataset-id=abc --location-ids=123 --org-ids=456 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to add images to. | **Required** |
| `--org-id` | Organization ID of the organization the dataset belongs to. | Optional |
| `--org-ids` | Organization IDs of the organizations to filter data on. | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |
| `--tags` | Filter by specified tag (accepts comma-separated list). | Optional |
| `--bbox-labels` | Filter data on bounding box labels. Accepts comma-separated list. | Optional |
| `--component-name` | Filter data on component name. | Optional |
| `--component-type` | Filter data on component type. | Optional |
| `--location-ids` | Filter data on location IDs. Accepts comma-separated list. | Optional |
| `--machine-id` | Filter data on machine ID. | Optional |
| `--machine-name` | Filter data on machine name. | Optional |
| `--method` | Filter data on capture method. | Optional |
| `--mime-types` | Filter data on MIME types. Accepts comma-separated list. | Optional |
| `--part-id` | Filter data on part ID. | Optional |
| `--part-name` | Filter data on part name. | Optional |

### `dataset data remove ids`

Remove images from an existing dataset by binary data ID. See [Using the `ids` argument](#using-the-ids-argument) for details on retrieving the IDs.

```sh {class="command-line" data-prompt="$"}
viam dataset data remove ids --dataset-id=abc --binary-data-ids=aaa,bbb
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to remove images from. | **Required** |
| `--binary-data-ids` | The binary data IDs of the images to remove. | **Required** |

### `dataset data remove filter`

Remove from an existing dataset images that match a specified [filter](#using-the-filter-argument).

```sh {class="command-line" data-prompt="$"}
viam dataset data remove filter --dataset-id=abc --location-ids=123 --org-ids=456 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | Dataset to remove images from. | **Required** |
| `--org-ids` | Organization IDs of the organizations to filter data on. | Optional |
| `--start` | ISO-8601 timestamp indicating the start of the interval. | Optional |
| `--end` | ISO-8601 timestamp indicating the end of the interval. | Optional |
| `--tags` | Filter by specified tag (accepts comma-separated list). | Optional |
| `--bbox-labels` | Filter data on bounding box labels. Accepts comma-separated list. | Optional |
| `--component-name` | Filter data on component name. | Optional |
| `--component-type` | Filter data on component type. | Optional |
| `--location-ids` | Filter data on location IDs. Accepts comma-separated list. | Optional |
| `--machine-id` | Filter data on machine ID. | Optional |
| `--machine-name` | Filter data on machine name. | Optional |
| `--method` | Filter data on capture method. | Optional |
| `--mime-types` | Filter data on MIME types. Accepts comma-separated list. | Optional |
| `--part-id` | Filter data on part ID. | Optional |
| `--part-name` | Filter data on part name. | Optional |

### Using the `ids` argument

When you use the `viam dataset data add` and `viam dataset data remove` commands, you specify images to add or remove using their binary data IDs as a comma-separated list.
For example, the following command adds three images specified by their binary data IDs to the specified dataset:

```sh {class="command-line" data-prompt="$"}
viam dataset data add ids --binary-data-ids=abc,123 --dataset-id=abc
```

The following command tags two images specified by their binary data IDs with three tags:

```sh {class="command-line" data-prompt="$"}
viam data tag ids add --tags=new_tag_1,new_tag_2,new_tag_3 --binary-data-ids=123,456
```

To find your organization's ID, run `viam organization list` or navigate to your organization's **Settings** page in the [Viam app](https://app.viam.com/).
Find **Organization ID** and click the copy icon.

To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) of the **DATA** tab and select a dataset.
Click **...** in the left-hand menu and click **Copy dataset ID**.

To find a location ID, run `viam locations list` or visit your [fleet's page](https://app.viam.com/robots) and copy the **Location ID**.

To find the binary data ID of a given image, navigate to the [**DATA** tab](https://app.viam.com/data/view) and select your image.
The **Binary Data ID** is shown under the **DETAILS** subtab that appears on the right.

You cannot use filter arguments such as `--start` or `--end` with the `ids` argument.

### Using the `filter` argument

When you use the `viam dataset data add`, `viam dataset data remove` or `viam data tag` commands, you can optionally `filter` by common search criteria to `add` or `remove` a specific subset of images based on a search filter.
For example, the following command adds all images captured between January 1 and October 1, 2023, that have the `example` tag applied, to the specified dataset:

```sh {class="command-line" data-prompt="$"}
viam dataset data add filter --dataset-id=abc --org-ids=123 --start=2023-01-01T05:00:00.000Z --end=2023-10-01T04:00:00.000Z --tags=example
```

The following command adds `"new_tag_1"` and `"new_tag_2"` to all images of type `"image/jpeg"` or `"image/png"` captured by the machine named `"cool-machine"` in organization `8484` and location `012`:

```sh {class="command-line" data-prompt="$"}
viam data tag filter add --tags=new_tag_1,new_tag_2 --location-ids=012 --machine-name=cool-machine --org-ids=84842  --mime-types=image/jpeg,image/png
```

To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) under the **DATA** tab and select a dataset.
Click **...** in the left-hand menu and click **Copy dataset ID**.

To find a location ID, run `viam locations list` or visit your [fleet's page](https://app.viam.com/robots) and copy from **Location ID**.

#### Copy `export` command

You can also have the filter parameters generated for you using the **Filters** pane of the **DATA** tab.
Navigate to the [**DATA** tab](https://app.viam.com/data/view), make your selections from the search parameters under the **Filters** pane (such as robot name, start and end time, or tags), and click the **Copy export command** button.
A `viam data export` command string will be copied to your clipboard that includes the search parameters you selected.
Removing the `viam data export` string, you can use the same filter parameters (such as `--start`, `--end`, etc) with your `viam data database add filter`, `viam data database remove filter`, or `viam data tag filter` commands, except you _must_ exclude the data type `binary` and `tabular` subcommands and `--destination` flags, which are specific to `viam data export`.

You cannot use the `--binary-data-ids` argument when using `filter`.

See [Create a dataset](/train/create-a-dataset/) for more information.

## `defaults`

The `defaults` command sets or clears default argument values so you do not have to pass the same `--org-id` or `--location-id` flag on every command. Once set, the value is read from your CLI config and used as the default for any command that accepts that argument.

```sh {class="command-line" data-prompt="$"}
viam defaults set-org --org-id=<org-id>
viam defaults clear-org
viam defaults set-location --location-id=<location-id>
viam defaults clear-location
```

### `defaults set-org`

Set the default organization argument.

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID to set as the default. | **Required** |

### `defaults clear-org`

Clear the default organization argument.

### `defaults set-location`

Set the default location argument.

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--location-id` | The location ID to set as the default. | **Required** |

### `defaults clear-location`

Clear the default location argument.

## `infer`

The `infer` command enables you to run [cloud inference](/vision/configure/) on data. Cloud inference runs in the cloud, instead of on a local machine.

```sh {class="command-line" data-prompt="$" data-output="2-18"}
viam infer --binary-data-id <binary-data-id> --model-name <model-name> --model-org-id <org-id-that-owns-model> --model-version "2025-04-14T16-38-25" --org-id <org-id-that-executes-inference>
Inference Response:
Output Tensors:
  Tensor Name: num_detections
    Shape: [1]
    Values: [1.0000]
  Tensor Name: classes
    Shape: [32 1]
    Values: [...]
  Tensor Name: boxes
    Shape: [32 1 4]
    Values: [...]
  Tensor Name: confidence
    Shape: [32 1]
    Values: [...]
Annotations:
Bounding Box Format: [x_min, y_min, x_max, y_max]
  No annotations.
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--binary-data-id` | The binary data ID of the image you want to run inference on. | **Required** |
| `--model-name` | The name of the model that you want to run in the cloud. | **Required** |
| `--model-version` | The version of the model that you want to run in the cloud. To find the latest version string for a model, visit the [registry page](https://app.viam.com/registry?type=ML+Model) for that model. You can find the latest version string in the **Version history** section, for instance "2024-02-16T12-55-32". Pass this value as a string, using double quotes. | **Required** |
| `--org-id` | The organization ID of the organization that will run the inference. | **Required** |
| `--model-org-id` | The organization ID of the organization that owns the model. | **Required** |

## `locations`

The `locations` command allows you to manage the [locations](/reference/) that you have access to.
With it, you can list available locations, filter locations by organization, or create a new location API key.

```sh {class="command-line" data-prompt="$"}
viam locations list [--organization=<organization>]
viam locations api-key create [--location-id=<location-id>] [--name=<name>] [--org-id=<org-id>]
```

### `locations list`

List all locations (name and id) that the authenticated session has access to, grouped by organization.

```sh {class="command-line" data-prompt="$"}
viam locations list [--organization=<organization>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--organization` | Restrict results to this organization. Default: the org set by `viam defaults set-org` if it exists, else the first one alphabetically. | Optional |

### `locations api-key create`

Create an API key for a specific location.

```sh {class="command-line" data-prompt="$"}
viam locations api-key create --location-id=<location-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--location-id` | The location to create an API key for. Default: the default location set with `viam defaults set-location`. | Optional |
| `--name` | The name of the API key. Default: your login info with the current time. | Optional |
| `--org-id` | The organization ID to attach the key to. Default: attempts to attach the key to the org of the location if only one org is attached to the location. | Optional |

## `login`

The `login` command authorizes your device for CLI usage.
By default, `viam login` opens a browser to authenticate using a personal access token.
Pass `--no-browser` to authenticate in a headless environment without opening a browser.
Use `viam login api-key` to authenticate using an API key, or `viam login print-access-token` to print the access token used by the current session.
See [Authenticate](/cli/overview/#authenticate).

```sh {class="command-line" data-prompt="$"}
viam login [--no-browser]
viam login api-key --key-id=<api-key-uuid> --key=<api-key-secret-value>
viam login print-access-token
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--no-browser` | Authenticate in a headless environment by preventing the opening of the default browser during login. Default: `false`. | Optional |

### `login api-key`

Authenticate to Viam using an organization, location, or machine part API key.

```sh {class="command-line" data-prompt="$"}
viam login api-key --key-id=<api-key-uuid> --key=<api-key-secret-value>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--key-id` | The `key id` (UUID) of the API key. | **Required** |
| `--key` | The `key value` of the API key. | **Required** |

### `login print-access-token`

Print the access token used to authenticate the current CLI session.

```sh {class="command-line" data-prompt="$"}
viam login print-access-token
```

## `logout`

The `logout` command ends an authenticated CLI session.

```sh {class="command-line" data-prompt="$"}
viam logout
```

## `machines` (alias `robots` and `machine`)

The `machines` command allows you to manage your machine fleet.
This includes:

- Creating, updating, and deleting machines
- Listing all machines that you have access to, filtered by organization and location.
- Creating API keys to grant access to a specific machine
- Retrieving machine and machine part status
- Retrieving machine and machine part logs
- Controlling a machine by issuing component and service commands
- Accessing your machine with a secure shell (when this feature is enabled)
- Copy files from and to machines
- Enter an interactive terminal on your machines

```sh {class="command-line" data-prompt="$"}
viam machines create --name=<machine name> --location=<location id>
viam machines update --machine=<machine id> [--name=<new name>] [--location=<new location id>]
viam machines delete --machine=<machine id>
viam machines list
viam machines status --machine=<machine id>
viam machines logs --machine=<machine id> [...named args]
viam machines api-key create --machine-id=<machine id> --org-id=<org id> --name=<key name>
viam machines part list --machine=<machine id>
viam machines part logs --machine=<machine id> --part=<part id> [...named args]
viam machines part status --machine=<machine id>
viam machines part run --machine=<machine id> [--stream] --data <method>
viam machines part shell --machine=<machine id> --part=<part id>
viam machines part restart --machine=<machine id> --part=<part id>
viam machines part history --part=<part id>
viam machines part cp --part=<part id> <file name> machine:/path/to/file
viam machines part add-job --part=<part id> [--config=<json or path>]
viam machines part update-job --part=<part id> --name=<job name> --config=<json or path>
viam machines part delete-job --part=<part id> --name=<job name>
viam machines part add-trigger --part=<part id> [--config=<json or path>]
viam machines part delete-trigger --part=<part id> --name=<trigger name>
```

To use `part shell` and `part cp`, add the [`ViamShellDanger` fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json), which contains the latest version of the shell service.

### `machines create`

Create a new machine in a specified location.

```sh {class="command-line" data-prompt="$"}
viam machines create --name="My Machine" --location=12345
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--name` | Name for the machine. | **Required** |
| `--location` | ID of the location that the machine belongs to. | **Required** |

### `machines update`

Move a machine from one location to another and/or rename the machine.

```sh {class="command-line" data-prompt="$"}
viam machines update --machine=123 --name="New Name"
viam machines update --machine=123 --location=67890
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine` | Machine ID or name for which the command is being issued. If machine name is used instead of ID, `--organization` and `--location` are required. | **Required** |
| `--new-name` | New name for the machine when renaming. | Optional |
| `--new-location` | ID of the location to move the machine to. | Optional |
| `--organization` | ID of the organization that the machine belongs to. | Optional |
| `--location` | ID of the current location of the machine. | Optional |

### `machines delete`

Delete a machine. Passing location and organization is optional but speeds up the process.

```sh {class="command-line" data-prompt="$"}
viam machines delete --machine=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine` | Machine ID or name. | **Required** |
| `--location` | ID of the location that the machine belongs to. | Optional |
| `--organization` | ID of the organization that the machine belongs to. | Optional |

### `machines list`

List all machines that the authenticated session has access to in a specified organization or location. Defaults to first organization and location alphabetically.

```sh {class="command-line" data-prompt="$"}
# list all machines in an organization, in all locations
viam machines list --all --organization=12345
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--all` | List all machines in the organization. Overrides `--location` flag. Default: `false`. | Optional |
| `--location` | ID of the location to list machines in. | Optional |
| `--organization` | ID of the organization to list machines in. | Optional |

### `machines status`

Retrieve machine status for a specified machine.

```sh {class="command-line" data-prompt="$"}
# get machine status
viam machines status --machine=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine` | Machine ID or name. | **Required** |
| `--location` | ID of the location that the machine belongs to. | Optional |
| `--organization` | ID of the organization that the machine belongs to. | Optional |

### `machines logs`

Retrieve logs for a specified machine.

```sh {class="command-line" data-prompt="$"}
# stream logs from a machine
viam machines logs --machine=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine` | Machine ID or name. | **Required** |
| `--errors` | Boolean, return only errors. Default: `false`. | Optional |
| `--levels` | Filter logs by levels (debug, info, warn, error). Accepts multiple inputs in comma-separated list. | Optional |
| `--keyword` | Filter logs by keyword. | Optional |
| `--start` | Filter logs to include only those after the start time. Time format example: `2025-01-13T21:30:00Z` (ISO-8601 timestamp in RFC3339). | Optional |
| `--end` | Filter logs to include only those before the end time. Time format example: `2025-01-13T21:35:00Z` (ISO-8601 timestamp in RFC3339). | Optional |
| `--count` | The number of logs to fetch. | Optional |
| `--format` | The file format for the output file. Options: `text` or `json`. | Optional |
| `--output` | The path to the output file to store logs in. | Optional |
| `--location` | ID of the location that the machine belongs to. | Optional |
| `--organization` | ID of the organization that the machine belongs to. | Optional |

### `machines api-key create`

Create an API key for a specific machine.

```sh {class="command-line" data-prompt="$"}
# create an API key for a machine
viam machines api-key create --machine-id=123 --name=MyKey
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine-id` | The ID of the machine to create an API key for. | **Required** |
| `--name` | The optional name of the API key. If omitted, a name will be auto-generated. | Optional |

### `machines part list`

List machine parts.

```sh {class="command-line" data-prompt="$"}
# list machine parts
viam machines part list --machine=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine` | Machine ID or name. | **Required** |
| `--location` | ID of the location that the machine belongs to. | Optional |
| `--organization` | ID of the organization that the machine belongs to. | Optional |

### `machines part status`

Retrieve machine status for a specified machine part.

```sh {class="command-line" data-prompt="$"}
viam machines part status --machine=<machine id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--location` | ID of the location that the machine belongs to. | Optional |
| `--organization` | ID of the organization that the machine belongs to. | Optional |

### `machines part run`

Run a component or service command, optionally at a specified interval. For commands that return data in their response, you can use this to stream data. See [Using the `--stream` and `--data` arguments](#using-the---stream-and---data-arguments).

```sh {class="command-line" data-prompt="$"}
# stream classifications from a machine part every 500 milliseconds from the Viam Vision Service with classifier "stuff_detector"
viam machines part run --part=myrover-main --stream=500ms \
--data='{"name": "vision", "camera_name": "cam", "classifier_name": "stuff_classifier", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--data` | Command data for the command being request to run. See [Using the `--stream` and `--data` arguments](#using-the---stream-and---data-arguments). | **Required** |
| `--stream` | If specified, the interval in which to stream the specified data, for example, 100ms or 1s. | Optional |

### `machines part logs`

Get logs for the specified machine part.

```sh {class="command-line" data-prompt="$"}
# stream logs from a machine part
viam machines part logs --part=myrover-main --tail=true
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--tail` | Tail (stream) logs. Default: `false`. | Optional |
| `--errors` | Return only errors. Default: `false`. | Optional |
| `--levels` | Filter logs by levels (debug, info, warn, error). Accepts multiple inputs in comma-separated list. | Optional |
| `--keyword` | Filter logs by keyword. | Optional |
| `--start` | Filter logs to include only those after the start time. | Optional |
| `--end` | Filter logs to include only those before the end time. | Optional |
| `--count` | The number of logs to fetch. | Optional |
| `--format` | The file format for the output file. Options: `text` or `json`. | Optional |
| `--output` | The path to the output file to store logs in. | Optional |

### `machines part shell`

Access a machine part securely using a secure shell to execute commands. To use this feature you must add the [`ViamShellDanger` fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json). The `ViamShellDanger` fragment contains the latest version of the shell service, which you must add to your machine before copying files or using the shell.

```sh {class="command-line" data-prompt="$"}
viam machines part shell --machine=<machine id> --part=<part id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |

### `machines part restart`

Restart a machine part.

```sh {class="command-line" data-prompt="$"}
# restart a part of a specified machine
viam machines part restart --part=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |

### `machines part history`

Display the configuration history for a machine part.

```sh {class="command-line" data-prompt="$"}
viam machines part history --part=<part id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--organization` | Organization name. | Optional |
| `--location` | Location name. | Optional |
| `--machine` | Machine ID or name. | Optional |
| `--filter-by-email` | Show only history entries saved by this email address. | Optional |

### `machines part cp`

Copy files to and from a machine part. To use this feature you must add the [`ViamShellDanger` fragment](https://app.viam.com/fragment/b511adfa-80ab-4a70-9bd5-fbb14696b17e/json), which contains the shell service, to your machine. Once added you can use `cp` in a similar way to the Linux `scp` command to copy files to and from machines.

```sh {class="command-line" data-prompt="$"}
# Copy a single file to a machine:
viam machines part cp --part=123 my_file machine:/home/user/

# Recursively copy a directory to a machine:
viam machines part cp --part=123 -r my_dir machine:/home/user/

# Copy multiple files to a machine with recursion and keep original permissions and metadata for the files:
viam machines part cp --part=123 -r -p my_dir my_file machine:/home/user/some/existing/dir/

# Copy a single file from a machine to a local destination:
viam machines part cp --part=123 machine:my_file ~/Downloads/

# Recursively copy a directory from a machine to a local destination:
viam machines part cp --part=123 -r machine:my_dir ~/Downloads/

# Copy multiple files from the machine to a local destination with recursion and keep original permissions and metadata for the files:
viam machines part cp --part=123 -r -p machine:my_dir machine:my_file ~/some/existing/dir/
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--recursive`, `-r` | Recursively copy files. Default: `false`. | Optional |
| `--preserve`, `-p` | Preserve modification times and file mode bits from the source files. Default: `false`. | Optional |

### `machines part tunnel`

Tunnel connections to a specified port on a machine part. You must explicitly enumerate ports to which you are allowed to tunnel in your machine's JSON config. See [Tunnel to a machine part](/fleet/system-settings/).

```sh {class="command-line" data-prompt="$"}
# tunnel connections to the specified port on a machine part
viam machines part tunnel --part=123 --destination-port=1111 --local-port 2222
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--destination-port` | The port on a machine part to tunnel to. | **Required** |
| `--local-port` | The local port from which to tunnel. | **Required** |

### `machines part get-ftdc`

Download FTDC data from a machine part. Requires the shell service.

```sh {class="command-line" data-prompt="$"}
# Download FTDC data from a part to a local directory:
viam machines part get-ftdc --part=123 ~/some/existing/dir/
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |

### `machines part create`

Create a new part on a machine.

```sh {class="command-line" data-prompt="$"}
viam machines part create --machine=<machine id> --part-name=<new part name>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--machine` | Machine ID or name. | **Required** |
| `--part-name` | Name for the new part. | **Required** |

### `machines part delete`

Delete a part.

```sh {class="command-line" data-prompt="$"}
viam machines part delete --part=<part id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID to delete. | **Required** |

### `machines part add-resource`

Add a component or service to a part's configuration by specifying an API and model triplet.

```sh {class="command-line" data-prompt="$"}
viam machines part add-resource --part=<part id> --name=<resource name> --model-name=<namespace:type:model>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--name` | Name for the resource. | **Required** |
| `--model-name` | Model triplet (`namespace:type:model`) for the resource to add. | **Required** |

### `machines part remove-resource`

Remove a resource from a part's configuration.

```sh {class="command-line" data-prompt="$"}
viam machines part remove-resource --part=<part id> --name=<resource name>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--name` | Name of the resource to remove. | **Required** |

### `machines part fragments add`

Attach a configuration fragment to a part.

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add --part=<part id> [--fragment=<fragment id>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--fragment` | Fragment ID to add. If omitted, the CLI prompts interactively. | Optional |

### `machines part fragments remove`

Detach a configuration fragment from a part.

```sh {class="command-line" data-prompt="$"}
viam machines part fragments remove --part=<part id> [--fragment=<fragment id>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--fragment` | Fragment ID to remove. | Optional |

### `machines part motion print-config`

Print the motion planning configuration for the part.

```sh {class="command-line" data-prompt="$"}
viam machines part motion print-config --part=<part id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |

### `machines part motion print-status`

Print current motion state for the part.

```sh {class="command-line" data-prompt="$"}
viam machines part motion print-status --part=<part id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |

### `machines part motion get-pose`

Get the pose of a component in a reference frame.

```sh {class="command-line" data-prompt="$"}
viam machines part motion get-pose --part=<part id> --component=<component name>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--component` | Component name for the motion command. | **Required** |

### `machines part motion set-pose`

Command a component to move to a specific pose.

```sh {class="command-line" data-prompt="$"}
viam machines part motion set-pose --part=<part id> --component=<component name>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--component` | Component name for the motion command. | **Required** |

### `machines part add-job`

Add a scheduled job that runs a method on a resource at a given interval. Run without `--config` to launch an interactive builder, or pass `--config` with inline JSON or a path to a JSON file.

A job config object accepts the following fields:

- `name` (required): unique name for this job.
- `schedule` (required): one of `continuous`, a Go duration (for example, `5s`, `1h30m`, `500ms`), or a cron expression (for example, `0 0 * * *`, or `*/5 * * * * *` with seconds).
- `resource` (required): name of the component or service to run the method on.
- `method` (required): gRPC method name. For example, `DoCommand` or `GetReadings`.
- `command` (optional): JSON object passed as the argument to `DoCommand`.
- `log_configuration` (optional): for example, `{"level":"debug"}`. Level must be one of `debug`, `info`, `warn`, or `error`.

```sh {class="command-line" data-prompt="$"}
# launch the interactive job builder
viam machines part add-job --part=<part id>

# add a job from inline JSON
viam machines part add-job --part=<part id> \
    --config '{"name":"my-job","schedule":"1h","resource":"my-sensor","method":"GetReadings"}'

# add a job from a JSON file
viam machines part add-job --part=<part id> --config ./job.json
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--config` | JSON job config or path to JSON file. Omit to use the interactive form. | Optional |
| `--organization` | Organization name. | Optional |
| `--location` | Location name. | Optional |
| `--machine` | Machine ID or name. | Optional |

### `machines part update-job`

Update an existing job's configuration by name. The `--config` flag accepts a single JSON object (inline or a path to a JSON file) with the fields to change. Only the fields provided will be updated; all other fields remain unchanged. The job name cannot be changed.

```sh {class="command-line" data-prompt="$"}
# change the schedule
viam machines part update-job --part=<part id> --name=my-job --config '{"schedule":"30m"}'

# change multiple fields
viam machines part update-job --part=<part id> --name=my-job \
    --config '{"schedule":"0 0 * * *","method":"DoCommand","command":{"action":"reset"}}'
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--name` | Name of the job to update. | **Required** |
| `--config` | JSON job config or path to JSON file with fields to update. | **Required** |
| `--organization` | Organization name. | Optional |
| `--location` | Location name. | Optional |
| `--machine` | Machine ID or name. | Optional |

### `machines part delete-job`

Delete an existing scheduled job by name.

```sh {class="command-line" data-prompt="$"}
viam machines part delete-job --part=<part id> --name=my-job
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--name` | Name of the job to delete. | **Required** |
| `--organization` | Organization name. | Optional |
| `--location` | Location name. | Optional |
| `--machine` | Machine ID or name. | Optional |

### `machines part add-trigger`

Add a trigger to a machine part. Run without `--config` to use an interactive form, or provide `--config` with inline JSON or a path to a JSON file.

Trigger configs support the following event types:

- `part_online`: liveness check.
- `part_data_ingested`: fires when data of the specified types is ingested.
- `conditional_data_ingested`: fires when data ingested by a specific data capture method matches a condition.
- `conditional_logs_ingested`: fires when logs at the specified levels are ingested.

Each trigger requires `notifications`, an array of objects with `type` (`email` or `webhook`), `value`, and `seconds_between_notifications`.

```sh {class="command-line" data-prompt="$"}
# launch the interactive trigger builder
viam machines part add-trigger --part=<part id>

# add a trigger from inline JSON
viam machines part add-trigger --part=<part id> \
    --config '{"name":"my-online-trigger","event":{"type":"part_online"},"notifications":[{"type":"email","value":"user@example.com","seconds_between_notifications":60}]}'

# add a trigger from a JSON file
viam machines part add-trigger --part=<part id> --config ./trigger.json
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--config` | JSON trigger config or path to JSON file. Omit to use the interactive form. | Optional |
| `--organization` | Organization name. | Optional |
| `--location` | Location name. | Optional |
| `--machine` | Machine ID or name. | Optional |

### `machines part delete-trigger`

Delete a trigger from a machine part by name.

```sh {class="command-line" data-prompt="$"}
viam machines part delete-trigger --part=<part id> --name=<trigger name>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Part ID for which the command is being issued. | **Required** |
| `--name` | Name of the trigger to delete. | **Required** |
| `--organization` | Organization name. | Optional |
| `--location` | Location name. | Optional |
| `--machine` | Machine ID or name. | Optional |

### Using the `--stream` and `--data` arguments

Issuing the `part` command with the `run` positional argument allows you to run component and service (resource) commands for a selected machine part.

The `--data` parameter is required and you must specify both:

- Method arguments in JSON format
- A resource method (in the form of the {{< glossary_tooltip term_id="protobuf" text="protobuf" >}} package and method path)

The format of what is passed to the `--data` argument is:

```sh {class="command-line" data-prompt="$"}
'{"arg1": "val1"}' <protobuf path>
```

You can find the protobuf path for the Viam package and method in the [Viam API package](https://github.com/viamrobotics/api/tree/main/proto/viam) by navigating to the component or service directory and then clicking on the resource file. The protobuf path is the package name.

For example:

```sh {class="command-line" data-prompt="$"}
'{"name": "vision", "camera_name": "cam", "classifier_name": "my_classifier", "n":1}' \
viam.service.vision.v1.VisionService.GetClassificationsFromCamera
```

The `--stream` argument, when included in the CLI command prior to the `--data` command, will stream data back at the specified interval.

## `metadata`

The `metadata` command allows you to read organization, location, machine, and machine part metadata.

```sh {class="command-line" data-prompt="$"}
viam metadata read --part-id=<part-id>
```

### `metadata read`

Read organization, location, machine, and machine part metadata.

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--location-id` | The ID of the location to read metadata from. | Optional |
| `--machine-id` | The ID of the machine to read metadata from. | Optional |
| `--org-id` | The ID of the org to read metadata from. | Optional |
| `--part-id` | The ID of the part to read metadata from. | Optional |

## `module`

The `module` command allows to you to work with {{< glossary_tooltip term_id="module" text="modules" >}}.
This includes:

- Generating stub files for a new module
- Creating metadata for a {{< glossary_tooltip term_id="resource" text="modular resource" >}}
- Uploading a new module to the [registry](https://app.viam.com/registry)
- Uploading a new version of your module to the [registry](https://app.viam.com/registry)
- Updating an existing module in the Viam Registry
- Updating a module's metadata file based on models it provides
- Building your module for different architectures using cloud runners
- Building a module locally and running it on a target device. Rebuilding & restarting if already running.
- Downloading a module package from the registry

See [Update and manage modules you created](/build-modules/manage-modules/) for more information.

If you update and release your module as part of a continuous integration (CI) workflow, you can also
[automatically upload new versions of your module on release](/build-modules/manage-modules/) using a GitHub Action.

```sh {class="command-line" data-prompt="$"}
viam module generate
viam module create --name=<module-name> [--org-id=<org-id> | --public-namespace=<namespace>]
viam module update [--module=<path to meta.json>]
viam module update-models [--binary=<binary>] [...named args]
viam module build start --version=<version> [...named args]
viam module build local --module=<path to meta.json> [arguments...]
viam module build list [command options] [arguments...]
viam module build logs --build-id=<build-id> [...named args]
viam module reload [...named args]
viam module upload --version=<version> --platform=<platform> [--org-id=<org-id> | --public-namespace=<namespace>] [--module=<path to meta.json>] <module-path> --tags=<tags>
viam module download [command options]
viam module local-app-testing --app-url http://localhost:3000
```

### `module generate`

Generate a new module with stub files and a <file>meta.json</file> file. Recommended when starting a new module.

```sh {class="command-line" data-prompt="$"}
# auto-generate stub files for a new modular resource by following prompts
viam module generate
```

{{% alert title="Note" color="note" %}}
If you are writing your module using Python, you must have Python version 3.11 or newer installed on your computer for the `viam module generate` command to work.
{{% /alert %}}

{{% hiddencontent %}}

The `viam module generate` command can generate code for the following resource types:

Components:

- Arm component
- Audio input component
- Base component
- Board component
- Camera component
- Encoder component
- Gantry component
- Generic component
- Gripper component
- Input component
- Motor component
- Movement sensor component
- Pose tracker component
- Power sensor component
- Sensor component
- Servo component

Services:

- Generic service
- MLModel service
- Motion service
- Navigation service
- SLAM service
- Vision service

{{% /hiddencontent %}}

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--name` | Name to use for the module. For example, a module that contains sensor implementations might be named `sensors`. We recommend _not_ using this option and instead following the prompts. | Optional |
| `--language` | Language to use for the module. Options: `python`, `go`. We recommend _not_ using this option and instead following the prompts. | Optional |
| `--visibility` | Module visibility. Options: `private`, `public`, `public_unlisted`. We recommend _not_ using this option and instead following the prompts. | Optional |
| `--public-namespace` | Namespace or organization ID of the module. Must be either a valid organization ID, or a namespace that exists within a user organization. We recommend _not_ using this option and instead following the prompts. | Optional |
| `--resource-subtype` | The API to implement with the modular resource. For example, `motor`. We recommend _not_ using this option and instead following the prompts after running the command. | Optional |
| `--model-name` | Name for the particular resource subtype implementation. For example, a sensor model that detects moisture might be named `moisture`. We recommend _not_ using this option and instead following the prompts. | Optional |
| `--register` | Register the module with Viam to associate it with your organization. Default: `false`. | Optional |

### `module create`

Generate a <file>meta.json</file> file and register the metadata with the Viam registry. Recommended when you already have working module code.

```sh {class="command-line" data-prompt="$"}
# generate metadata for and register a module named 'my-module' using your organization's public namespace:
viam module create --name=my-module --public-namespace=my-namespace

# generate metadata for and register a module named "my-module" using your organization's organization ID:
viam module create --name=my-module --org-id=abc
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--name` | The name of the module. For example: `hello-world`. | **Required** |
| `--org-id` | The organization ID to associate the module to. See [Using the `--org-id` and `--public-namespace` arguments](#using-the---org-id-and---public-namespace-arguments). | **Required** |
| `--public-namespace` | The namespace to associate the module to. See [Using the `--org-id` and `--public-namespace` arguments](#using-the---org-id-and---public-namespace-arguments). | **Required** |
| `--local-only` | Create a meta.json file for local use, but don't create the module on the backend. Default: `false`. | Optional |

### `module update`

Update your module's metadata and documentation in the Viam registry. Updates are based on changes to [<file>meta.json</file>](/build-modules/module-reference/), the module <file>README.md</file>, and the model readme <FILE>namespace_module_model.md</FILE>. Viam automatically runs `update` when you `upload` your module, as well as when you trigger a cloud build with Viam's default build action.

```sh {class="command-line" data-prompt="$"}
# update an existing module
viam module update --module=./meta.json
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. | Optional |

### `module update-models`

Update the module's metadata file with the models it provides.

```sh {class="command-line" data-prompt="$"}
# update a module's metadata file based on models it provides
viam module update-models --binary=./packaged-module.tar.gz --module=./meta.json
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--binary` | The module executable to run (binary or script). Must work on the OS or processor of the device. If omitted, the CLI uses the entrypoint defined in <file>meta.json</file>. | Optional |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. | Optional |

### `module upload`

Validate and upload a new or existing custom module on your local filesystem to the Viam Registry. See [Upload validation](#upload-validation) for more information.

Pass the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code as a positional argument.

```sh {class="command-line" data-prompt="$"}
# upload a new or updated custom module to the Viam Registry:
viam module upload --version=1.0.0 --platform=darwin/arm64 packaged-module.tar.gz --tags=distro:ubuntu,os_version:20.04,codename:focal,cuda:true,cuda_version:11,jetpack:5
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--version` | The version of your module to set for this upload. See [Using the `--version` argument](#using-the---version-argument). | **Required** |
| `--platform` | The architecture of your module binary. See [Using the `--platform` argument](#using-the---platform-argument). | **Required** |
| `--org-id` | The organization ID to associate the module to. See [Using the `--org-id` and `--public-namespace` arguments](#using-the---org-id-and---public-namespace-arguments). | **Required** |
| `--public-namespace` | The namespace to associate the module to. See [Using the `--org-id` and `--public-namespace` arguments](#using-the---org-id-and---public-namespace-arguments). | **Required** |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. Default: `./meta.json`. | Optional |
| `--name` | Name of the module. Used if you don't have a <file>meta.json</file>. | Optional |
| `--upload` | The path to the upload. | Optional |
| `--tags` | Comma-separated list of platform tags that determine to which platforms this binary can be deployed. Examples: `distro:debian,distro:ubuntu, os_version:22.04,os_codename:jammy`. For a machine to use an uploaded binary, all tags must be satisfied as well as the `--platform` field. <ul><li>`distro`: Distribution. You can find this in `/etc/os-release`. `"debian"` or `"ubuntu"`.</li><li>`os_version`:  Operating System version. On Linux, you can find this in `/etc/os-release`. Example for linux: `22.04`. On Mac, run `sw_vers --productVersion` and use the major version only. Example for mac: `14`.</li><li>`codename`: The operating system codename. Find this in `/etc/os-release`. For example: `"bullseye"`, `"bookworm"`, or `"jammy"`.</li><li>`cuda`: Whether using CUDA compiler. Run `nvcc --version`. For example: `"true"`.</li><li>`cuda_version`: The CUDA compiler version. Run `nvcc --version`. For example: `"11"` or `"12"`.</li><li>`jetpack`: Version of the NVIDIA JetPack SDK. Run `apt-cache show nvidia-jetpack`. For example: `"5"`.</li><li>`pi`: Version of the Raspberry Pi: `"4"` or `"5"`.</li><li>`pifull`: Compute module or model number, for example `cm5p` or `5B`.</li></ul> | Optional |
| `--force` | Skip local validation of the packaged module, which may result in an unusable module if the contents of the packaged module are not correct. | Optional |

### `module reload`

Build a module in the cloud and configure the target machine to download it directly. Rebuild and restart if the module is already running.

```sh {class="command-line" data-prompt="$"}
# build a module and run it on target machine
viam module reload --part-id e1234f0c-912c-1234-a123-5ac1234612345
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part-id` | Part ID of the machine part. Get from the **Live**/**Offline** dropdown in the web app. Default: the part ID present in the cloud credentials at <file>/etc/viam.json</file>. | Optional |
| `--cloud-config` | The location of the <FILE>viam.json</FILE> file which contains the machine ID to lookup the part-id. Alternative to `--part-id`. Default: `/etc/viam.json`. | Optional |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. Default: `meta.json`. | Optional |
| `--model-name` | If passed, creates a resource in the part config with the given model triple. Use with `--resource-name`. Default: Creates no new resource. | Optional |
| `--resource-name` | If passed, creates a new resource with the given resource name. Use with `--model-name`. Default: resource type with a unique numerical suffix. | Optional |
| `--path` | The path to the root of the module's git repo to build. Default: `.`. | Optional |
| `--workdir` | Use this to indicate that your <file>meta.json</file> is in a subdirectory of your repo. `--module` flag should be relative to this. Default: `.`. | Optional |

### `module reload-local`

Build a module locally and run it on a target machine. Rebuild and restart if it is already running. The module is loaded to <FILE>~/.viam/packages-local/namespace_module-name_from_reload-module.tar.gz</FILE> on the target machine.

```sh {class="command-line" data-prompt="$"}
# build and configure a module running on your local machine without shipping a tarball.
viam module reload-local --local
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | The module ID (`namespace:module-name` or `org-id:module-name`). | Optional |
| `--part-id` | Part ID of the machine part. Required if running on a remote device. | Optional |
| `--cloud-config` | The location of the <FILE>viam.json</FILE> file which contains the machine ID to lookup the part-id. Alternative to `--part-id`. Default: `/etc/viam.json`. | Optional |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. | Optional |
| `--model-name` | If passed, creates a resource in the part config with the given model triple. Use with `--resource-name`. Default: Creates no new resource. | Optional |
| `--resource-name` | If passed, creates a new resource with the given resource name. Use with `--model-name`. Default: Creates no new resource. | Optional |
| `--local` | Use if the target machine is localhost, to run the entrypoint directly rather than transferring a bundle. Default: `false`. | Optional |
| `--workdir` | Use this to indicate that your <file>meta.json</file> is in a subdirectory of your repo. `--module` flag should be relative to this. Default: `.`. | Optional |
| `--no-build` | Skip build step. Default: `false`. | Optional |
| `--no-progress` | Hide progress of the file transfer. Default: `false`. | Optional |
| `--home` | Specify home directory for a remote machine where `$HOME` is not the default `/root`. | Optional |
| `--name` | The name of the module. For example: `hello-world`. | Optional |

### `module restart`

Restart a running module.

```sh {class="command-line" data-prompt="$"}
# restart a running module
viam module restart --id viam:python-example-module
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | ID of the module to restart, for example `viam:wifi-sensor`. Pass at most one of `--name`, `--id`. | Optional |
| `--name` | Name of the module to restart. Pass at most one of `--name`, `--id`. | Optional |
| `--part-id` | Part ID of the machine part. Required if running on a remote device. Default: the part ID present in <file>/etc/viam.json</file>. | Optional |
| `--cloud-config` | The location of the <FILE>viam.json</FILE> file which contains the machine ID to lookup the part-id. Alternative to `--part-id`. Default: `/etc/viam.json`. | Optional |
| `--module` | The path to the <file>meta.json</file> file. Used for module ID. Can be overridden with `--id` or `--name`. Default: `meta.json`. | Optional |

### `module build start`

Start a module build in a cloud runner using the build step in your [`meta.json` file](/build-modules/module-reference/). See [Using the `build` subcommand](#using-the-build-subcommand).

```sh {class="command-line" data-prompt="$"}
# initiate a cloud build for a public GitHub repo
viam module build start --version "0.1.2"

# initiate a cloud build for a private GitHub repo
viam module build start --version "0.1.2" --token ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--version` | The version of your module to set for this build. See [Using the `--version` argument](#using-the---version-argument). | **Required** |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. | Optional |
| `--platforms` | List of platforms to cloud build for. Default: `build.arch` in <file>meta.json</file>. | Optional |
| `--ref` | Git reference to clone when building your module. This can be a branch name or a commit hash. Default: `main`. | Optional |
| `--token` | GitHub token with repository **Contents** read access, and **Actions** read and write access. Required for private repos, not necessary for public repos. | Optional |
| `--workdir` | Use this to indicate that your <file>meta.json</file> is in a subdirectory of your repo. `--module` flag should be relative to this. Default: `.`. | Optional |

### `module build local`

Start a module build locally using the build step in your [`meta.json` file](/build-modules/module-reference/). See [Using the `build` subcommand](#using-the-build-subcommand).

```sh {class="command-line" data-prompt="$"}
# initiate a build locally without running a cloud build job
viam module build local
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--module` | The path to the [`meta.json` file](/build-modules/module-reference/) for the module, if not in the current directory. | Optional |

### `module build list`

List the status of your cloud module builds. See [Using the `build` subcommand](#using-the-build-subcommand).

```sh {class="command-line" data-prompt="$"}
# list all in-progress builds and their build status
viam module build list
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--module` | Path to <file>meta.json</file>. Default: `./meta.json`. | Optional |
| `--id` | Restrict output to just return builds that match this build ID. | Optional |
| `--count` | Number of cloud builds to list. Defaults to displaying all builds. | Optional |

### `module build logs`

Show the logs from a specific cloud module build. See [Using the `build` subcommand](#using-the-build-subcommand).

```sh {class="command-line" data-prompt="$"}
# initiate a build and return the build logs as soon as completed
viam module build logs --wait --build-id=$(viam module build start --version "0.1.2")
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--build-id` | The build ID to show logs for, as returned from `build start`. | **Required** |
| `--platform` | Restricts the logs returned by the command to only those build jobs that match the specified platform. See [Using the `--platform` argument](#using-the---platform-argument). Default: all platforms. | Optional |
| `--wait` | Wait for the build to finish before outputting any logs. Default: `false`. | Optional |
| `--group-logs` | Write `::group::` commands so GitHub Actions logs collapse. Default: `false`. | Optional |

### `module download`

Download a module package from the registry.

```sh {class="command-line" data-prompt="$"}
# download a module package from the registry to the current directory
viam module download --id=acme:my-module

# download a module package from the registry to a specific directory
viam module download --id=acme:my-module --destination=/path/to/download/directory

# download a specific version of a module package for a specific platform
viam module download --id=acme:my-module --version=1.0.0 --platform=linux/amd64
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--id` | The module ID (`namespace:module-name` or `org-id:module-name`). | Optional |
| `--version` | The version of the module to download. Defaults to `latest`. | Optional |
| `--platform` | The architecture of the module binary to download. See [Using the `--platform` argument](#using-the---platform-argument). | Optional |
| `--destination` | Output directory for downloaded package. Default: `.`. | Optional |

### `module local-app-testing`

Test your viam application locally. This will stand up a local proxy at `http://localhost:8012` to simulate the Viam application server.

```sh {class="command-line" data-prompt="$"}
# proxy your local Viam application and open a browser window and navigate to `http://localhost:8012/
viam module local-app-testing --app-url http://localhost:3000
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--app-url` | The url where local app is running, including port number. For example `http://localhost:5000`. | **Required** |
| `--machine-id` | The machine ID of the machine you want to test with. You can get your machine ID on the [Fleet page](https://app.viam.com/fleet/machines). | Optional |

### Using the `--org-id` and `--public-namespace` arguments

All of the `module` commands accept either the `--org-id` or `--public-namespace` argument.

- Use the `--public-namespace` argument to supply the [namespace of your organization](/build-modules/module-reference/).
  This will upload your module to the Viam Registry and share it with other users.
- Use the `--org-id` to provide your organization ID instead, This will upload your module privately within your organization.

You may use either argument for the `viam module create` command, but must use `--public-namespace` for the `update` and `upload` commands when uploading as a public module (`"visibility": "public"`) to the Viam Registry.

### Using the `--platform` argument

The `--platform` argument accepts one of the following architectures:

<!-- prettier-ignore -->
| Architecture | Description | Common use case |
| ------------ | ----------- | --------------- |
| `any` | Any supported OS running any supported architecture. | Suitable for most Python modules that do not require OS-level support (such as platform-specific dependencies). |
| `any/amd64` | Any supported OS running the `amd64` architecture. | Suitable for most Docker-based modules on `amd64`. |
| `any/arm64` | Any supported OS running the `arm64` (`aarch64`) architecture. | Suitable for most Docker-based modules on `arm64`. |
| `linux/any` | Linux machines running any architecture. | Suitable for Python modules that also require Linux OS-level support (such as platform-specific dependencies). |
| `darwin/any` | macOS machines running any architecture. | Suitable for Python modules that also require macOS OS-level support (such as platform-specific dependencies). |
| `linux/amd64` | Linux machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on Linux `amd64`. |
| `linux/arm64` | Linux machines running the `arm64` (`aarch64`) architecture, such as the Raspberry Pi. | Suitable for most C++ or Go modules on Linux `arm64`. |
| `linux/arm32v7` | Linux machines running the `arm32v7` architecture. | Suitable for most C++ or Go modules on Linux `arm32v7`. |
| `linux/arm32v6` | Linux machines running the `arm32v6` architecture. | Suitable for most C++ or Go modules on `arm32v6`. |
| `darwin/amd64` | macOS machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on macOS `amd64`. |
| `darwin/arm64` | macOS machines running the `arm64` architecture, such as Apple Silicon. | Suitable for most C++ or Go modules on macOS `arm64`. |
| `windows/amd64` | Windows machines running the Intel `x86_64` architecture. | Suitable for most C++ or Go modules on Windows `amd64`. |

For information on which of these platforms are supported for cloud build, see [Supported platforms for automatic updates](/build-modules/manage-modules/).

You can use the `uname -m` command on your computer or board to determine its system architecture.

The `viam module upload` command only supports one `platform` argument at a time.
If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.

If you specify a platform that includes `any` (such as `any`, `any/amd64`, or `linux/any`), a machine that deploys your module will select the _most restrictive_ architecture from the ones you have provided for your module.
For example, if you upload your module with support for `any/amd64` and then also upload with support for `linux/amd64`, a machine running the `linux/amd64` architecture deploys the `linux/amd64` distribution, while a machine running the `darwin/amd64` architecture deploys the `any/amd64` distribution.

The Viam Registry page for your module displays the platforms your module supports for each version you have uploaded.

If you are using the `build logs` command, the `--platform` argument instead restricts the logs returned by the command to only those build jobs that match the specified platform.

### Using the `--version` argument

The `--version` argument accepts a valid [semver 2.0](https://semver.org/) version (example: `1.0.0`).
You set an initial version for your custom module with your first `viam module upload` command for that module, and can later increment the version with subsequent `viam module upload` commands.

{{% alert title="Important" color="note" %}}
You cannot upload multiple distributions for the same architecture with the same version number.
You can delete the distribution files for a version, but you must increment to a new version number to upload a new distribution.
{{% /alert %}}

Once your module is uploaded, users can select which version of your module to use on their machine from your module's page on the Viam Registry.
Users can choose to pin to a specific patch version, permit upgrades within major release families or only within minor releases, or permit continuous updates.

When you `update` a module configuration and then `upload` it, the `entrypoint` for that module defined in the [`meta.json` file](/build-modules/module-reference/) is associated with the specific `--version` for that `upload`.
Therefore, you are able to change the `entrypoint` file from version to version, if desired.

### Upload validation

When you `upload` a module, the command performs basic validation of your module to check for common errors.
The following criteria are checked for every `upload`:

- The module must exist on the filesystem at the path provided to the `upload` command.
- The entry point file specified in the [`meta.json` file](/build-modules/module-reference/) must exist on the filesystem at the path specified.
- The entry point file must be executable.
- If the module is provided to the `upload` command as a compressed archive, the archive must have the `.tar.gz` or `.tgz` extension.

See [Create a module](/build-modules/write-a-driver-module/) and [Update and manage modules you created](/build-modules/manage-modules/) for a detailed walkthrough of the `viam module` commands.

### Using the `build` subcommand

You can use the `module build start` or `module build local` commands to build your custom module according to the build steps in your <file>meta.json</file> file:

- Use `build start` to build or compile your module on a cloud build host that might offer more platform support than you have access to locally.
- Use `build local` to quickly test that your module builds or compiles as expected on your local hardware.

To configure your module's build steps, add a `build` object to your [`meta.json` file](/build-modules/module-reference/) like the following:

<!-- Developers can either have a single build file for all platforms, or platform specific files: -->

<!-- { {< tabs >}}
{ {% tab name="Single Build File" %}} -->

```json {class="line-numbers linkable-line-numbers"}
"build": {
  "setup": "./setup.sh",                  // optional - command to install your build dependencies
  "build": "./build.sh",                  // command that will build your module
  "path" : "dist/archive.tar.gz",         // optional - path to your built module
                                          // (passed to the 'viam module upload' command)
  "arch" : ["linux/amd64", "linux/arm64"] // architecture(s) to build for
}
```

{{% expand "Click to view example setup.sh" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

{{% /expand %}}

{{%expand "Click to view example build.sh (with setup.sh)" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand %}}

{{% expand "Click to view example build.sh (without setup.sh)" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
set -e
UNAME=$(uname -s)

if [ "$UNAME" = "Linux" ]
then
    echo "Installing venv on Linux"
    sudo apt-get install -y python3-venv
fi
if [ "$UNAME" = "Darwin" ]
then
    echo "Installing venv on Darwin"
    brew install python3-venv
fi

python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{{% /expand%}}

<!-- { {% /tab %}} -->
<!-- { {% tab name="Platform Specific" %}}

```json {class="line-numbers linkable-line-numbers"}
"build": {
  "path" : "dist/archive.tar.gz",               // optional - path to your built module
                                                // (passed to the 'viam module upload' command)
  "arch": {
        "linux/arm64": {
          "build": "./build-linux-arm64.sh" // command that will build your module
        },
        "darwin/arm64": {
          "build": "./build-darwin-arm64.sh" // command that will build your module
        }
      } // architecture(s) to build for
}
```

{ {%expand "Click to view example build-linux-arm64.sh" %}}

```sh { class="command-line"}
#!/bin/bash
set -e

sudo apt-get install -y python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{ {% /expand%}}

{ {%expand "Click to view example build-darwin-arm64.sh" %}}

```sh {class="line-numbers linkable-line-numbers"}
#!/bin/bash
set -e

brew install python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
```

{ {% /expand%}}

{{ % /tab %}}
{ {< /tabs >}} -->

For example, the following extends the `my-module` <file>meta.json</file> file using the single build file approach, adding a new `build` object to control its build parameters when used with `module build start` or `module build local`:

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/<my-repo-name>/my-module",
  "description": "An example custom module.",
  "build": {
    "setup": "./setup.sh",
    "build": "./build.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  },
  "entrypoint": "<PATH-TO-EXECUTABLE>"
}
```

When you initiate a build job using either `start` or `local`, the command returns the build ID of your job.
Provide that build ID to the `module build logs` command to show the relevant build logs for that build.

For example, use the following to initiate a build, and return the build logs as soon as it completes:

```sh {class="command-line" data-prompt="$"}
viam module build logs --wait --build-id=$(viam module build start --version "0.1.2")
```

To list all in-progress builds and their build status, use the following command:

```sh {class="command-line" data-prompt="$"}
viam module build list
```

## `organizations`

The `organizations` command allows you to list the organizations your authenticated session has access to, and to create a new organization API key.

```sh {class="command-line" data-prompt="$"}
viam organizations list
viam organizations api-key create --org-id=<org-id> [--name=<key-name>]
viam organizations support-email [get | set] --org-id=<org-id> --support-email=<support-email>
viam organizations logo [get | set] --org-id=<org-id> [--logo-path=<logo-path>]
viam organizations firebase-config [set | read | delete] --org-id=<org-id> [--app-id=<app-id>] [--firebase-config-path=<path>]
viam organizations billing-service get-config --org-id=<org-id>
viam organizations billing-service [enable | update] --org-id=<org-id> --address=<address>
viam organizations billing-service disable --org-id=<org-id>
viam organization auth-service [enable | disable] --org-id=<org-id>
viam organization auth-service oauth-app [create | update] --client-authentication [required | unspecified | not_required | not_required_when_using_pkce] \
    --client-name <client-name> --enabled-grants [password | unspecified | refresh_token | implicit | device_code | authorization_code] \
    --logout-uri=https://logoipsum.com --origin-uris=https://logoipsum.com \
    --pkce=[required | not_required | unspecified] --redirect-uris=https://logoipsum.com/callback \
    --url-validation=[allow_wildcards | unspecified | exact_match] --org-id=<org-id>
viam organization auth-service oauth-app [list] --org-id=<org-id>
viam organization auth-service oauth-app [read | delete] --org-id=<org-id> --client-id=<client-id>
```

See [Manage API keys](/cli/administer-your-organization/#manage-api-keys) for more information.

### `organizations list`

List all organizations (name, ID, and [namespace](/build-modules/module-reference/)) that the authenticated session has access to.

```sh {class="command-line" data-prompt="$"}
# list all the organizations that you are currently authenticated to
viam organizations list
```

### `organizations api-key create`

Create a new organization API key.

```sh {class="command-line" data-prompt="$"}
# create a new organization API key in org 123
viam organizations api-key create --org-id=123 --name=my-key
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to create the API key in. | **Required** |
| `--name` | The optional name for the organization API key. If omitted, a name will be auto-generated based on your login info and the current time. | Optional |

### `organizations support-email get`

Get the support email for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations support-email get --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |

### `organizations support-email set`

Set the support email for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations support-email set --org-id=<org-id> --support-email=<support-email>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |
| `--support-email` | The support email to set for the organization. | **Required** |

### `organizations logo set`

Upload the logo for an organization from a local file.

```sh {class="command-line" data-prompt="$"}
viam organizations logo set --org-id=<org-id> --logo-path=<logo-path>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |
| `--logo-path` | Path to the logo file to upload. Must be a PNG file. | **Required** |

### `organizations logo get`

Get the logo for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations logo get --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to get the logo for. | **Required** |

### `organizations firebase-config set`

Upload a Firebase config JSON for a specific app ID. Organization owner only.

```sh {class="command-line" data-prompt="$"}
viam organizations firebase-config set --org-id=<org-id> --app-id=com.example.myapp --firebase-config-path=./firebase-config.json
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | Organization ID. | **Required** |
| `--app-id` | App ID. For example, `com.example.myapp`. | **Required** |
| `--firebase-config-path` | Path to the Firebase config JSON file. | **Required** |

### `organizations firebase-config read`

Read Firebase config metadata for an organization. Organization owner only.

```sh {class="command-line" data-prompt="$"}
viam organizations firebase-config read --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | Organization ID. | **Required** |

### `organizations firebase-config delete`

Delete a Firebase config for a specific app ID. Organization owner only.

```sh {class="command-line" data-prompt="$"}
viam organizations firebase-config delete --org-id=<org-id> --app-id=com.example.myapp
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | Organization ID. | **Required** |
| `--app-id` | App ID. For example, `com.example.myapp`. | **Required** |

### `organizations billing-service get-config`

Get the billing service config for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service get-config --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |

### `organizations billing-service enable`

Enable the billing service for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service enable --org-id=<org-id> --address=<address>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |
| `--address` | The stringified billing address that follows the pattern: line1, line2 (optional), city, state, zipcode. | **Required** |

### `organizations billing-service update`

Update the billing service for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service update --org-id=<org-id> --address=<address>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |
| `--address` | The stringified billing address that follows the pattern: line1, line2 (optional), city, state, zipcode. | **Required** |

### `organizations billing-service disable`

Disable the billing service for an organization.

```sh {class="command-line" data-prompt="$"}
viam organizations billing-service disable --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |

### `organizations auth-service enable`

Enable auth-service for OAuth applications.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service enable --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |

### `organizations auth-service disable`

Disable auth-service for OAuth applications. Disabling the auth-service does not delete your OAuth token, it will just take off the custom branding.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service disable --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |

### `organizations auth-service oauth-app create`

Create a new OAuth application.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service oauth-app create --client-authentication=<policy> --client-name=<name> --enabled-grants=<grants> --logout-uri=<uri> --origin-uris=<uris> --pkce=<pkce> --redirect-uris=<uris> --url-validation=<validation> --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID that is tied to the OAuth application. | **Required** |
| `--client-authentication` | The client authentication policy for the OAuth application. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_pkce`. | **Required** |
| `--enabled-grants` | Comma-separated enabled grants for the OAuth application. Options: `unspecified`, `refresh_token`, `password`, `implicit`, `device_code`, `authorization_code`. | **Required** |
| `--logout-uri` | The logout URI for the OAuth application. | **Required** |
| `--pkce` | Proof Key for Code Exchange (PKCE) for the OAuth application. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_client_authentication`. | **Required** |
| `--redirect-uris` | Comma-separated redirect URIs for the OAuth application. Requires at least one. | **Required** |
| `--url-validation` | URL validation for the OAuth application. Options: `unspecified`, `exact_match`, `allow_wildcards`. | **Required** |
| `--client-name` | The name for the OAuth application. | Optional |
| `--origin-uris` | Comma-separated origin URIs for the OAuth application. | Optional |
| `--invite-redirect-uri` | Redirect URI to send users after they accept an org invite. | Optional |

### `organizations auth-service oauth-app update`

Update an existing OAuth application.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service oauth-app update --org-id=<org-id> --client-id=<client-id> [other options]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID that is tied to the OAuth application. | **Required** |
| `--client-id` | The client ID of the OAuth application to be updated. | **Required** |
| `--client-name` | Updated name for the OAuth application. | Optional |
| `--client-authentication` | Updated client authentication policy. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_pkce`. Default: `unspecified`. | Optional |
| `--enabled-grants` | Updated comma-separated enabled grants. Options: `unspecified`, `refresh_token`, `password`, `implicit`, `device_code`, `authorization_code`. | Optional |
| `--logout-uri` | Updated logout URI for the OAuth application. | Optional |
| `--origin-uris` | Updated comma-separated origin URIs for the OAuth application. | Optional |
| `--pkce` | Updated PKCE policy. Options: `unspecified`, `required`, `not_required`, `not_required_when_using_client_authentication`. Default: `unspecified`. | Optional |
| `--redirect-uris` | Updated comma-separated redirect URIs for the OAuth application. | Optional |
| `--url-validation` | Updated URL validation. Options: `unspecified`, `exact_match`, `allow_wildcards`. Default: `unspecified`. | Optional |
| `--invite-redirect-uri` | Redirect URI to send users after they accept an org invite. | Optional |

### `organizations auth-service oauth-app list`

List OAuth applications for an organization.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service oauth-app list --org-id=<org-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |

### `organizations auth-service oauth-app read`

Read an OAuth application.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service oauth-app read --org-id=<org-id> --client-id=<client-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |
| `--client-id` | The client ID of the OAuth application. | **Required** |

### `organizations auth-service oauth-app delete`

Delete an OAuth application.

```sh {class="command-line" data-prompt="$"}
viam organization auth-service oauth-app delete --org-id=<org-id> --client-id=<client-id>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization to perform the command on. | **Required** |
| `--client-id` | The client ID of the OAuth application. | **Required** |

## `packages`

The `packages` command allows you to upload packages to the Viam Cloud or export packages from the Viam Cloud.
For example, you can use this command to download ML models or modules from the registry.

```sh {class="command-line" data-prompt="$"}
viam packages upload --path=<path-to-package.tar.gz> --org-id=<org-id> --name=<package-name> --version=<version> --type=<type>
viam packages export --type=<type> [--org-id=<org-id>] [--name=<package-name>] [--version=<version>] [--destination=<path-to-export-destination>]
```

### `packages upload`

Upload a package to the Viam Cloud.

```sh {class="command-line" data-prompt="$"}
viam packages upload --path=./the_package.tar.gz --org-id=123 --name=MyMLModel --version=1.0.0 --type=ml_model --model-framework=tensorflow
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--path` | The path to the package for upload. Executable or zipped tar with the `.tar.gz` extension. | **Required** |
| `--org-id` | The organization ID of the package. | **Required** |
| `--name` | The name of the package. | **Required** |
| `--version` | The version of the package or `latest`. | **Required** |
| `--type` | The type of the package: `ml_model`, `archive`, `module`, `slam_map`, or `unspecified`. | **Required** |
| `--model-framework` | The framework for an uploaded `ml_model`. Valid options: `unspecified`, `tflite`, `tensorflow`, `pytorch`, or `onnx`. | Required if `--type=ml_model` |
| `--model-type` | The type of the model. Valid options: `unspecified`, `single_label_classification`, `multi_label_classification`, `object_detection`. | Required if `--type=ml_model` |

### `packages export`

Download a package from the Viam Cloud.

```sh {class="command-line" data-prompt="$"}
viam packages export --type=ml_model --org-id=123 --name=MyMLModel --version=latest --destination=.
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--type` | The type of the package: `ml_model`, `archive`, `module`, `slam_map`, or `unspecified`. | **Required** |
| `--org-id` | The organization ID or namespace of the package. Default: `default-org` value if set, else attempts to read from <file>meta.json</file>. | Optional |
| `--name` | The name of the package. Default: attempts to read from <file>meta.json</file>. | Optional |
| `--version` | The version of the package or `latest`. Default: `latest`. | Optional |
| `--destination` | The output directory for downloaded package. Default: `.`. | Optional |

## `parse-ftdc`

The `parse-ftdc` command parses an FTDC (Full-Time Diagnostic Data Capture) file and opens an interactive REPL for inspecting performance metrics collected by `viam-server`.
This is a diagnostic tool. Viam support may ask you to run it when troubleshooting performance issues.

```sh {class="command-line" data-prompt="$"}
viam machines part get-ftdc --part=<part-id> ftdc-data
viam parse-ftdc --path ftdc-tmp/<part-id>/viam-server-<date>-<time>.ftdc
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--path` | The absolute file path to the FTDC file. | **Required** |

## `profiles`

The `profiles` command allows you to manage different CLI authentication profiles, so you can easily switch between API key authentications (for example authentication to one organization versus another).

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name=<name-of-profile-to-add> --key-id=<API-key-ID> --key=<API-key>
viam profiles update --profile-name=<name-of-profile-to-update> --key-id=<API-key-ID> --key=<API-key>
viam profiles list
viam profiles remove --profile-name=<name-of-profile-to-remove>
```

Examples:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
# Add a new profile for authentication (throws error if profile already exists)
viam profiles add --profile-name=mycompany --key-id=54321zyx --key=123abcd1234

# Update an existing profile for authentication, or add it if it doesn't exist
viam profiles update --key=123abcd1234 --key-id=54321zyx --profile-name=mycompany

# List all existing profiles by name
viam profiles list

# Remove a profile
viam profiles remove --profile-name=mycompany

# Example of using a profile to see a list of machines available to that profile
viam --profile=mycompany machines list
```

See [Manage API keys](/cli/administer-your-organization/#manage-api-keys) for more information.

{{% alert title="Tip" color="tip" %}}
You can set a default profile by using the `VIAM_CLI_PROFILE_NAME` environment variable.
{{% /alert %}}

### `profiles add`

Add a new profile for authentication. Throws an error if the profile already exists.

```sh {class="command-line" data-prompt="$"}
viam profiles add --profile-name=<name-of-profile-to-add> --key-id=<API-key-ID> --key=<API-key>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--profile-name` | Name of the profile to add. | **Required** |
| `--key-id` | The `key id` (UUID) of the API key. | **Required** |
| `--key` | The `key value` of the API key. | **Required** |

### `profiles update`

Update an existing profile for authentication, or add it if it doesn't exist.

```sh {class="command-line" data-prompt="$"}
viam profiles update --profile-name=<name-of-profile-to-update> --key-id=<API-key-ID> --key=<API-key>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--profile-name` | Name of the profile to update. | **Required** |
| `--key-id` | The `key id` (UUID) of the API key. | **Required** |
| `--key` | The `key value` of the API key. | **Required** |

### `profiles list`

List all existing profiles by name.

```sh {class="command-line" data-prompt="$"}
viam profiles list
```

### `profiles remove`

Remove a profile.

```sh {class="command-line" data-prompt="$"}
viam profiles remove --profile-name=<name-of-profile-to-remove>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--profile-name` | Name of the profile to remove. | **Required** |

## `resource`

The `resource` command enables, disables, or updates individual resources (components and services) on a machine part. Use it to temporarily disable a resource without removing it from the configuration, or to update attributes without using the Viam app.

```sh {class="command-line" data-prompt="$"}
viam resource enable --part=<part> --resource-name=<resource-name> [--resource-name=<resource-name> ...]
viam resource disable --part=<part> --resource-name=<resource-name> [--resource-name=<resource-name> ...]
viam resource update --part=<part> --resource-name=<resource-name> --config=<json-or-path>
```

Examples:

```sh {class="command-line" data-prompt="$"}
# enable a single resource
viam resource enable --part=abc123 --resource-name=my-sensor

# enable multiple resources at once
viam resource enable --part=abc123 --resource-name=my-sensor --resource-name=arm-1

# update a resource attribute inline
viam resource update --part=abc123 --resource-name=my-sensor --config='{"pin": "38"}'

# update from a JSON file
viam resource update --part=abc123 --resource-name=my-sensor --config=/path/to/updates.json

# delete an attribute by passing an empty value
viam resource update --part=abc123 --resource-name=my-sensor --config='{"pin": ""}'
```

### `resource enable`

Enable one or more resources on a machine part.

```sh {class="command-line" data-prompt="$"}
viam resource enable --part=<part> --resource-name=<resource-name> [--resource-name=<resource-name> ...]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Machine part ID or name. | **Required** |
| `--resource-name` | Name of the resource. Repeat the flag to apply `enable` to multiple resources at once. | **Required** |
| `--organization` | Organization ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--location` | Location ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--machine` | Machine ID or name. Required when using a name (rather than ID) to identify the part. | Optional |

### `resource disable`

Disable one or more resources on a machine part. Disabled resources are not started by viam-server.

```sh {class="command-line" data-prompt="$"}
viam resource disable --part=<part> --resource-name=<resource-name> [--resource-name=<resource-name> ...]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Machine part ID or name. | **Required** |
| `--resource-name` | Name of the resource. Repeat the flag to apply `disable` to multiple resources at once. | **Required** |
| `--organization` | Organization ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--location` | Location ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--machine` | Machine ID or name. Required when using a name (rather than ID) to identify the part. | Optional |

### `resource update`

Replace a resource's attributes with new values. The `--config` flag accepts inline JSON or a path to a JSON file. An empty JSON object deletes all attributes.

```sh {class="command-line" data-prompt="$"}
viam resource update --part=<part> --resource-name=<resource-name> --config=<json-or-path>
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Machine part ID or name. | **Required** |
| `--resource-name` | Name of the resource. | **Required** |
| `--config` | Inline JSON or path to a JSON file containing the new attributes. | **Required** |
| `--organization` | Organization ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--location` | Location ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--machine` | Machine ID or name. Required when using a name (rather than ID) to identify the part. | Optional |

## `train`

Use a training script to train an ML model on data.

```sh {class="command-line" data-prompt="$"}
viam train submit managed --dataset-id=<dataset-id> --model-org-id=<model-org-id> --model-name=<model-name> --model-type=<model-type> --model-labels=<model-labels> [...named args]
viam train submit custom from-registry --dataset-id=<dataset-id> --org-id=<org-id> --model-name=<model-name> --script-name=<script-name> --version=<version> --args=<arg-key>=<arg-value> [...named args]
viam train submit custom with-upload --dataset-id=<dataset-id> --org-id=<org-id> --model-name=<model-name> --path=<path> --script-name=<script-name> --args=<arg-key>=<arg-value> [...named args]
viam train get --job-id=<job-id>
viam train logs --job-id=<job-id>
viam train cancel --job-id=<job-id>
viam train list --org-id=<org-id> --job-status=<job-status>
viam train containers list
```

### `train submit managed`

Submit a training job on data in the Viam Cloud with a Viam-managed training script.

```sh {class="command-line" data-prompt="$"}
# submit training job on data in Viam Cloud with a Viam-managed training script
viam train submit managed --dataset-id=456 --model-org-id=123 --model-name=MyCoolClassifier --model-type=single_label_classification --model-labels=1,2,3
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | The ID of the dataset to train on. To find the dataset ID of a given dataset, go to the [**DATASETS** subtab](https://app.viam.com/data/datasets) of the **DATA** tab and select a dataset. Click **...** in the left-hand menu and click **Copy dataset ID**. | **Required** |
| `--model-org-id` | The organization ID to train and save the ML model in. You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/). | **Required** |
| `--model-name` | The name of the ML model. | **Required** |
| `--model-type` | Type of model to train. Must be one of `single_label_classification`, `multi_label_classification`, or `object_detection`. | **Required** |
| `--model-framework` | The framework of model to train. Must be one of `tflite` or `tensorflow`. | **Required** |
| `--model-labels` | Labels to train on. These will either be classification or object detection labels. | **Required** |
| `--model-version` | Set the version of the submitted model. Defaults to current timestamp if unspecified. | Optional |

### `train submit custom from-registry`

Submit a custom training job with an existing training script in the registry on data in the Viam Cloud.

```sh {class="command-line" data-prompt="$"}
# submit custom training job with an existing training script in the Registry on data in Viam Cloud
viam train submit custom from-registry --dataset-id=<INSERT DATASET ID> --org-id=<INSERT ORG ID> --model-name=MyRegistryModel --model-version=2 --version=1 --script-name=mycompany:MyCustomTrainingScript  --args=num_epochs=3,model_type=multi_label
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | The ID of the dataset to train on. | **Required** |
| `--org-id` | The organization ID to train and save the ML model in. | **Required** |
| `--model-name` | The name of the ML model. | **Required** |
| `--script-name` | The registry name of the ML training script to use for training. | **Required** |
| `--version` | The version of the ML training script to use for training. | **Required** |
| `--container-version` | Docker container version for training. Use `viam train containers list` to see available versions. | **Required** |
| `--model-version` | Set the version of the submitted model. Defaults to current timestamp if unspecified. | Optional |
| `--args` | Pass custom comma-separated arguments to the training script. Example: `num_epochs=3,model_type=multi_label`. To include whitespace, enclose the value with whitespace in single and double quotes. Example: `num_epochs=3,labels="'green_square blue_star'"`. | Optional |

### `train submit custom with-upload`

Upload a draft training script and submit a custom training job on data in the Viam Cloud.

```sh {class="command-line" data-prompt="$"}
# submit custom training job with an uploaded training script on data in Viam Cloud
viam train submit custom with-upload --dataset-id=<INSERT DATASET ID> --model-org-id=<INSERT ORG ID> --model-name=MyRegistryModel --model-type=single_label_classification --model-version=2 --version=1 --path=<path-to-tar.gz> --script-name=mycompany:MyCustomTrainingScript --args=num_epochs=3,labels="'green_square blue_star'"
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--dataset-id` | The ID of the dataset to train on. | **Required** |
| `--model-org-id` | The organization ID to train and save the ML model in. | **Required** |
| `--model-name` | The name of the ML model. | **Required** |
| `--script-name` | The registry name of the ML training script to use for training. This sets the name on upload. | **Required** |
| `--version` | The version of the ML training script to use for training. | **Required** |
| `--path` | The path to the ML training script to upload. | **Required** |
| `--framework` | Framework of the ML training script to upload, can be `tflite`, `tensorflow`, `pytorch`, or `onnx`. | **Required** |
| `--container-version` | Docker container version for training. Use `viam train containers list` to see available versions. | **Required** |
| `--model-type` | Type of model to train. Must be one of `single_label_classification`, `multi_label_classification`, `object_detection`, or `unspecified`. | Optional |
| `--model-version` | Set the version of the submitted model. Defaults to current timestamp if unspecified. | Optional |
| `--url` | URL of the GitHub repository associated with the training scripts. | Optional |
| `--args` | Pass custom comma-separated arguments to the training script. Example: `num_epochs=3,model_type=multi_label`. To include whitespace, enclose the value with whitespace in single and double quotes. Example: `num_epochs=3,labels="'green_square blue_star'"`. | Optional |

### `train get`

Get a training job from the Viam Cloud based on training job ID.

```sh {class="command-line" data-prompt="$"}
# get a training job from Viam Cloud based on training job ID
viam train get --job-id=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--job-id` | The ID of the training job to get. You can retrieve this value with `train list`. | **Required** |

### `train logs`

Get the logs of a training job from the Viam Cloud based on training job ID.

```sh {class="command-line" data-prompt="$"}
# get training job logs from Viam Cloud based on training job ID
viam train logs --job-id=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--job-id` | The ID of the training job to get logs for. | **Required** |

### `train cancel`

Cancel a training job in the Viam Cloud based on training job ID.

```sh {class="command-line" data-prompt="$"}
# cancel training job in Viam Cloud based on training job ID
viam train cancel --job-id=123
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--job-id` | The ID of the training job to cancel. | **Required** |

### `train list`

List training jobs in Viam Cloud based on organization ID and job status.

```sh {class="command-line" data-prompt="$"}
# list training jobs in Viam Cloud based on organization ID and job status
viam train list --org-id=123 --job-status=completed
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID to list training jobs from. | **Required** |
| `--job-status` | Training status to filter for. Can be one of `canceled`, `canceling`, `completed`, `failed`, `in_progress`, `pending`, or `unspecified`. | Optional |

### `train containers list`

List supported Docker container images for custom training.

```sh {class="command-line" data-prompt="$"}
viam train containers list
```

## `training-script`

Manage training scripts for [custom ML training](/train/custom-training-scripts/).

```sh {class="command-line" data-prompt="$"}
viam training-script upload --framework=<framework> --org-id=<org-id> --path=<path-to-script> --script-name=<script-name> --type=<type>
viam training-script update --org-id=<org-id> --script-name=<script-name> --visibility=<visibility>
```

### `training-script upload`

Upload an ML training script to the registry.

```sh {class="command-line" data-prompt="$"}
# upload a single label classification script in the tflite framework to organization 123
viam training-script upload --framework=tflite --org-id=123 --path=. --script-name=MyCustomTrainingScript --type=single_label_classification
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--path` | The path to ML training scripts for upload. | **Required** |
| `--org-id` | The organization ID to host the scripts in. You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/). | **Required** |
| `--script-name` | Name of the ML training script to upload. | **Required** |
| `--version` | Version of the ML training script to upload. | Optional |
| `--framework` | Framework of the ML training script to upload, can be `tflite`, `tensorflow`, `pytorch`, or `onnx`. | Optional |
| `--url` | URL of GitHub repository associated with the training script. | Optional |
| `--type` | Task type of the ML training script to upload, can be `single_label_classification`, `multi_label_classification`, or `object_detection`. | Optional |
| `--draft` | Indicate draft mode, drafts are not viewable in the registry. | Optional |

### `training-script update`

Update the visibility of an ML training script in the registry.

```sh {class="command-line" data-prompt="$"}
# update MyCustomTrainingScript with public visibility
viam training-script update --org-id=123 --script-name=MyCustomTrainingScript --visibility=public --description="A single label classification training script"
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--org-id` | The organization ID hosting the script. You can find your organization ID by running `viam organizations list` or by visiting your organization's **Settings** page in the [Viam app](https://app.viam.com/). | **Required** |
| `--script-name` | Name of the ML training script to update. | **Required** |
| `--visibility` | Visibility of the registry item, can be `public`, `private`, or `draft`. | **Required** |
| `--description` | Description of the ML training script. | Optional |

## `traces`

The `traces` command imports viam-server trace files to an OTLP endpoint or prints them to the console. Use it to debug machine performance and request flow with a tracing backend such as Jaeger or Tempo.

The `import-remote`, `print-remote`, and `get-remote` subcommands require the machine to have a valid shell-type service. Organization and location are required if you are identifying the part by name rather than ID.

```sh {class="command-line" data-prompt="$"}
viam traces import-local <traces-file> [--endpoint=<host:port>]
viam traces import-remote --part=<part> [--endpoint=<host:port>] [--organization=<org>] [--location=<location>]
viam traces print-local <traces-file>
viam traces print-remote --part=<part> [--organization=<org>] [--location=<location>]
viam traces get-remote --part=<part> [target] [--organization=<org>] [--location=<location>]
```

### `traces import-local`

Import traces from a local viam-server trace file to an OTLP endpoint.

```sh {class="command-line" data-prompt="$"}
viam traces import-local <traces-file> [--endpoint=<host:port>]
```

Pass the path to a local viam-server trace file as a positional argument.

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--endpoint` | OTLP endpoint in `host:port` format. Default: `localhost:4317`. | Optional |

### `traces import-remote`

Import traces from a remote machine to an OTLP endpoint.

```sh {class="command-line" data-prompt="$"}
viam traces import-remote --part=<part> [--endpoint=<host:port>] [--organization=<org>] [--location=<location>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Machine part ID or name. | **Required** |
| `--endpoint` | OTLP endpoint in `host:port` format. Default: `localhost:4317`. | Optional |
| `--organization` | Organization ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--location` | Location ID or name. Required when using a name (rather than ID) to identify the part. | Optional |

### `traces print-local`

Print traces from a local trace file to the console.

```sh {class="command-line" data-prompt="$"}
viam traces print-local <traces-file>
```

Pass the path to a local viam-server trace file as a positional argument.

### `traces print-remote`

Print traces from a remote machine to the console.

```sh {class="command-line" data-prompt="$"}
viam traces print-remote --part=<part> [--organization=<org>] [--location=<location>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Machine part ID or name. | **Required** |
| `--organization` | Organization ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--location` | Location ID or name. Required when using a name (rather than ID) to identify the part. | Optional |

### `traces get-remote`

Download traces from a remote machine to a local file. If `[target]` is omitted, the file is saved to the current working directory.

```sh {class="command-line" data-prompt="$"}
viam traces get-remote --part=<part> [target] [--organization=<org>] [--location=<location>]
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--part` | Machine part ID or name. | **Required** |
| `--organization` | Organization ID or name. Required when using a name (rather than ID) to identify the part. | Optional |
| `--location` | Location ID or name. Required when using a name (rather than ID) to identify the part. | Optional |

## `update`

The `update` command updates the CLI to the latest version.
If the CLI was installed with Homebrew, it updates through Homebrew.
Otherwise, it downloads and replaces the binary directly.

```sh {class="command-line" data-prompt="$"}
viam update
```

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--no-progress` | Hide progress output during the update. Default: `false`. | Optional |

## `version`

The `version` command returns the version of the Viam CLI.
To update to the latest version of the CLI, run [`viam update`](#update).

```sh {class="command-line" data-prompt="$"}
viam version
```

## `whoami`

The `whoami` command returns the Viam user for an authenticated CLI session, or "Not logged in" if there is no authenticated session.

```sh {class="command-line" data-prompt="$"}
viam whoami
```

## `xacro`

The `xacro` command converts ROS xacro files to URDF using a Docker container. Use it to integrate ROS-based robot descriptions with Viam's frame system.

```sh {class="command-line" data-prompt="$"}
viam xacro convert --input-file=<file> --output-file=<file> [other options]
```

Examples:

```sh {class="command-line" data-prompt="$"}
# basic conversion
viam xacro convert --input-file=robot.xacro --output-file=robot.urdf

# pass xacro arguments
viam xacro convert --input-file=arm.xacro --output-file=arm.urdf --args=name:=ur20

# collapse fixed-joint chains so only one end effector exists
viam xacro convert --input-file=robot.xacro --output-file=robot.urdf --collapse-fixed-joints
```

### `xacro convert`

Convert a xacro file to URDF.

<!-- prettier-ignore -->
| Argument | Description | Required? |
| -------- | ----------- | --------- |
| `--input-file` | Path to the xacro file to expand. | **Required** |
| `--output-file` | Path where the URDF file will be written. | **Required** |
| `--args` | xacro arguments to pass through, in the form `name:=value`. Repeat the flag for multiple arguments. Required if the xacro file uses `<xacro:arg>` tags. | Optional |
| `--ros-distro` | ROS distribution to use. Auto-detected from the docker image if not specified. | Optional |
| `--docker-image` | Docker image to use for xacro processing. Default: `osrf/ros:humble-desktop`. | Optional |
| `--package-xml` | Path to `package.xml` if not in the current directory. | Optional |
| `--collapse-fixed-joints` | Collapse fixed-joint chains to ensure only one end effector exists. | Optional |
| `--install-packages` | Install `ros-<distro>-xacro` in the container (required for the default image). Disable only if your custom image already includes xacro. | Optional |
| `--dry-run` | Show the docker command without executing it. | Optional |
