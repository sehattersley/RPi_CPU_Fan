#!/usr/bin/python
# Aurthor: sehattersley
# Purpose: Turn a fan on if the CPU temperature goes above a set value.
# Notes: Run this code as a cron job. Dont have the fan on and off temperatures close together or the fan will constantly be switching.



# --- Imports ---
import os
import RPi.GPIO as GPIO



# --- Control Settings ---
nPin = 18 # GPIO number
nFanOnSetting_C = 60 # Fan on setting. Anything below 80 Deg C is ok.
nFanOffSetting_C = 50
bDebugPrint = 0 # Set to 1 to show debug print statements



# --- Functions ---
def Initialise():
	GPIO.setwarnings(False) # Disable warning such as channel already in use
    GPIO.setmode(GPIO.BCM) # Reference pins by GPIO number. Use BOARD instead of BCM if you want to use pin numbers.
    GPIO.setup(nPin, GPIO.OUT) # Set pin as an output

def Get_CPU_Temperature():
    sTemperature_C = os.popen("vcgencmd measure_temp").readline()
    if bDebugPrint == 1:
    	print ("CPU temperature in its raw format: " + sTemperature_C)
    sTemperature_C = (sTemperature_C.replace("temp=",""))
    sTemperature_C = (sTemperature_C.replace("'C\n",""))
    if bDebugPrint == 1:
    	print ("CPU Temperature with leading and trailing text removed: " + sTemperature_C)
    return (sTemperature_C)



# --- Main Code ---
Initialise() # Set GPIO pins up etc

fCPUTemp_C = float(Get_CPU_Temperature()) # Get CPU temperature and convert it to float

if fCPUTemp_C > nFanOnSetting_C:
    GPIO.output(nPin, True) # Set pin high
    if bDebugPrint == 1:
        print("Temperature setting is " + str(nFanOnSetting_C) + ". Turning Fan on")
elif fCPUTemp_C < nFanOffSetting_C:
    GPIO.output(nPin, False) # Set pin low
    if bDebugPrint == 1:
        print("Temperature setting is " + str(nFanOnSetting_C) + ". Turning fan off")

if bDebugPrint == 1:
	print("End of script")