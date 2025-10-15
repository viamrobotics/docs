Once you've installed `viam-server` and your machine has come online, if your machine has a webcam, you can try an example project:

1. Click the **+** icon next to your machine part in the left-hand menu and select **Insert Fragment**.

   Add the [`DeskSafariGame` fragment](https://app.viam.com/fragment/0161c5da-48fa-4a23-8e7f-95fb85cfb3f8) by the `Robot Land` organization and click **Insert Fragment**.
   This adds a number of {{< glossary_tooltip term_id="resource" text="resources" >}} to your machine:

   - a camera component which connects to the webcam
   - machine learning resources to run a model and apply it to the camera stream
   - control logic that implements a game

1. **Save** your config and review the available resources on the **CONFIGURE** tab.
1. Log into [this Viam application](https://hello-world-game-web-app_naomi.viamapplications.com/) with your Viam credentials and select your machine.
   The application provides a UI for playing the game
1. Select a camera and press the Start Game button.
   The goal of the game is to find and show specific objects to the camera.

If you'd like to learn how to create this game, see the [Desk Safari tutorial](/operate/hello-world/tutorial-desk-safari/).

Should the game not work, return to your machine in the Viam web UI and check the **LOGS** tab for errors.
