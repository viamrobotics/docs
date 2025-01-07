If your camera is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review this camera model's documentation to ensure you have configured all required attributes.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the camera there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

### Common errors

{{% expand "Failed to find the best driver that fits the constraints" %}}

When working with a [camera](/operate/reference/components/camera/) component, depending on the camera, you may need to explicitly provide some camera-specific configuration parameters.

**Solution:** Check the specifications for your camera, and manually provide configuration parameters such as width and height to the camera component configuration page on the [Viam app](https://app.viam.com).
On the **CONFIGURE** page, find your camera, then fill in your camera's specific configuration either using the **Show more** button to show the relevant configuration options, or the **{}** (Switch to Advanced) button in the top right of the component panel to enter these attributes manually.
Provide at least the width and height values to start.
{{% /expand%}}
