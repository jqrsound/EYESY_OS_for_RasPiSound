# EYESY on RasPi4 w/ Pisound (step-by-step guide)

This is a step-by-step guide that worked for me, I now have a EYESY running smoothly on my Pi and I hope this will help *not programmer* like me to set their Pi without too much headache :slight_smile:

EYESY from Critter and Guitari is a self-contained video synthesizer based on a Raspberry Pi. It generates animated graphics (made with Python)

More Infos: https://docs.critterandguitari.com/EYESY/ey_os_2/

---

**Difficulty:** Intermediate

**Optimized for Headless Use:** Yes

**Recommended Raspberry Pi Models:** I have a Raspberry PI 4 8GB, but I guess it'll work on other models.

### Required Hardware:

* Pisound
* Raspberry Pi w/ power supply and micro SD card (16 GB is great)
* Windows, macOS or Linux computer w/ micro SD card reader

### Required Software:

* Etcher for SD card flashing - https://etcher.io
* Raspbian Lite - https://www.raspberrypi.org/downloads/raspbian
* RealVNC Viewer - https://www.realvnc.com/en/connect/download/viewer

**An important note:** in order to run EYESY on a RaspberryPi 4 8Gb with PiSound I mixed several information and tutorials together (mostly the ones from Mads Kjeldgaard, @mzero  and @okyeron, you can find them at the end of this guide).

Some passages may be redundant (especially with Jack) and when I encountered a problem I found a solution than it was more empirical or based on information I gathered here in the community or on some other forums.

For this guide I did copy/paste the mentioned tutorials plus I added some personal notes. Some mistakes where probably made, so please report them to me, but please consider that after a lot of trial and error at the end is all working :slight_smile:

Note: according to Okyeron EYESY expects a `pi/pi` user/group, therefore I installed Raspbian instead of Patchbox. I also used OS X.

The process is 2 or 3 hours long, so grab a drink and here we go!

## Here we go!

**Step 01: Prepare the SD card with the base system image.**
Download Raspberry Pi OS Lite and flash it onto your SD card with Balena Etcher.
Open up the image for Raspbian Lite, choose the SD card and click flash.


**Step 02: Enable SSH in the Image**
This is very important so that you can connect into the Pi when it boots headless.
After copying the image, you’ll need to edit it slightly before using it in the Pi.
If you can’t see the mounted SD card volume on your desktop, remove it and then insert it again in the card reader.
You should have an external disk named boot, you need to add a file called ssh **(no extensions)** at the top of this volume.

In the terminal, run this command:

```bash
touch /Volumes/boot/ssh
```


**Step 03: Setup default WIFI-network**
To automatically connect to your WIFI network on startup, you need to add another file to the boot folder.
This one should be named `wpa_supplicant.conf` which will contain information about your network.

```bash
touch /Volumes/boot/wpa_supplicant.conf
```

You can copy and paste the snippet below into the file, but make sure you:

1. Replace the string in the ssid line with the name of your network.
2. Replace the string in the psk line with the password your network.
3. Replace the country code in the country=DE line (I am in Germany = DE).
   
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
ap_scan=1
fast_reauth=1
country=DE
 
network={
ssid="Your network's SSID"
psk="Your network's password/psk"
id_str="0"
priority=100
}
```

Save the file, put the SD card back into your Pi and plug the power cord into it to boot it. Wait a few minutes for it to boot.


**Step 04: Log in to your Raspbian Lite remotely**
If you followed the steps above, your Pi should now be connected to the same network as your computer. Now you need the IP address of the Pi.
I used FING for Android, Mzero simply ran on terminal `ssh pi@raspberrypi.local` but I suggest you to read this post:

https://community.blokas.io/t/raspberry-pi-find-raspberry-pis-ip-address/596

Once found the IP address, you can log in from your computer by opening up a terminal and executing `ssh pi@address`, replacing “address” with the actual IP address. If successful you should now be prompted for the password of the pi user which by default is `raspberry`.

In case of ssh warning, type on terminal:

```bash
ssh-keygen -R [Your Raspi IP-Address]
```


**Step 05: Update and Install Basics**
This will ensure you have the latest version of all the installed packages.

```bash
sudo apt-get update
sudo apt-get dist-upgrade
```

Depending on how old the image you downloaded is, this could be quick or take some time.
Now install the minimal things needed to be able to run a graphical desktop.
Run these two commands.

```bash
sudo apt-get install --no-install-recommends \
screen vim \
git make \
xserver-xorg xinit \
realvnc-vnc-server

