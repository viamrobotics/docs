---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam is a complete software platform for smart machines that runs on any 64-bit Linux OS and macOS."
weight: 1
no_list: true
type: "docs"
noToc: true
hide_feedback: true
sitemap:
  priority: 1.0
outputs:
  - html
carouselscript: true
date: "2024-09-17"
# updated: ""  # When the content was last entirely checked
---

<div class="max-page">
  <p>
    Welcome to the Viam Documentation!
    Viam is a software platform that makes it easy to combine and integrate hardware and software to build machines, connect them with the cloud, and make them smarter with machine learning.
  </p>
  <div class="cards max-page use-cases aligncenter">
    <div class="front-card-container">
      <div class="hover-card primary">
        <a href="how-tos/" class="noanchor">
        <div>
          <p>How-to Guides</p>
        </div>
      </a>
      </div>
      <div class="hover-card">
        <a href="platform/" class="noanchor"><div>
        <p>Platform Reference</p></div>
        </a>
      </div>
    </div>
  </div>
</div>
<br>
<div class="max-page">
  <h2 class="frontpage-headers">Program any device</h2>
  <p>
    Viam integrates with hardware and software on <b>any device</b>. Once installed, you can control your devices and any attached physical hardware like this:
  </p>

<div class="table front-page">
  <ul class="nav nav-tabs" id="tab-tabset--program" role="tablist">
    <li class="nav-item"><a data-toggle="tab" class="nav-link active" data-td-tp-persist="Drive rover" data-bs-toggle="tab" data-bs-target="#tabset--program-0" href="#tabset--program-0" role="tab" aria-controls="tabset--program-0" aria-selected="true">Drive rover</a></li>
    <li class="nav-item"><a data-toggle="tab" class="nav-link" data-td-tp-persist="Control motor" data-bs-toggle="tab" data-bs-target="#tabset--program-1" href="#tabset--program-1" role="tab" aria-controls="tabset--program-1">Control motor</a></li>
    <li class="nav-item"><a data-toggle="tab" class="nav-link" data-td-tp-persist="Take picture" data-bs-toggle="tab" data-bs-target="#tabset--program-2" href="#tabset--program-2" role="tab" aria-controls="tabset--program-2">Take picture</a></li>
    <li class="nav-item"><a data-toggle="tab" class="nav-link" data-td-tp-persist="Get sensor reading" data-bs-toggle="tab" data-bs-target="#tabset--program-3" href="#tabset--program-3" role="tab" aria-controls="tabset--program-3">Get sensor reading</a></li>
    <li class="nav-item"><a data-toggle="tab" class="nav-link" data-td-tp-persist="Operate custom hardware" data-bs-toggle="tab" data-bs-target="#tabset--program-4" href="#tabset--program-4" role="tab" aria-controls="tabset--program-4">Operate custom hardware</a></li>
  </ul>
  <div class="tab-content" id="tab-content-tabset--program">
    <div id="tabset--program-0" class="tab-pane show active" role="tabpanel" aria-labelledby="tabset--program-0" style="min-height: ">
      <span>
      <div>
{{< tabs >}}
{{% tab name="Python" %}}

```python {class="dark"}
async def moveInSquare(base):
    for _ in range(4):
        # moves the rover forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        print("move straight")
        # spins the rover 90 degrees at 100 degrees per second
        await base.spin(velocity=100, angle=90)
        print("spin 90 degrees")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="dark"}
func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // moves the rover forward 600mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        logger.Info("move straight")
        // spins the rover 90 degrees at 100 degrees per second
        base.Spin(ctx, 90, 100.0, nil)
        logger.Info("spin 90 degrees")
    }
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts {class="dark"}
// This function moves a base component in a square.
async function moveInSquare(client: VIAM.RobotClient) {
  // Replace with the name of the base on your machine.
  const name = "viam_base";
  const baseClient = new VIAM.BaseClient(client, name);

  for (let i = 0; i < 4; i++) {
    console.log("move straight");
    await baseClient.moveStraight(500, 500);
    console.log("spin 90 degrees");
    await baseClient.spin(90, 100);
  }
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart {class="dark"}
Future<void> moveSquare() async {
  for (var i=0; i<4; i++) {
    await base.moveStraight(500, 500);
    await base.spin(90, 100);
  }
}
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp {class="dark"}
void move_in_square(std::shared_ptr<viam::sdk::Base> base) {
  for (int i = 0; i < 4; ++i) {
    cout << "Move straight" << endl;
    // Move the base forward 600mm at 500mm/s
    base->move_straight(500, 500);
    cout << "Spin" << endl;
    // Spin the base by 90 degree at 100 degrees per second
    base->spin(90, 100);
  }
}
```
{{% /tab %}}
{{< /tabs >}}
  </div>
  <div class="gif"><video autoplay="" loop="" muted="" playsinline="" alt="Overhead view of the Viam Rover showing it as it drives in a square." width="100%" style="max-width:400px" class="lozad" data-loaded="true"><source data-src="/tutorials/try-viam-sdk/image1.webm" type="video/webm" src="/tutorials/try-viam-sdk/image1.webm"><source data-src="/tutorials/try-viam-sdk/image1.mp4" type="video/mp4" src="/tutorials/try-viam-sdk/image1.mp4">There should have been a video here but your browser does not seem to support it.</video><noscript><video autoplay loop muted playsinline alt="Overhead view of the Viam Rover showing it as it drives in a square." width=100% style=max-width:400px><source data-src=/tutorials/try-viam-sdk/image1.webm type=video/webm><source data-src=/tutorials/try-viam-sdk/image1.mp4 type=video/mp4>There should have been a video here but your browser does not seem to support it.</video></noscript></div>
  </span>
  <p>Learn about <a href="/how-tos/drive-rover/">driving a rover.</a></p>
</div>
    <div id="tabset--program-1" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-1" style="min-height: ">
      <p>TODO3</p>
    </div>
    <div id="tabset--program-2" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-2" style="min-height: ">
      <p>TODO2</p>
    </div>
    <div id="tabset--program-3" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-3" style="min-height: ">
      <p>TODO4</p>
    </div>
    <div id="tabset--program-4" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-4" style="min-height: ">
      <p>TODO5</p>
    </div>
  </div>
</div>
</div>
<div class="max-page">
  <h2 class="frontpage-headers">Make your devices smarter and better</h2>
  <p>
    You can pick and choose from additional tools to make your devices understand their environment, interact with it, and collect information:
  </p>
</div>
<div class="max-page">
  <h2 class="frontpage-headers">Go from one machine to thousands</h2>
  <p>
    When you connect machines to the cloud you get fleet management tools that let you scale from one prototype to thousands of machines you can manage and operate from one place.
  </p>
</div>