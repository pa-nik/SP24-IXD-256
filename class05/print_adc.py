# convert ADC input to 8-bit range and print the result

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

title0 = None
label0 = None
adc1 = None
adc1_val = None

def setup():
  global label0, adc1
  M5.begin()
  # initialize display title and label on M5Stack AtomS3:
  title0 = Widgets.Title("print ADC", 3, 0x000000, 0xffffff, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("--", 3, 20, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
  # initialize analog to digital converter on pin 1:
  adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)

# function to map input value range to output value range:
def map_value(in_val, in_min, in_max, out_min, out_max):
  out_val = out_min + (in_val - in_min) * (out_max - out_min) / (in_max - in_min)
  if out_val < out_min:
    out_val = out_min
  elif out_val > out_max:
    out_val = out_max
  return int(out_val)

def loop():
  global label0, adc1, adc1_value
  M5.update()

  # read ADC value:
  adc1_val = adc1.read()

  # map the ADC value from 0-4095 to 0-255 (8-bit) range:
  adc1_val_8bit = map_value(adc1_val, 0, 4095, 0, 255)
  
  # print the 8-bit ADC value:
  print(str(adc1_val_8bit))
        
  # show 8-bit ADC value on display label:
  label0.setText(str(adc1_val_8bit))

  time.sleep_ms(500)

if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")

