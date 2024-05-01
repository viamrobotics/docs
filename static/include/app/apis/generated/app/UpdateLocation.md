### UpdateLocation

{{< tabs >}}
{{% tab name="Python" %}}

Change the name of a location and/or assign it a new parent location.

**Parameters:**

- `location_id` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): ID of the location to update. Must be specified.
- `name` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional new name to be updated on the location. Defaults to the empty string “” (i.e., the name doesn’t change).
- `parent_location_id` [(str)](<INSERT PARAM TYPE LINK>) (optional): Optional ID of new parent location to move the location under. Defaults to the empty string “” (i.e., no new parent location is assigned).


**Returns:**

- [(viam.proto.app.Location)](INSERT RETURN TYPE LINK): The newly updated location.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/app/app_client/index.html#viam.app.app_client.AppClient.update_location).

``` python {class="line-numbers linkable-line-numbers"}
# The following line takes the location with ID "abc12abcde" and moves it to be a
# sub-location of the location with ID "xyz34xxxxx"
my_updated_location = await cloud.update_location(
    location_id="abc12abcde",
    name="",
    parent_location_id="xyz34xxxxx",
)

# The following line changes the name of the location without changing its parent location
my_updated_location = await cloud.update_location(
    location_id="abc12abcde",
    name="Land Before Robots"
)

# The following line moves the location back up to be a top level location without changing its name
my_updated_location = await cloud.update_location(
    location_id="abc12abcde",
    name="",
    parent_location_id=""
)

```

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `locationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `parentLocationId` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `region` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.app.app/AppServiceClient/updateLocation.html).

{{% /tab %}}
{{< /tabs >}}
