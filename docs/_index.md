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
<p>
You can, for example,
<select class="custom-select" id="program-action" on onclick="showTab('program');">
    <option value="program-base" onclick="showTab('program');">drive any robotic base</option>
    <option value="program-motor" onclick="showTab('program');">control any motor</option>
    <option value="program-camera" onclick="showTab('program');">get photos from any camera</option>
    <option value="program-sensor" onclick="showTab('program');">get readings from any sensor</option>
    <option value="program-arm" onclick="showTab('program');">move any arm</option>
    <option value="program-other" onclick="showTab('program');">operate custom hardware</option>
</select>
with
<select class="custom-select lang" id="program-lang" onclick="showTab('program');">
    <option value="lang-py" onclick="showTab('program');">Python</option>
    <option value="lang-go" onclick="showTab('program');">Go</option>
    <option value="lang-ts" onclick="showTab('program');">TypeScript</option>
    <option value="lang-dart" onclick="showTab('program');">Flutter</option>
    <option value="lang-cpp" onclick="showTab('program');">C++</option>
</select>
:</p>

<script>
function showTab(set) {
  alert(set)
  let action = document.getElementById(set + "-action").value;
  let lang = document.getElementById(set + "-lang").value;

  console.log(action, lang);

  // active parent tab
  let parentTab = document.getElementById("tabset--" + action)
  let parentChildren = parentTab.parentElement.children;
  for (let i=0; i<parentChildren.length; i++) {
    console.log(parentChildren[i]);
    if (parentChildren[i].id == "tabset--" + action) {
      new bootstrap.Tab(parentChildren[i]).show();
      console.log("show")
    } else {
      new bootstrap.Tab(parentChildren[i]).dispose();
      parentChildren[i].classList.remove("active");
      console.log("hide")
    }
  }

  // activate language tab
  let languageTab = document.getElementById("tabset--" + action + '-' + lang)
  let allLanguageTabs = languageTab.parentElement.children;
  for (let i=0; i<allLanguageTabs.length; i++) {
    console.log(allLanguageTabs[i]);
    if (allLanguageTabs[i].id == "tabset--" + action + '-' + lang) {
      new bootstrap.Tab(allLanguageTabs[i]).show();
      console.log("show")
    } else {
      new bootstrap.Tab(allLanguageTabs[i]).dispose();
      allLanguageTabs[i].classList.remove("active");
      console.log("hide")
    }
  }

}
</script>

<div class="table front-page">
  <div class="tab-content" id="tab-content-tabset--program">
    <div id="tabset--program-base" class="tab-pane show active" role="tabpanel" aria-labelledby="tabset--program-base">
      <div>
<div class="tab-content" id="tab-content-tabset--program-lang"><div id="tabset--program-base-lang-py" class="tab-pane show active" role="tabpanel" aria-labelledby="tabset--program-base-lang-py">

```python {class="dark"}
async def moveInSquare(base):
    for _ in range(4):
        # move forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        # spin 90 degrees at 100 degrees/s
        await base.spin(velocity=100, angle=90)
```

</div>
<div id="tabset--program-base-lang-go" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program=base-lang-go">

```go {class="dark"}
func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // move forward 500mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        // spin 90 degrees at 100 degrees/s
        base.Spin(ctx, 90, 100.0, nil)
    }
}
```

</div>
<div id="tabset--program-base-lang-ts" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-base-lang-ts">

```ts {class="dark"}
async function moveInSquare(baseClient: VIAM.BaseClient) {
  for (let i = 0; i < 4; i++) {
    // move forward 500mm at 500mm/s
    await baseClient.moveStraight(500, 500);
    // spin 90 degrees at 100 degrees/s
    await baseClient.spin(90, 100);
  }
}
```

</div>
<div id="tabset--program-base-lang-dart" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-base-lang-dart">

```dart {class="dark"}
Future<void> moveSquare() async {
  for (var i=0; i<4; i++) {
    // move forward 500mm at 500mm/s
    await base.moveStraight(500, 500);
    // spins the rover 90 degrees at 100 degrees/s
    await base.spin(90, 100);
  }
}
```
</div>
<div id="tabset--program-base-lang-cpp" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-base-lang-cpp">

```cpp {class="dark"}
void move_in_square(std::shared_ptr<viam::sdk::Base> base) {
  for (int i = 0; i < 4; ++i) {
    // move forward 500mm at 500mm/s
    base->move_straight(500, 500);
    // spins the rover 90 degrees at 100 degrees/s
    base->spin(90, 100);
  }
}
```

</div></div>
</div>
<div class="explanation">
  <div class="explanationtext">

Try it yourself, [drive a rover](/how-tos/drive-rover/).

  </div>
  <div class="explanationvideo">
    {{<gif webm_src="/tutorials/try-viam-sdk/image1.webm" mp4_src="/tutorials/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square.">}}
  </div>
</div>
</div>
    <div id="tabset--program-motor" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-motor">
      <div>
<div class="tab-content" id="tab-content-tabset--program-lang"><div id="tabset--program-motor-lang-py" class="tab-pane show active" role="tabpanel" aria-labelledby="tabset--program-motor-lang-py">

```python {class="dark"}
async def spin_motor(motor):
    # turn the motor at 35% power forwards
    await motor.set_power(power=0.35)
    # let the motor spin for 3 seconds
    time.sleep(3)
    # stop the motor
    await await motor_1.stop()
```

