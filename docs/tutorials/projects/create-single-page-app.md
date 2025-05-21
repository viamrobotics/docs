---
title: "Create a Single Page App"
linkTitle: "Create a Single Page App"
weight: 45
type: "docs"
description: "Build and deploy a web application hosted by Viam."
tags: ["web", "single page app", "react", "module"]
difficulty: intermediate
time_to_complete: "1 hour"
---

This tutorial guides you through creating and deploying a Single Page App (SPA) with Viam. You'll build a simple React application that allows users to select a machine and view its camera feed.

## Prerequisites

- A Viam account with an organization that has a public namespace
- Node.js and npm installed on your development machine
- Basic familiarity with React
- A machine with a camera component configured in your Viam account

## Step 1: Create a React application

First, let's create a new React application using Create React App:

```bash
npx create-react-app viam-camera-viewer
cd viam-camera-viewer
```

## Step 2: Install dependencies

Install the Viam TypeScript SDK and other necessary dependencies:

```bash
npm install @viamrobotics/sdk react-router-dom
```

## Step 3: Create the application structure

Let's create a simple application with the following pages:

1. Home page - For selecting organization, location, and machine
2. Machine page - For viewing the selected machine's camera feed

Create the following folder structure:

```
src/
├── components/
│   ├── OrganizationSelector.js
│   ├── LocationSelector.js
│   ├── MachineSelector.js
│   └── CameraViewer.js
├── pages/
│   ├── HomePage.js
│   └── MachinePage.js
├── App.js
└── index.js
```

## Step 4: Implement the components

Let's implement each component:

### OrganizationSelector.js

```jsx
import React, { useState, useEffect } from 'react';

function OrganizationSelector({ onSelect }) {
  const [organizations, setOrganizations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // In a real app, you would fetch organizations from the Viam API
    // This is a simplified example
    setOrganizations([
      { id: 'org1', name: 'My Organization' },
      { id: 'org2', name: 'Another Organization' }
    ]);
    setLoading(false);
  }, []);

  if (loading) return <div>Loading organizations...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h3>Select an Organization</h3>
      <select onChange={(e) => onSelect(e.target.value)}>
        <option value="">Select an organization</option>
        {organizations.map(org => (
          <option key={org.id} value={org.id}>{org.name}</option>
        ))}
      </select>
    </div>
  );
}

export default OrganizationSelector;
```

### LocationSelector.js

```jsx
import React, { useState, useEffect } from 'react';

function LocationSelector({ organizationId, onSelect }) {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!organizationId) {
      setLocations([]);
      setLoading(false);
      return;
    }

    // In a real app, you would fetch locations from the Viam API
    // This is a simplified example
    setLocations([
      { id: 'loc1', name: 'Home' },
      { id: 'loc2', name: 'Office' }
    ]);
    setLoading(false);
  }, [organizationId]);

  if (!organizationId) return null;
  if (loading) return <div>Loading locations...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h3>Select a Location</h3>
      <select onChange={(e) => onSelect(e.target.value)}>
        <option value="">Select a location</option>
        {locations.map(loc => (
          <option key={loc.id} value={loc.id}>{loc.name}</option>
        ))}
      </select>
    </div>
  );
}

export default LocationSelector;
```

### MachineSelector.js

```jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function MachineSelector({ locationId }) {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!locationId) {
      setMachines([]);
      setLoading(false);
      return;
    }

    // In a real app, you would fetch machines from the Viam API
    // This is a simplified example
    setMachines([
      { id: 'machine1', name: 'My Robot' },
      { id: 'machine2', name: 'Another Robot' }
    ]);
    setLoading(false);
  }, [locationId]);

  const handleMachineSelect = (machineId) => {
    if (machineId) {
      navigate(`/machine/${machineId}`);
    }
  };

  if (!locationId) return null;
  if (loading) return <div>Loading machines...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h3>Select a Machine</h3>
      <select onChange={(e) => handleMachineSelect(e.target.value)}>
        <option value="">Select a machine</option>
        {machines.map(machine => (
          <option key={machine.id} value={machine.id}>{machine.name}</option>
        ))}
      </select>
    </div>
  );
}

export default MachineSelector;
```

### CameraViewer.js

```jsx
import React, { useState, useEffect, useRef } from 'react';

function CameraViewer({ machineId }) {
  const [cameras, setCameras] = useState([]);
  const [selectedCamera, setSelectedCamera] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const imageRef = useRef(null);

  useEffect(() => {
    if (!machineId) {
      setCameras([]);
      setLoading(false);
      return;
    }

    // In a real app, you would fetch cameras from the Viam API
    // This is a simplified example
    setCameras([
      { id: 'camera1', name: 'Main Camera' },
      { id: 'camera2', name: 'Secondary Camera' }
    ]);
    setLoading(false);
  }, [machineId]);

  useEffect(() => {
    if (!selectedCamera) return;

    // In a real app, you would set up a stream from the Viam API
    // This is a simplified example
    const interval = setInterval(() => {
      // Simulate camera feed with a placeholder
      if (imageRef.current) {
        imageRef.current.src = `https://picsum.photos/800/600?random=${Date.now()}`;
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [selectedCamera]);

  const handleCameraSelect = (cameraId) => {
    setSelectedCamera(cameraId);
  };

  if (!machineId) return null;
  if (loading) return <div>Loading cameras...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h3>Camera Feed</h3>
      <div>
        <select onChange={(e) => handleCameraSelect(e.target.value)}>
          <option value="">Select a camera</option>
          {cameras.map(camera => (
            <option key={camera.id} value={camera.id}>{camera.name}</option>
          ))}
        </select>
      </div>
      {selectedCamera && (
        <div style={{ marginTop: '20px' }}>
          <img 
            ref={imageRef} 
            alt="Camera feed" 
            style={{ maxWidth: '100%', border: '1px solid #ccc' }} 
          />
        </div>
      )}
    </div>
  );
}

