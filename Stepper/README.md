**This is the code for the stepper motor on the pi4**

dm_driver.py is run when the pi boots the outputs are redirected to Logging.txt
If you want to change this behavior you will need to update launcher.sh
then run chmod 755 launcher.sh to recompile and sudo sh launcher.sh to test
If there are errors on boot the error message will be outputed to ~/logs/cronlog

All the recognized signals are in dm_Driver.py at the bottom check that if you would like to use customStep for obscure controls
For regular controls use the built in functions of motor.py on the other py
There is currently no way to control the stepper from this pi, but that is very easy to change if needed