sudo apt-get install raspberrypi-ui-mods
```


**Step 06: Configuration**
This step uses the standard RaspberryPi configuration program to configure the Pi, it uses the arrow keys and the tab key to navigate.
Run in the shell on the Pi:

```bash
sudo raspi-config
```

And change the following:
```
System Option
S3 Change User Password -- Set a new password
```
Then configure:
```
System Option
S5 Boot/Autologin -- Desktop

Localisation Options
L2 Change Timezone -- pick your timezone
L4 Change Wi-fi Country -- pick your country

Interfacing Options
P3 VNC -- Yes

Performance
P2 GNU Memory -- 16

Display
D1 Resolution -- 1600x1200
```
Then \[tab\] key to *Finish*, hit return, then select *Yes* to reboot.


**Step 07: Important packages and dependencies**
Run this command to install git and perl which are important packages you will need later on.

```bash
sudo apt update && sudo apt install git perl
```


**Step 08: Tuning the system**
The following commands are based on the canonical instructions for tuning your Linux system for audio work.
**Warning**: These will alter config files on your system, use at your own risk and only on a fresh Raspbian installation.
Mads Kjeldgaard gathered these in a handy gist, so you can execute them just by copy-pasting his long command:

```bash
git clone https://gist.github.com/madskjeldgaard/c5731e95bc5be9b3e2789b14b1149b6e && mv c5731e95bc5be9b3e2789b14b1149b6e raspiaudiotune && cd raspiaudiotune && chmod +x raspiaudiotune.sh && ./raspiaudiotune.sh && cd ~ && rm -rf raspiaudiotune
```

To make these changes take effect, the Pi must be rebooted

```bash
sudo reboot
```


**Step 09: Install and setup Jack**
Jack is used to patch audio throughout your audio system on Linux.
Let’s install and setup Jack:

```bash
sudo apt-get install jackd2
```

Jack has a configuration file in *\~/.jackdrc* that we will set up on installation, but you can edit this anytime to tune the system’s settings using a text editor by running

```bash
vi ~/.jackdrc. 
```

The config file consists of a *jackdcommand* which will be run when we boot the audio server in there.

Create config file in home folder called *.jackdrc:*

```bash
echo /usr/bin/jackd -P75 -dalsa -dhw:2 -r48000 -p512 -n2 > ~/.jackdrc
```

Explanations of the flags used here:
```
-P75 - the real-time priority of the audio
-dhw:2 is PiSound device number.
-r48000 is PiSound sample rate.
-p512 is the block size. This can be tuned to achieve lower latency. Must be power of two.
-n2 - Jack’s buffer periods. Blokas recommends using 2 here for Pisound.
```

**Step 10: Disable the on-board audio output**
I did this because EYESY is looking for your sound card to be the "default" device, so I guessed it'd be easier to disable the others :slight_smile:
To disable the on board Jack output on the Pi open up the *boot config* file

```bash
sudo vi /boot/config.txt
```

Find the line that says *dtparam=audio=on* and comment it out so that it looks like this:
```
#dtparam=audio=on
```

Then reboot, and run `aplay -l` to verify only PiSound is listed.


**Step 11: Install Pisound Drivers (to use the button)**
Blokas provides an installer script. You can download it directly into the shell so it runs immediately:

```bash
curl https://blokas.io/pisound/install-pisound.sh | sh
```

You may have to enter your password, since installation runs with sudo.
At the end of the script you can verify that the drivers are installed, and that the Pisound hardware is all operating with the O.S.
Run this to see the list of audio output devices:

```bash
aplay -l
```

You should see only PiSound listed in the list.
Run this to see the list of audio input devices:

```bash
arecord -l
```

Run this to see the list of MIDI devices:

```bash
aconnect -l
```


**Step 12: Check your system’s configuration**
If you haven’t rebooted yet, go ahead and `sudo reboot`. And then wait for the Pi to power back up again before ssh’ing in to continue.

*realTimeConfigQuickScan* is a nice script that you can use to see if your system is setup correctly. Download and run it like this:

```bash
git clone git://github.com/raboof/realtimeconfigquickscan.git
cd realtimeconfigquickscan
perl ./realTimeConfigQuickScan.pl
```


**Step 13: Watchdog**
If you are using your Pi for a live gig or an installation, setting up a watchdog can be a good idea. If your Pi gets overexcited or crashes, the watchdog will reboot the system (which as a consequence will trigger whatever startup script you have installed, if any).

```bash
sudo apt install watchdog
```

Open up the config file for the watchdog: */etc/watchdog.conf*
Uncomment the following:
```
max-load-1 = 24
min-memory = 1
watchdog-device = /dev/watchdog
```

Then add the following:
```
watchdog-timeout=15
```

The watchdog can be run and activated automatically using *systemd*. This is done using the following commands:

```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
```

To test if the watchdog is doing it’s job, you can stress the system by creating a so-called fork bomb which will make the system crash by recursively calling a function until the Pi chokes up.
On the Pi **(not your main computer!)**, execute the following fork bomb:

```bash
forkbomb(){ forkbomb | forkbomb & }; forkbomb
```

Wait a bit and then see your Pi crash. After choking up, it should automatically reboot itself. If it does this, your watchdog is doing it’s job.


**Step 14: Backup**
It’s a good idea to back up your sd card at this point.
I followed this instructions:

https://thepihut.com/blogs/raspberry-pi-tutorials/17789160-backing-up-and-restoring-your-raspberry-pis-sd-card


**Step 15: Graphic Login**
You can work with your Pi entirely from the ssh connection. But having a graphical desktop on the Pi often makes setting up patches, and debugging them much much easier.

On your computer, install RealVNC Viewer:

https://www.realvnc.com/en/connect/download/viewer

Run it and connect to your Pi.
You’ll need to enter login information twice, once so RealVNC connect to the Pi and then once to the Pi screen that comes up.


**Step 16: Install VideoSynth Eyesy (by Okyeron)**
Open a terminal and type the following:

```bash
git clone https://github.com/okyeron/EYESY_OS_for_RasPi.git Eyesy
cd Eyesy
./deploy.sh
```

This will install Pure Data and over 700 MB of packages.


**Step 17: Install *amidiauto* to control MIDI on Pisound**
Run in the Terminal:

```bash
sudo apt-get update && sudo apt-get install amidiauto
```

Then to enable MIDI thru on Pisound copy the following lines in */etc/amidiauto.conf* (if you can't find the file, create it):
```
\[allow\] 
 \* <-> \*
