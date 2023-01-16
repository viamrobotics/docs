---
title: "Heading Test"
linkTitle: "Heading Test"
weight: 1
draft: true
type: "docs"
---


<style>

/* body, lists*/
.td-content p, .td-content li, .td-content td {
    font-weight: normal;
    color: black;
    margin-left: 24pt;
}
/* table margin */
.table, .td-content > table, .td-box .row.section > table {
    margin: 12pt 0pt 12pt 24pt;
}

/* img margin */
.img-fluid, .td-content img {
    max-width: 100%;
    height: auto;
    margin: 12pt 0pt  12pt 24pt;
}

/* expander */

.expand-label {
    font-family: Space Grotesk, sans-serif;
    font-weight: bold;
    font-size: 12px !important;
    background-color: #e7ecff;
    margin-top: 12pt;
    margin-left: 24pt;
}


.nav-tabs {
    border-bottom: 1px solid #dee2e6;
    margin-left:24pt;
}

h7 {
    margin-left:24pt;
}

h1, .h1 {
    font-size: 32pt !important;
    margin-left: 0px;
   }
   
   h2, .h2 {
    font-size: 24 pt !important;
        margin-left: 0px;

   }
   
   h3, .h3 {
    font-size: 18pt !important;
        margin-left: 0px;
   }

      /* Added H4 and H5 in response to DAD-97 */
      /* Added rules and increased indents */
   h4, .h4 {
    font-size: 16pt !important;
    margin-left: 0px;    
   }

   h5, .h5 {
    font-size: 16pt !important;
    font-weight: 400;
    font-style: italic;
    margin-left: 0px;    

   }
   h7 {
    font-size: 10pt !important;
    font-weight: 400;
    font-style: italic;
    text-decoration: underline green;
   }



h1:after
{
    content:' ';
    display:block;
    border:1px solid black;
}

h2:after
{
    content:' ';
    display:block;
    border:1px solid black;
    margin-right:5%;
}

h3:after
{
    content:' ';
    display:block;
    border:1px solid black;
    margin-right:35%;
}

h4:after
{
    content:' ';
    display:block;
    border:1px solid black;
    margin-right:55%;
}
h5:after
{
    content:' ';
    display:block;
    border:1px solid  black;
    margin-right:75%;
}

</style>

# heading 1

* list item
  * list item
  * list item
  * list item
* list item

<img style="border:solid 1px black" alt="Screen capture of Tab/Tabs Shortcode Usage" src="/img/tabbed-panel-markdown.png">

{{%expand "Click to view the source" %}}
<br>

**Prism syntax highlighting works in expanders, as do most other shortcodes.**

``` go
	motion_svc = MotionServiceClient.from_robot(robot, "NAME”)
  	arm = Arm.from_robot(robot=robot, name='xArm6')
  	pos = await arm.get_end_position()
 	 
  	print("~~~~TESTING ARM LINEAR MOVE~~~~~")
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x += 300
  	# Note we are passing an empty worldstate
  	await arm.move_to_position(pose=pos, world_state=WorldState())
  	pos = await arm.get_end_position()
  	print(pos)
  	pos.x -= 300
  	await asyncio.sleep(1)
  	await arm.move_to_position(pose=pos, world_state=WorldState())
```

{{% /expand%}}

<table>
    <tr>
        <td>id</td>
        <td>name</td>
        <td>age</td>
        <td>gender</td>
    </tr>
    <tr>
        <td>1</td>
        <td>Roberta</td>
        <td>39</td>
        <td>M</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Oliver</td>
        <td>25</td>
        <td>M</td>
    </tr>
    <tr>
        <td>3</td>
        <td>Shayna</td>
        <td>18</td>
        <td>F</td>
    </tr>
    <tr>
        <td>4</td>
        <td>Fechin</td>
        <td>18</td>
        <td>M</td>
    </tr>
</table>



## heading 2

| id | name    | age | gender |
|----|---------|-----|--------|
| 1  | Roberta | 39  | M      |
| 2  | Oliver  | 25  | M      |
| 3  | Shayna  | 18  | F      |
| 4  | Fechin  | 18  | M      |

