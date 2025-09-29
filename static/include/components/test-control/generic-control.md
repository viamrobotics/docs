## Test the generic component

After you configure your generic component, open the generic's panel on the [**CONTROL**](/manage/troubleshoot/teleoperate/default-interface/#web-ui) tab.
Use the card to send arbitrary commands to the resource with [`DoCommand()`](/dev/reference/apis/components/generic/#docommand).

{{<imgproc src="/components/generic/generic-control.png" alt="The generic component in control panel." resize="900x" style="width:500px" class="imgzoom shadow">}}

The example above works for interacting with the generic component model shown in [Deploy control logic](/operate/modules/control-logic/), but other components require different commands depending on how `DoCommand()` is implemented.
