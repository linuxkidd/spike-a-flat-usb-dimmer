# spike-a-flat.py
Python script to control the [Spike-a USB Dimmer](http://www.spike-a.com/USBDimmer) for their [Spike-a Flat Fielder](http://www.spike-a.com/flatfielders/).

##### Usage:
- Run without any parameter to get the current intensity of the panel
- Run with a numeric paramter from 0 to 1023 to set the intensity of the panel
- The script will always print the final intensity value upon exit

**NOTE:** The script will have a delay associated with the time it takes for the panel to ramp between the current and set intensity levels.  This is normal, please be patient.

##### Example:
```
$ ./spike-a-flat.py
0

$ ./spike-a-flat.py 100
100

$ ./spike-a-flat.py
100

$ ./spike-a-flat.py 500
500
```
