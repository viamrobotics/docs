The `applications` field is an array of application objects with the following properties:

<!-- prettier-ignore -->
| Property     | Type   | Description |
| ------------ | ------ | ----------- |
| `name`       | string | The name of your application, which is part of the application's URL (`name_publicnamespace.viamapplications.com`). For more information on valid names see [Valid application identifiers](/operate/modules/advanced/metajson/#valid-application-identifiers). |
| `type` | string | The type of application: `"single_machine"` or `"multi_machine"`. Whether the application can access and operate one machine or multiple machines. |
| `entrypoint` | string | The path to the HTML entry point for your application. The `entrypoint` field specifies the path to your application's entry point. For example: <ul><li><code>"dist/index.html"</code>: Static content rooted at the `dist` directory</li><li><code>"dist/foo.html"</code>: Static content rooted at the `dist` directory, with `foo.html` as the entry point</li><li><code>"dist/"</code>: Static content rooted at the `dist` directory (assumes `dist/index.html` exists)</li><li><code>"dist/bar/foo.html"</code>: Static content rooted at `dist/bar` with `foo.html` as the entry point</li></ul> |
| `fragmentIds` | []string | Specify the fragment or fragments that a machine must contain to be selectable from the machine picker screen. Only for single machine applications. |
| `logoPath` | string | The URL or the relative path to the logo to display on the machine picker screen for a single machine application. |
| `customizations` | object | Override the branding heading and subheading to display on the authentication screen for single machine applications: <ul><li>`heading`: Override the heading. May not be longer than 60 characters. </li><li>`subheading` Override the subheading. May not be longer than 256 characters.</li></ul> Example: `{ "heading": "Air monitoring dashboard", "subheading": "Sign in and select your devices to view your air quality metrics in a dashboard" }`. |
