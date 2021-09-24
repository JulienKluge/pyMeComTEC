# pyMeComTEC
A python library to interface with temperature controllers from Meerstetter Engineering

It implements nearly the full MeCom protocol for the TECs up to the specification of 5136AL (30. July 2020).
Excluded APIs are currently everything bootloader related, lookup table related and all deprecated functionalities.
It should work on:
 * TEC-1092 <span style="color:rgb(150,150,150)">(Tested)</span>
 * TEC-1091 <span style="color:rgb(150,150,150)">(Tested)</span>
 * TEC-1161-4A
 * TEC-1089-SV
 * TEC-1161-10A
 * TEC-1122-SV <span style="color:rgb(150,150,150)">(Tested)</span>
 * TEC-1090-HV
 * TEC-1123-HV <span style="color:rgb(150,150,150)">(Tested)</span>


## First Steps
We use the library to first connect to a TEC via USB:
```python
from pyMeComTEC_Serial import TEC_Serial #import the TEC object for serial connections


tec = TEC_Serial(port = "COM10") #connect to port COM10

print("Firmware ID: {}".format(tec.read_firmware_id())) #read the firmware id
print(tec.status()) #read the tec status

#read basic measurements
print("Temp: {} °C - Current {} A - Voltage {} V".format(
    tec.temperature(),
    tec.current(),
    tec.voltage()
))
```


## Future bullet points
 - Lookup table control


## Author
Julien Kluge

Humboldt-Universität zu Berlin

Institut für Physik, AG QOM

Newtonstraße 15, 12489 Berlin, Germany

+49 (0)30 2093-4939