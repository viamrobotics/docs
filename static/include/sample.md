### This is a Heading in the Sample File

This entire section was added to the current topic using the `readfile` shortcode.

{{% alert="Note" color="note" %}}
Changes to included files do not appear in local mode (`hugo server -D`).
You'll need to halt and restart the server to view the changes.
{{% /alert %}}

## Heading 2

* bullet 1
* bullet 2

### Heading 3

This Markdown code:

``` sh
Markdown Table
| id | name    |
|----|---------|
| 1  | Roberta |
| 2  | Oliver  |
| 3  | Shayna  |
| 4  | Fechin  |
```

Renders like so:

Markdown Table
| id | name    |
|----|---------|
| 1  | Roberta |
| 2  | Oliver  |
| 3  | Shayna  |
| 4  | Fechin  |

This HTML code:

``` html
<h3>HTML Table</h3>

<table>
  <tr>
    <th>id</th>
    <th>name</th>
  </tr>
  <tr>
    <td>1</td>
    <td>Roberta</td>
  </tr>
  <tr>
    <td>2</td>
    <td>Oliver</td>
  </tr>
  <tr>
    <td>3</td>
    <td>Shayna</td>
  </tr>
  <tr>
    <td>4</td>
    <td>Fechin</td>
  </tr>
</table>
```

Renders like so:

<h3>HTML Table</h3>

<table>
  <tr>
    <th>id</th>
    <th>name</th>
  </tr>
  <tr>
    <td>1</td>
    <td>Roberta</td>
  </tr>
  <tr>
    <td>2</td>
    <td>Oliver</td>
  </tr>
  <tr>
    <td>3</td>
    <td>Shayna</td>
  </tr>
  <tr>
    <td>4</td>
    <td>Fechin</td>
  </tr>
</table>

**This is the last line of the included file.**
