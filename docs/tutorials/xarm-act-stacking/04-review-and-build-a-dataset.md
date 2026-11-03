---
title: "Phase 4: Review and build a dataset"
linkTitle: "4. Review and build a dataset"
type: "docs"
slug: "review-and-build-a-dataset"
weight: 40
description: "Review your recorded episodes, tag the keepers, and collect them into a sequence dataset for training."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 4
phase_total: 7
time_estimate: "30 minutes"
prev: "/tutorials/xarm-act-stacking/record-demonstrations/"
next: "/tutorials/xarm-act-stacking/train-a-policy/"
languages: ["python"]
capabilities: ["sequences", "datasets", "viam-apps", "docs"]
diataxis: tutorial
draft: true
---

You recorded about 50 episodes. Now you decide which ones the policy learns from. You watch each episode in the capture-control webapp and tag it as a keeper or a discard. Then you collect the keepers into a sequence dataset named `xarm-stacking-v1`.

## Why review

A few bad episodes cost more than they add. A dropped block, a long pause, or a camera dropout all become training data. ACT (Action Chunking with Transformers) learns hesitation as readily as skill, so a policy trained on a pause will pause. Thirty clean episodes beat fifty mixed ones.

## Review in the webapp

Open the capture-control webapp and use one of these:

- **Review session** lists the episodes from the session you just ended, as they sync.
- **Episodes** opens the same player for this machine's past episodes. Filter by task, session, and review status.

Each episode plays its camera frames in real time. Press **K** to tag the episode `review:keep` or **D** to tag it `review:discard`. The app then jumps to the next episode you haven't reviewed.

Nothing is deleted. An episode with neither tag counts as not reviewed.

A sequence can appear before all its frames have synced. **K** and **D** unlock once the frames have caught up. If no new frames arrive for 15 seconds, the app marks the episode partial. Discard partial episodes.

| Key       | Action                                                  |
| --------- | ------------------------------------------------------- |
| **K / D** | Keep or discard, then go to the next unreviewed episode |
| **← / →** | Previous or next episode                                |
| **Space** | Play or pause                                           |
| **, / .** | Step one frame                                          |
| **Esc**   | Close review                                            |

<!-- ASSET webapp-review (SCREENSHOT): the capture-control webapp's review player showing an episode, the playback controls, and the keep and discard buttons -->

## What to discard

Discard an episode if any of these happened:

- The stack failed, or a block was knocked over.
- The arm paused for a long time.
- The gripper re-grasped the block.
- The arm left the camera frame.
- The episode is partial.

When in doubt, discard it. You can always record more.

## Create the sequence dataset

Collect every sequence tagged `review:keep` into a new sequence dataset named `xarm-stacking-v1`. Dataset names must be unique in your organization.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **DATA** tab, click **DATASETS**.
2. Click **Create dataset**.
3. In the **Dataset Name** field, enter `xarm-stacking-v1`.
4. Set **Data type** to **Sequence Data**, and click **Create dataset** again.
5. Open the dataset and click **Add Data**.
6. In the **All sequences** dialog, select the sequences tagged `review:keep` and click **Add**.

<!-- TODO(dep): confirm the All sequences dialog can filter by sequence tag, so you can select all review:keep sequences at once -->

The dataset's sidebar shows how many sequences it holds.

{{% /tab %}}
{{% tab name="CLI and Python" %}}

`viam dataset create` can't set a dataset's type yet, so this path uses the Python SDK. The script lists every sequence in your organization, keeps the ones tagged `review:keep`, creates the dataset, and adds them. Save this as `create_dataset.py`:

```python
import asyncio
import os

from viam.app.viam_client import ViamClient
from viam.proto.app.dataset import DatasetType
from viam.rpc.dial import DialOptions


async def main():
    client = await ViamClient.create_from_dial_options(
        DialOptions.with_api_key(
            os.environ["VIAM_API_KEY"], os.environ["VIAM_API_KEY_ID"]
        )
    )
    data = client.data_client

    sequence_ids = []
    page_token = None
    while True:
        sequences, page_token = await data.list_sequences(
            organization_id=os.environ["VIAM_ORG_ID"], page_token=page_token
        )
        for s in sequences:
            if s.part_id != os.environ["VIAM_PART_ID"]:
                continue
            if "review:keep" in s.sequence_tags:
                sequence_ids.append(s.id)
        if not page_token:
            break

    dataset_id = await data.create_dataset(
        name="xarm-stacking-v1",
        organization_id=os.environ["VIAM_ORG_ID"],
        type=DatasetType.DATASET_TYPE_SEQUENCE_DATA,
    )
    await data.add_sequences_to_dataset(
        dataset_id=dataset_id, sequence_ids=sequence_ids
    )
    print(f"{dataset_id}: {len(sequence_ids)} sequences")
    client.close()


asyncio.run(main())
```

Set `VIAM_API_KEY`, `VIAM_API_KEY_ID`, `VIAM_ORG_ID`, and `VIAM_PART_ID` to your machine's values, then run it:

```sh {class="command-line" data-prompt="$"}
python create_dataset.py
```

Note the dataset ID it prints. You use it in the next section.

{{% /tab %}}
{{< /tabs >}}

For more on sequence datasets, see [Create a dataset](/train/create-a-dataset/).

{{< checkpoint >}}
The dataset `xarm-stacking-v1` exists, and its sequence count matches your keep count. Aim for at least 40 sequences.
{{< /checkpoint >}}

## Sanity-check the export (optional)

Export the dataset to a local folder and confirm that it holds one sequence per kept episode. Use the dataset ID from the dataset page or the script:

```sh {class="command-line" data-prompt="$"}
viam dataset export \
  --dataset-id=<dataset-id> \
  --destination=./xarm-stacking-v1 \
  --only-parquet
```

`--only-parquet` skips the images, so the export is small. It writes `<dataset-id>.zip` to the destination. `sequences.parquet` has one row per sequence. To count the rows, install `pandas` and `pyarrow` (`pip install pandas pyarrow`), then run:

```sh {class="command-line" data-prompt="$"}
python -c "import zipfile, pandas as pd; z = zipfile.ZipFile('xarm-stacking-v1/<dataset-id>.zip'); print(len(pd.read_parquet(z.open('sequences.parquet'))))"
```

The number should equal your keep count. This check is optional, and you can skip it. For every column in the export, see [Sequence dataset format](/train/sequence-dataset-format/).

{{< workshop-nav >}}