export default CameraViewer;
```

## Step 5: Create the pages

### HomePage.js

```jsx
import React, { useState } from 'react';
import OrganizationSelector from '../components/OrganizationSelector';
import LocationSelector from '../components/LocationSelector';
import MachineSelector from '../components/MachineSelector';

function HomePage() {
  const [selectedOrg, setSelectedOrg] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Viam Camera Viewer</h1>
      <p>Select your organization, location, and machine to view camera feeds.</p>
      
      <div style={{ marginBottom: '20px' }}>
        <OrganizationSelector onSelect={setSelectedOrg} />
      </div>
      
      {selectedOrg && (
        <div style={{ marginBottom: '20px' }}>
          <LocationSelector 
            organizationId={selectedOrg} 
            onSelect={setSelectedLocation} 
          />
        </div>
      )}
      
      {selectedLocation && (
        <div style={{ marginBottom: '20px' }}>
          <MachineSelector locationId={selectedLocation} />
        </div>
      )}
    </div>
  );
}

export default HomePage;
```

### MachinePage.js

```jsx
import React from 'react';
import { useParams, Link } from 'react-router-dom';
import CameraViewer from '../components/CameraViewer';

function MachinePage() {
  const { machineId } = useParams();

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <Link to="/">&larr; Back to selection</Link>
      </div>
      
      <h1>Machine: {machineId}</h1>
      <CameraViewer machineId={machineId} />
    </div>
  );
}

export default MachinePage;
```

## Step 6: Update App.js with routing

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MachinePage from './pages/MachinePage';

function App() {
  return (
    <Router basename="/machine">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/:machineId" element={<MachinePage />} />
      </Routes>
    </Router>
  );
}

export default App;
```

## Step 7: Build the application

Build your React application:

```bash
npm run build
```

This will create a production build in the `build` directory.

## Step 8: Create a Viam module

Now, let's create a Viam module to host our Single Page App:

```bash
mkdir viam-camera-viewer-module
cd viam-camera-viewer-module
```

Create a `meta.json` file:

```json
{
  "module_id": "your-namespace:camera-viewer",
  "visibility": "public",
  "url": "https://github.com/your-username/viam-camera-viewer",
  "description": "A simple camera viewer single page application",
  "models": [],
  "entrypoint": "",
  "applications": [
    {
      "name": "camera-viewer",
      "type": "web",
      "entrypoint": "build/index.html"
    }
  ]
}
```

Replace `your-namespace` with your organization's public namespace.

## Step 9: Package and upload the module

Copy your React build files to the module directory:

```bash
cp -r ../viam-camera-viewer/build ./
```

Create a module tarball:

```bash
tar -czvf module.tar.gz build meta.json
```

Upload the module to the Viam Registry:

```bash
viam module upload module.tar.gz
```

## Step 10: Access your Single Page App

Once your module is approved, you can access your Single Page App at:

```
https://camera-viewer.your-namespace.viamapps.com
```

Replace `your-namespace` with your organization's public namespace.

## Integrating with the Viam SDK

The example above uses placeholder data. In a real application, you would use the Viam TypeScript SDK to interact with your machines. Here's how you might implement the actual API calls:

### Connecting to Viam

```jsx
import { createRobotClient, ViamClient } from '@viamrobotics/sdk';

// Create a Viam client
const createClient = async () => {
  try {
    // Get credentials from localStorage
    const apiKey = localStorage.getItem('viamApiKey');
    const apiKeyId = localStorage.getItem('viamApiKeyId');
    
    if (!apiKey || !apiKeyId) {
      throw new Error('API credentials not found');
    }
    
    const client = await createRobotClient({
      host: 'your-machine-fqdn.viam.cloud',
      credential: {
        type: 'api-key',
        payload: apiKey,
      },
      signingAuthority: apiKeyId,
      authEntity: 'your-machine-id',
    });
    
    return client;
  } catch (error) {
    console.error('Error creating client:', error);
    throw error;
  }
};
```

### Getting camera data

```jsx
// Get camera image
const getCameraImage = async (client, cameraName) => {
  try {
    const camera = await client.camera.fromRobot(cameraName);
    const image = await camera.getImage();
    return image;
  } catch (error) {
    console.error('Error getting camera image:', error);
    throw error;
  }
};
```

## Conclusion

You've successfully created and deployed a Single Page App with Viam! This simple application demonstrates how to build a web interface for interacting with Viam machines. You can extend this application to include more features, such as controlling motors, reading sensor data, or implementing more complex machine interactions.

For more information about Single Page Apps, see the [Single Page Apps documentation](/operate/reference/single-page-apps/).