---
title: "SLAM Service Background"
linkTitle: "SLAM Technical"
weight: 70
type: "docs"
draft: true
description: "Background and technical information for the Simultaneous Localization And Mapping (SLAM) service, its configuration, its functionality, and its interfaces."
tags: ["slam", "services"]
aliases:
  - "/internals/slam/"
# SMEs: Jeremy, Kat
---

{{< glossary_tooltip term_id="slam" text="SLAM" >}} is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.
At Viam, we want to offer our users an easy-to-use, intuitive method for interfacing with various SLAM algorithms that may be useful in their mission.

As of June 01, 2022, we support the following SLAM libraries:

[ORBSLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3)

## Current Architecture

The SLAM service in rdk (located in /rdk/service/slam) is a wrapper for the C++ SLAM libraries mentioned above.
It has three roles, interface with an executable C++ binary of the chosen library, start up a data process (if desired), and to pass GRPC requests/responses between servers.

<img src="/mobility/slam-service-arch.png"/>

### Data Generation

Coming soon!

TODO: Do we want to discuss that RGBD cameras produce a rgb and depth folder inside data?
--> Add an explanation of what kind of subfolders are created for the "mono" case and the "rgbd" case (that is rgb, and rgbd + depth).
Elaborate on what the user should keep in mind when creating & integrating their own slam libraries, and whether or not it is important for them to document the subfolders that are created.

<pre>
.
└──\(The Directory Defined in Config)
    ├── data
    ├── map
    └── config
</pre>

The implemented SLAM libraries rely on the filename to know when this data was generated and what sensor was used to collect it.
The format for the timestamp is currently (10 Oct 2022) `"2006-01-02T15_04_05.0000"`.
Please note, this will be updated soon to align with the conventions used by the datamanager service.

### **Interfacing with the C++ Binary**

### Interfacing with the C++ Binary

The SLAM binaries used are stored in <file>/usr/local/bin</file>.
If you wish to use an updated version, copy the new binary into this directory.
If you use an identical name for this new binary, you will not need to change the RDK SLAM code. If you use a new name for the binary, then it must be relinked in <file>services/slam/slamlibraries.go</file> in the BinaryLocation metadata.
Note: a new binary with a different name can be stored anywhere as long as it is included in your PATH.

## **RDK Config**

```json
"services": [
  {
    "attributes": {
      "algorithm": "cartographer",
      "data_dir": "<path_to_folder>",
      "sensors": ["rplidar"],
      "config_params": {
        "mode": "2d"
      },
      "map_rate_sec": 60,
      "data_rate_ms": 200,
      "input_file_pattern": "1:1000:1"
    },
    "name": "test",
    "type": "slam"
  }
]
```

### Required Attributes

**algorithm** (string): Name of the SLAM library/algorithm to be used.
Current options are cartographer or orbslamv3.

**data_dir** (string): This is the data directory used for saving input sensor/map data and output maps/visualizations.
It has an architecture consisting of three internal folders, config, data and map.
If these have not been provided, they will be created by the SLAM service.
The data in the data directory also dictate what type of SLAM will be run:

- If no map is provided in the data folder, the SLAM algorithm will generate a new map using all the provided data (PURE MAPPING MODE)

- If a map is found in the data folder, it will be used as a priori information for the SLAM run and only data generated after the map will be used.
  (PURE LOCALIZATION MODE/UPDATING MODE)

- If a map_rate_sec is provided, then the system will overlay new data on any given map (PURE MAPPING MODE/UPDATING MODE)

**Sensors** (string[]): Names of sensors which are input to SLAM

### Optional Attributes

**map_rate_sec** (int): Map generation rate for saving current state (in seconds).
The default value is 60.
If an integer is less or equal to 0 then SLAM is run in localization mode.

**data_rate_ms** (int): Data generation rate for collecting sensor data to be fed into SLAM (in milliseconds).
The default value is 200.
If 0, no new data is sent to the SLAM algorithm.

**input_file_pattern** (string): File glob describing how to ingest previously saved sensor data.
Must be in the form X:Y:Z where Z is how many files to skip while iterating between the start index, X and the end index Y.

{{% alert title="Info" color="info" %}}
X and Y are the file numbers since the most recent map data package in the data folder.
If nil, includes all previously saved data.
{{% /alert %}}

