#!/usr/bin/python
"""
A script which reads from a HC-SR04 distance sensor via RaspberryPi, and
then outputs data in a format which can be read by Prometheus reporting the
state of a garage door. See:
https://gpiozero.readthedocs.io/en/stable/api_input.html#distance-sensor-hc-sr04
"""

import argparse
import gpiozero
import os
import time

def write_to_file(filename, value):
  """Write data into the given file in a format that prometheus can read."""
  results = {'distance': value, 'door_open': 0, 'car_in': -1, 'time': -1}
  results['time'] = int(time.time())

  # Hardcoded values. The garage door is expected to be <42cm away from the
  # sensor when open, while the roof of the car is expected to be <90cm
  # away. 
  if value < 42:
    # We don't know the status of the car in this scenario.
    results['door_open'] = 1
  elif value < 90:
    results['car_in'] = 1
  else:
    results['car_in'] = 0
  with open(filename,'w') as outfile:
    for key, val in results.items():
      if val >= 0:
        outfile.write('garage_' + key + ' ' + str(val) + '\n')

def main():
  """Main function to read sensor and update stats."""
  parser = argparse.ArgumentParser(
    description='Pull data from GPIO and write a Prometheus file output')
  parser.add_argument('--file', default='garage.prom',
                      nargs='?', help='File to write')
  parser.add_argument('--delay', nargs='?', default=10, type=int,
                      help='Delay in seconds between readings')
  parser.add_argument('--echo', nargs='?', default=18, type=int,
                      help='GPIO Echo pin')
  parser.add_argument('--trigger', nargs='?', default=23, type=int,
                      help='GPIO Trigger pin')
  parser.add_argument('--remote_file', nargs='?', default='',
                      help='File to write')
  args = parser.parse_args()
  sensor = gpiozero.DistanceSensor(echo=args.echo, trigger=args.trigger)
  while True:
    write_to_file(args.file, sensor.distance * 100)
    # If we've got a remote_file specified, try to scp the file across.
    if args.remote_file:
      os.system('scp ' + args.file + ' ' + args.remote_file)
    time.sleep(args.delay)

if __name__ == '__main__':
  main()