pisound <-> pisound
puredata <-> pisound
```

Now open Pure Data and under Media select Alsa MIDI.

Before you run EYESY and play with the MIDI the first time, an **IMPORTANT NOTE** on the MIDI CC setup:
CC34 doesn't work correctly, instead of modifying the input gain of EYESY, it actually mute your audio input (Midi 0 to127 result in a gain stage of 0.00% to 0.29%). To restore the original setup you need to reinstall the entire Eyesy folder on the Pi.


**Step 18: The Button**
In order to use the Pi headless in a live situation, I wanted to set the button to start and stop Eyesy directly.
Follow this tutorial to locate the right folder where you'll create two files *start_eyesy.sh* and *stop_eyesy.sh:*

https://blokas.io/pisound/docs/the-button/

In *start_eyesy.sh* paste the following:

```
#!/bin/sh
. /usr/local/pisound/scripts/common/common.sh
flash_leds 100

#!/bin/bash
cd /home/pi/Eyesy
sudo ./run.sh
```

While in *stop_eyesy.sh* paste the following:
```
#!/bin/sh
. /usr/local/pisound/scripts/common/common.sh
flash_leds 100

#!/bin/bash
cd /home/pi/Eyesy
sudo ./stop.sh
```

Then type `sudo pisound-config` on Terminal and change the button settings as you prefer.
My setup for live performances is:

```
Hold1: start eyesy
Hold3: stop eyesy
Hold5: shutdown
Hold other: do nothing
 
Click1: do nothing
Click2: do nothing
Click3: toggle wifi
Click other: toggle bt
```

Shutdown your Pi, connect a display to the HDMI out and boot up your Pi.
When ready, hold down the button for 1 second and you'll see the EYESY logo.
Audio and MIDI should work as expected, to test them follow the "Control via Midi" section from Okyeron Github page:

https://github.com/okyeron/EYESY_OS_for_RasPi


**Step 19: Clean and clone**
To removes packages which are not longer needed from the system, run:

```bash
sudo apt autoremove && sudo apt clean
```

Download Piclone (SD Card Copier)

```bash
sudo apt update 
sudo apt install piclone
```

The SD Card Copier application, which can be found on the Accessories menu of the Raspberry Pi Desktop, will copy Raspberry Pi OS from one card to another. To use it, you will need a USB SD card writer.

To back up your existing Raspberry Pi OS installation, put a blank SD card in your USB card writer and plug it into your Pi, and then launch SD Card Copier.


**That's it, at this point you have a running EYESY on your headless Pi, have fun!**