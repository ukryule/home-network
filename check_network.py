#!/usr/bin/python3
"""
A script for use with Prometheus. It requests a url and then updates stats
based on this. It reads/writes stats in this format:
  network_timing{domain="www.google.com",status="204"} 2.07937192917
  network_count{domain="www.google.com",status="/generate_204"} 3
  ...
This format is designed to be read by prometheus node_exporter.
"""

import argparse
import csv
import socket
import time
import http.client

def request_url(domain, path, timeout):
  """Get the given url and return basic stats."""
  start_time = time.time()
  try:
    conn = http.client.HTTPConnection(domain, timeout=timeout)
    conn.request('GET', path)
    res = conn.getresponse()
    status, data, success = res.status, res.read(), 1
  except socket.timeout:
    status, data, success = 0, '', 0
  end_time = time.time()
  latency = end_time - start_time
  return status, len(data), latency, success

def read_file_to_dict(filename, delimiter=' '):
  """Simple function to read a (2 column) CSV into a dict."""
  data = dict()
  with open(filename, mode='r') as infile:
    reader = csv.reader(infile, delimiter=delimiter)
    data = {rows[0].strip():rows[1].strip() for rows in reader
              if len(rows) > 1 and not rows[0] == "#"}
  return data

def write_dict_to_file(filename, data, delimiter=' '):
  """Write dict back into the given file."""
  with open(filename, 'w') as outfile:
    for key, value in list(data.items()):
      outfile.write(key + delimiter + str(value) + '\n')

def increment_value(data, key, value, type_func):
  """Increment key/domain/status tuple in data with the given value."""
  if key not in data:
    data[key] = 0
  data[key] = type_func(data[key]) + value

def update_network_stats(filename, prefix, domain, path, timeout):
  """Update data in given file with stats from requesting the given url."""
  data = read_file_to_dict(filename)
  status, data_length, timing, success = request_url(domain, path, timeout)
  # Build the key from the prefix, domain and status.
  key = '%s_%s{domain="%s",status="%s"}' % (prefix, '%s', domain, status)
  increment_value(data, key % 'timing', timing, float)
  increment_value(data, key % 'count', 1, int)
  increment_value(data, key % 'success', success, int)
  increment_value(data, key % 'length', data_length, int)
  write_dict_to_file(filename, data)

def main():
  """Main function to update network stats."""
  parser = argparse.ArgumentParser(
      description='Use nmap to output data for Prometheus')
  parser.add_argument('--file', default='/home/david/node_dir/network.prom',
                      nargs='?', help='File to read/write')
  parser.add_argument('--domain', default='www.google.com',
                      nargs='?', help='Domain to request')
  parser.add_argument('--path', default='/generate_204',
                      nargs='?', help='Path to request')
  parser.add_argument('--prefix', nargs='?', default='network',
                      help='Prefix for labels')
  parser.add_argument('--timeout', nargs='?', default=10, type=int,
                      help='Timeout in seconds for HTTP request')
  args = parser.parse_args()
  update_network_stats(
      args.file, args.prefix, args.domain, args.path, args.timeout)

if __name__ == '__main__':
  main()