**port** (string): Port for SLAM gRPC server.
If running locally, this should be in the form `localhost:<PORT>`.
If no value is given a random available port will be assigned.

**config_params** (map[string] string): Parameters specific to the
inputted SLAM library.

### SLAM Library Attributes

`config_params` is a catch-all attribute for parameters that are unique to the in-use SLAM library.
`config_params` often deal with the internal algorithms being run and will affect such aspects as submap size, update rate, and details on how to perform feature matching, to name a few.

You can find details on which inputs you can include for the available libraries in the following sections.

#### OrbSLAM

OrbSLAM can perform sparse SLAM using monocular or RGB-D images (not stereo); this must be specified in the config_params (as "mono" or "rgbd").
In addition the follow variables can be added to fine-tune cartographer's algorithm, all of which are optional:

<table>
    <tr>
        <th style="width:25%">Parameter Mode</th>
        <th style="width:70%">Description - The Type of SLAM to Use</th>
        <th>Default:<br>
        RGBD, Mono</th>
    </tr>
    <tr>
        <td>orb_n_features</td>
        <td>ORB parameter. Number of features per image</td>
        <td>1200</td>
    </tr>
    <tr>
        <td>orb_scale_factor</td>
        <td>ORB parameter. Scale factor between levels in the scale
         pyramid</td>
        <td>1.2</td>
    </tr>
    <tr>
        <td>orb_n_levels</td>
        <td>ORB parameter. Number of levels in the scale pyramid</td>
        <td>8</td>
    </tr>
    <tr>
        <td>orb_n_ini_th_fast</td>
        <td>ORB parameter. Initial FAST threshold</td>
        <td>20</td>
    </tr>
    <tr>
        <td>orb_n_min_th_fast</td>
        <td>ORB parameter. Lower threshold if no corners detected</td>
        <td>7</td>
</table>

## Hardware Requirements

Forthcoming

## Installation

### Using an App Image

Coming soon!

### Manual Installation

Perform a git clone on the SLAM repository using the recursive install flag to allow the sub packages to be downloaded as well.

```sh {class="command-line" data-prompt="$"}
git clone --recurse-submodules git@github.com:viamrobotics/slam.git
```

#### ORBSLAM3 Setup

This setup documents the current process for getting ORBSLAM3 working locally on a Raspberry Pi.

##### Dependencies

The following are the required dependencies for building and running ORBSLAM3.
In addition you should ensure the most recent version of the orbslam submodule is located in your directory with

```sh {class="command-line" data-prompt="$"}
git submodule update --init --recursive
```

###### Pangolin - to setup run the following

```sh {class="command-line" data-prompt="$"}
git clone --recursive https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
./scripts/install_prerequisites.sh recommended
mkdir build && cd build
cmake ..
make -j4
sudo make install
```

###### OpenCV

```{class="command-line" data-prompt="$"}
sudo apt install libopencv-dev
```

###### Eigen

```{class="command-line" data-prompt="$"}
sudo apt install libeigen3-dev
```

###### gRPC

To setup gRPC, use the following command:

```{class="command-line" data-prompt="$"}
cd \~/slam/slam-libraries
mae pull-rdk
```

This command pulls a minimal copy of rdk and build c++ gRPC files off of our proto.

###### Other Dependencies

```{class="command-line" data-prompt="$"}
sudo apt install libssl-dev
sudo apt-get install libboost-all-dev
```

##### Building ORBSLAM3

To build ORBSLAM3 run

```{class="command-line" data-prompt="$"}
cd \~/slam/slam-libraries/viam-orb-slam
./build_orbslam.sh
```

Should the code fail the initial setup (your Pi freezes and requires a restart), change the _make -j\`nproc\`_ flags into _make -j2_

After building, use the following command to move the binary to `/usr/local/bin`:

```{class="command-line" data-prompt="$"}
sudo cp bin/orb_grpc_server /usr/local/bin
```

In addition, make sure the binary is added in SLAMlibraries.go for ORBSLAM3 in rdk.

Lastly, move the vocabulary file into your data directory.
You must do this whenever a new data directory will be used.

```{class="command-line" data-prompt="$"}
cp ORB_SLAM3/Vocabulary/ORBvoc.txt ~/YOUR_DATA_DIR/config
```

## Usage

### Creating an initial map

Coming soon!

### Pure localization on a priori map

Coming soon!

### Updating an a priori map

Coming soon!
