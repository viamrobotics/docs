{{< table >}}
{{% tablestep number=1 %}}
**Authenticate with the CLI**

Authenticate using a personal access token:

```sh {class="command-line" data-prompt="$"}
viam login
```

For alternative authentication methods, see [Authenticate](/dev/tools/cli/#authenticate).

{{% /tablestep %}}
{{% tablestep number=2 %}}
**Find your organization ID**

The following steps require your organization ID.
To find, it use the following command:

```sh {class="command-line" data-prompt="$"}
viam organizations list
```

{{% /tablestep %}}
{{% tablestep number=3 %}}
**Configure a new database user**

Configure a new database user.
The database user will be able to connect to your data, which is stored in a MongoDB [Atlas Data Federation](https://www.mongodb.com/docs/atlas/data-federation/overview/) instance.

{{% alert title="Warning" color="warning" %}}
The command will create a user with your organization ID as the username.
If you or someone else in your organization have already created this user, the following steps update the password for that user instead.
Dashboards or other integrations relying on this password will then need to be updated.
{{% /alert %}}

Provide your organization's `org-id` from step 2, and a password for your database user.
Your password must be at least 8 characters long with 1 uppercase, and 1 numeric character.

```sh {class="command-line" data-prompt="$"}
viam data database configure --org-id=<YOUR-ORGANIZATION-ID> --password=<NEW-DBUSER-PASSWORD>
```

{{% /tablestep %}}
{{% tablestep number=4 %}}
**Determine the connection URI**

Determine the connection URI (also known as a connection string) for your organization's MongoDB Atlas Data Federation instance by running the following command with the organization's `org-id` from step 2:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam data database hostname --org-id=abcd1e2f-a1b2-3c45-de6f-ab123456c123

MongoDB Atlas Data Federation instance hostname: data-federation-abcd1e2f-a1b2-3c45-de6f-ab123456c123-0z9yx.a.query.mongodb.net
MongoDB Atlas Data Federation instance connection URI: mongodb://db-user-abcd1e2f-a1b2-3c45-de6f-ab123456c123:YOUR-PASSWORD-HERE@data-federation-abcd1e2f-a1b2-3c45-de6f-ab123456c123-0z9yx.a.query.mongodb.net/?ssl=true&authSource=admin
```

This command returns the:

- **hostname:** the MongoDB Atlas Data Federation instance hostname
- **connection URI:** the MongoDB Atlas Data Federation instance connection uniform resource indicator.
  This is the _connection URI_ to your organization's MongoDB Atlas Data Federation instance, which is of the form:

  ```sh {class="command-line" data-prompt="$"}
  mongodb://<USERNAME>:<YOUR-PASSWORD>@<HOSTNAME>/?ssl=true&authSource=admin
  ```

Most MQL-compatible database clients require the _connection URI_, along with your user credentials, to connect to this server.

Some MQL-compatible database client instead require a _hostname_ and _database name_, along with your user credentials, to connect to this server.
For sensor data, this database name will be `sensorData`.

{{% /tablestep %}}
{{< /table >}}
