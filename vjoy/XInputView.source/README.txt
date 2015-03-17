------------------------------------------------------------------------ 
XinputView 1.2 by goodoldmalk 
------------------------------------------------------------------------ 
An open source 360 gamepad input viewer. 

------------------------------------------------------------------------ 
Description: 
------------------------------------------------------------------------ 
XinputView is a simple gamepad input display software based on the 
xinput dynamic-link library and source code written in C#. It renders 
input from an xbox 360 controller of choice and displays the thumbstick 
movement in real time. 

Compatibility: XinputView is tested to work on Windows x86 and x64 
architectures. If anything fails and you can get a hold of me, please 
contact me with the technical report, error messages and any other 
pertinent information so I can track the error. 

------------------------------------------------------------------------ 
How to use: 
------------------------------------------------------------------------ 
XinputView uses context menus. Right click anywhere within the window to 
open the menu. 

Changing the background color: Default (Black)
Right click on the window screen and select 'Set Background'. A window 
will pop up with presets that you can select from. If you want a 
different color expand the window and use the visual palette. 


Selecting a controller: Default (Controller 1).
Xinput chooses the first Xbox controller (gamepad 1) and displays the 
input on a non-resizable screen. To select a different input right click 
anywhere on the window screen and select from the 'Controller' context 
menu. 

Selecting a layout: Default (Stacked view).
You can choose 4 different views by selecting the desired one from the 
context menu in 'Visibility' by right clicking anywhere on the window 
screen. 

Selecting an icon pack: Default (Mountain dew green).
Icon packs come in 3 different flavors: green, blue and red. Select your 
desired color by beating Mass Effect 3 without installing the latest 
DLC. Alternatively, just select the desired color from the 'Icons' 
context menu by right clicking anywhere on the window screen. 

(NEW) Selecting a custom icon pack: You can now select a custom icon 
pack or modify existing icons by going to the ../images/custom_icon/ 
folder. By default the program will start with the basic green pack 
regardless of changes you do to the icon folder. You can reload a new 
green icon pack by selecting it from the context menu. 

Changing icons:
You can edit any of the 4 included icon packs at any time. You must make 
sure of the following: 
	*Icon names must be the same as the originals.
	*Icon dpi resolution should be set to 96.
	*Icons should be saved in PNG-24 or PNG-8 format.
	*All icons must be accounted for, do not delete any of the icons.
Icon pixel size can be diferent but make sure to test your icon sets and 
see if all icons line up. It is easier to line up icons if you create 
bigger images and simply move them around until you get the desired 
position. 


------------------------------------------------------------------------ 
Troubleshooting:
------------------------------------------------------------------------ 
Q: I don't like this icons, can I change them?
A: Absolutely! You can go to the program folder and find the icon sets 
in the /images/ subfolder. Simply overwrite any icon set with your own 
and make sure to respect the image format, naming convention and dpi 
resolution. The custom_icon pack was created with this intention. 

Q: How do I move my icons around?
A: Currently icons position is hard coded. If you respect the icon pixel 
sizes or use the original images as a template you can probably get some 
good results but if you decide to change them then they will most likely 
be off-center. Work around this by using bigger image sizes and simply 
moving the icon around until you nail the position. 

Q: Can I use transparent images?
A: Yes! PNG images can use transparency for some cool effects.

Q: There a white background on my icons, how do I get rid off it?
A: Make sure you save the image transparency when creating your icons.

Q: Why are my icons larger than the ones I saved?
A: Icons need to be saved in 96 dpi resolution. Normally image programs 
use pixels for their dimensions but C# likes to troll everyone and 
consider dpi resolution when handling images. You need to set both pixel 
size and dpi resolution to have it work as you want. A standard 72 dpi 
file image tends to be 1.33 times bigger than a 96 dpi image even if 
they both have the same pixel size. 

Q: Why are my custom icons not loading?
A: Icons require to be saved in .png format with 96 dpi resoltion. Make 
sure you respect the naming convention of the folder you are 
overwritting and do not delete any icons. If you decide to use the green 
icon pack remember that you must reload the pack every time you start 
the program by right-clicking and selecting it from the context menu. 

Q: How do I make my other gamepads work with this program?
A: Currently only xbox 360 gamepads are detected by the program. You 
will need a 360 gamepad emulator. 

Q: I have an xbox 360 controller plugged in but it doesn't show. How do 
I fix this? 
A: Make sure the xbox 360 controller is plugged and you have selected 
the correct controller from the context menu. Wireless controllers will 
not be detected until you turn them on. 

Q: How can I change the xbox pad color?
A: You can't. Sorry.

Q: Help! I get this horrible crash after changing icon files!
A: That's not a question but, make sure that all the image files are 
accounted for. If even 1 of the PNG icon files is missing the program 
will crash. JPG or GIF files are no good. 


Q: Can you do X?
A: Maaaybe... (Nah)

------------------------------------------------------------------------ 
To do: 
------------------------------------------------------------------------ 
*The program does not remember last selected choices. consider creating 
an text or config file to handle this. 

*Maybe PS3 dualshock support... maybe. 