</div>
<div id="tabset--program-motor-lang-go" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-motor-lang-go">

```go {class="dark"}
func spinMotor(ctx context.Context, motor motor.Motor, logger logging.Logger) {
  // turn the motor at 35% power forwards
  err = motor1Component.SetPower(context.Background(), 0.35, nil)
  // let the motor spin for 3 seconds
  time.Sleep(3 * time.Second)
  // stop the motor
  err = motor1Component.Stop(context.Background(), nil)
}
```

</div>
<div id="tabset--program-motor-lang-ts" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-motor-lang-ts">

```ts {class="dark"}
async function spinMotor(motorClient: VIAM.MotorClient) {
  // turn the motor at 35% power forwards
  await motor.setPower(0.35);
  // let the motor spin for 3 seconds
  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));
  await sleep(3000);
  // stop the motor
  await motor.stop();
}
```

</div>
<div id="tabset--program-motor-lang-dart" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-motor-lang-dart">

```dart {class="dark"}
Future<void> spinMotor() async {
  // turn the motor at 35% power forwards
  await motorClient.setPower(0.35);
  // let the motor spin for 3 seconds
  // TODO (also fix control-motor...)

  // stop the motor
  await motorClient.stop();
}
```

</div>
<div id="tabset--program-motor-lang-cpp" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-motor-lang-cpp">

```cpp {class="dark"}
void spin_motor(std::shared_ptr<viam::sdk::Motor> motor) {
  // turn the motor at 35% power forwards
  motor->set_power(0.35);
  // let the motor spin for 3 seconds
  sleep(3);
  // stop the motor
  motor->stop();
}
```

</div></div>
</div>
<div class="explanation">
  <div class="explanationtext">

Try it yourself, [control a motor](/how-tos/control-motor/).
  </div>
  <div class="explanationvideo">
    {{<gif webm_src="/tutorials/single-component-tutorials-servo-mousemover/angle-100.webm" mp4_src="/tutorials/single-component-tutorials-servo-mousemover/angle-100.mp4" alt="A gif at the top of the CONTROL tab in the Viam app. The pointer finger is pressing the 10 button and it changes the angle from 90 to 100 repeatedly. The red STOP button is in the upper right corner. There is a blue circular arrow depicting the servo's direction as being counterclockwise. Below this is a gif of the Raspberry Pi to the left and the FS90R servo on the right. The servo stops, then spins counterclockwise repeatedly.">}}
  </div>
</div>
    </div>
    <div id="tabset--program-camera" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-camera">
      <p>TODO: Camera</p>
    </div>
    <div id="tabset--program-sensor" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-sensor">
      <p>TODO: Sensor</p>
    </div>
    <div id="tabset--program-arm" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-arm">
      <p>TODO: Arm</p>
    </div>
    <div id="tabset--program-other" class="tab-pane" role="tabpanel" aria-labelledby="tabset--program-other">
      <p>TODO: Other</p>
    </div>
  </div>
</div>
</div>
<div class="max-page">
  <h2 class="frontpage-headers">Make your devices smarter and better</h2>
  <p>
    You can pick and choose from additional tools to make your devices understand their environment, interact with it, and collect information:
  </p>
<p>
You can, for example, add
<select class="custom-select" id="smarter-action" >
    <option value="smarter-cv" onclick="showTab('smarter');">Computer Vision</option>
    <option value="smarter-ml" onclick="showTab('smarter');">Machine Learning</option>
    <option value="smarter-data" onclick="showTab('smarter');">Data Management</option>
    <option value="smarter-motion" onclick="showTab('smarter');">Motion</option>
    <option value="smarter-nav" onclick="showTab('smarter');">Navigation</option>
    <option value="smarter-custom" onclick="showTab('smarter');">Custom Logic</option>
</select>
and use it with
<select class="custom-select lang" id="smarter-lang">
    <option value="lang-py" onclick="showTab('smarter');">Python</option>
    <option value="lang-go" onclick="showTab('smarter');">Go</option>
    <option value="lang-ts" onclick="showTab('smarter');">TypeScript</option>
    <option value="lang-dart" onclick="showTab('smarter');">Flutter</option>
    <option value="lang-cpp" onclick="showTab('smarter');">C++</option>
</select>
:</p>
</div>
<div class="max-page">
  <h2 class="frontpage-headers">Go from one machine to thousands</h2>
  <p>
    When you connect machines to the cloud you get fleet management tools that let you scale from one prototype to thousands of machines you can manage and operate from one place.
  </p>
<p>
<select class="custom-select" id="scale-action" >
    <option value="scale-deployment" onclick="showTab('scale');">Deployment</option>
    <option value="scale-provisioning" onclick="showTab('scale');">Provisioning</option>
    <option value="scale-diagnostics" onclick="showTab('scale');">Remote Diagnostics</option>
    <option value="scale-data" onclick="showTab('scale');">Data Management</option>
    <option value="scale-ml" onclick="showTab('scale');">ML Training</option>
    <option value="scale-billing" onclick="showTab('scale');">Billing</option>
</select>
for all your machines with
<select class="custom-select lang" id="scale-lang">
    <option value="lang-py" onclick="showTab('scale');">Code</option>
    <option value="lang-go" onclick="showTab('scale');">Viam App</option>
</select>
:</p>
</div>