Robot ipsum datus scan amet, constructor ad ut splicing elit, sed do errus mod tempor in conduit ut laboratory et deplore electromagna aliqua. Ut enim ad minimum veniam, quis no indestruct exoform ullamco laboris nisi ut alius equip ex ea commando evaluant. Duis ex machina aute ire dolorus in scan detectus an voluptate volt esse cesium dolore eu futile nulla parameter. Execute primus sint occaecat cupidatat non proident, sunt in culpa qui technia deserunt mondus anim id est proceus.


1. num item
1. num item
1. num item
1. num item

### heading 3

Duis ex machina aute ire dolorus in scan detectus an voluptate volt esse cesium dolore eu futile nulla parameter. Execute primus sint occaecat cupidatat non proident, sunt in culpa qui technia deserunt mondus anim id est proceus.

**include file**

{{< readfile "/static/include/sample.md" >}}





Ut enim ad minimum veniam, quis no indestruct exoform ullamco laboris nisi ut alius equip ex ea commando evaluant.

#### heading 4

Ut enim ad minimum veniam, quis no indestruct exoform ullamco laboris nisi ut alius equip ex ea commando evaluant.

{{< figure src="/img/alert-markdown.png"  alt="The shortcodes used to display Alerts." title="Shortcodes for Alerts" >}}

{{< alert title="Tip" color="tip" >}}  
Use for tips
{{< /alert >}}

##### heading 5

Duis ex machina aute ire dolorus in scan detectus an voluptate volt esse cesium dolore eu futile nulla parameter. Execute primus sint occaecat cupidatat non proident, sunt in culpa qui technia deserunt mondus anim id est proceus.


{{< tabs name="TabPanelExample" >}}
{{% tab name="Support"%}}
**Supported**
* Markdown and HTML images. 
* Alert Shortcode
* PRISM syntax highlighting (the three backticks)
* "codelang" highlighting (add codelang="language" to tab element). It's very ugly, needs css work, and is not recommended at this time.

**Not Supported**
* Footnotes
* Expanders

**Example Usage**

<img style="border:solid 1px black" alt="Screen capture of Tab/Tabs Shortcode Usage" src="/img/tabbed-panel-markdown.png">

{{% /tab %}}
{{% tab name="Examples" %}}
<div>
	<h3>What is Rendered?</h3>
	<p>It renders <i>vanilla</i> HTML and markdown, Alerts, and images. For example, these two images:</p>

* **Markdown Image Example**<br>
![expand example](/img/expander-markdown.png)<br>
* **HTML Image Example** (with border)<br>
<img style="border:solid 1px black" src="/img/expander-markdown.png" alt="Screen capture of Tab/Tabs Shortcode Usage">
</div>
<br>

### Syntax Highlighting with Backticks

Line numbering is on by default.

```json-viam
{
"word":"As before, three backticks and the language name enables Prism syntax highlighting.",
"note":"Use "json-viam" as the language to highlight Viam's keywords."
}
```

With just line 6 highlighted. See https://prismjs.com/plugins/line-highlight/ for more:

```python {class="line-numbers linkable-line-numbers" data-line="6"}
while (True):
    # When True, sets the LED pin to high or on.
    await led.set(True)
    print('LED is on')

    await asyncio.sleep(1)

    # When False, sets the pin to low or off.
    await led.set(False)
    print('LED is off')

    await asyncio.sleep(1)
```


With linked lines and lines 8-10 highlighted.


```python {id="some-python-unique-id" class="linkable-line-numbers" data-line="8-10"}
while (True):
    # When True, sets the LED pin to high or on.
    await led.set(True)
    print('LED is on')

    await asyncio.sleep(1)

    # When False, sets the pin to low or off.
    await led.set(False)
    print('LED is off')

    await asyncio.sleep(1)
```

### Regular Markdown Formatting

This is **some markdown.**

### Alerts Shortcodes
{{< alert title="Note" color="note" >}}
It can even contain shortcodes.
{{< /alert >}}


{{% /tab %}}
{{< /tabs >}}


