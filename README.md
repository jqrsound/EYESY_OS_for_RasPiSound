# EYESY on Raspberry Pi with Blokas PiSound

The operating system for the EYESY video synthesizer device - remixed.
Adaptation of the Critter&Guitari EYESY video synth in order to run it on a Raspberry Pi with Blokas PiSound.
Eyesy Manual : https://www.critterandguitari.com/manual?m=EYESY_Manual#eyesy%E2%84%A2-user-manual


# Installation:

Run ./install.sh


# Usage:

- Connect a display to the HDMI out.
- Boot up your RasPi
- Push the Button once to start EYESY, twice to stop it.

   
# Control via MIDI CC

21 - 22 - 23 - 24: Knobs 1 to 4
25: Background Color 
26: Previous Scene
27: Next Scene
28: Save or delete (long hold)
29: Auto Clear Toggle 
30: Previous Mode 
31: Next Mode
32: Take Screenshot 
33: Shift Key
34: Input Gain
35: Trigger Source
36: Info Disp 
37: Send Trigger


# Web Editor
The web editor lets you edit the pygame scripts that generate the visuals on the fly. It should be accessible at http://patchbox.local:8080/
See the Eyesy manual for more details on using the web editor.


# Uninstall:
From the shellscript folder run ./uninstall.sh


# Rem:
You can use the stereo input in your Modes, in Python there are accessible via `etc.audio_left` and `etc.audio_right` in the scripts, `etc.audio_in` remains L + R.
