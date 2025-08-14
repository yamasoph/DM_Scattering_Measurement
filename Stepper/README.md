This is the code for the stepper motor on the pi4

dm_driver.py is run when the pi boots the outputs are redirected to Logging.txt
If you want to change this behavior you will need to update launcher.sh
then run chmod 755 launcher.sh to recompile and sudo sh launcher.sh to test
If there are errors on boot the error message will be outputed to ~/logs/cronlog