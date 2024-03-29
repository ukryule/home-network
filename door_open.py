#!/usr/bin/python3
"""
A script which sends GPIO signals to open my garage door. This depends on the
correct GPIO setup, and also checks .prom file for status.
"""


import argparse
import csv
import time
import RPi.GPIO as GPIO

IS_ACTIVE = True
CLOSING_ENABLED = True

def read_file_to_dict(filename, delimiter=' '):
  """Simple function to read a (2 column) CSV into a dict."""
  data = dict()
  with open(filename, mode='r') as infile:
    reader = csv.reader(infile, delimiter=delimiter)
    data = {rows[0].strip(): rows[1].strip() for rows in reader
            if len(rows) > 1 and not rows[0] == "#"}
  return data

def open_garage_door(direction='opening', pin=15):
  """Function which sends GPIO signal to open the door."""
  result = direction
  if IS_ACTIVE and (CLOSING_ENABLED or direction == 'opening'):
    # TODO: Write log about opening/closing.
    # Send the GPIO signals to open the door. Keep pin high for 2 seconds.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    GPIO.cleanup()
  else:
    result = '%s not enabled' % direction
  return result

def json_output(value):
  """Simple function to return data in a standard JSON format."""
  return '{"is_open": "%s"}\n' % value

def choose_action(direction, door_state):
  """Decide what action to take and return suitable response."""
  output = 'unknown command %s' % direction
  if direction == 'status':
    output = 'true' if door_state == '1' else 'false'
  elif direction == 'open':
    if door_state == '0':
      output = open_garage_door('opening')
    else:
      output = 'already open'
  elif direction == 'close':
    if door_state == '1':
      output = open_garage_door('closing')
    else:
      output = 'already closed'
  return output

def main():
  """Main function which will open/close garage or return status."""
  parser = argparse.ArgumentParser(
      description='Pull data from GPIO and write a Prometheus file output')
  parser.add_argument('--file',
                      default='/var/lib/prometheus/node-exporter/garage.prom',
                      nargs='?', help='File to read state from')
  parser.add_argument('direction', metavar='open|close|status',
                      default='status',
                      help='Whether to open or close the garage')
  parser.add_argument('--json', action='store_true',
                      help='Output json format')

  args = parser.parse_args()
  data = read_file_to_dict(args.file)
  output = choose_action(args.direction, data['garage_door_open'])
  if args.json:
    output = json_output(output)
  print(output)


if __name__ == '__main__':
  main()
