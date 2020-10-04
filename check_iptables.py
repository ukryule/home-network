#!/usr/bin/python3
"""
A script for use with Prometheus. It calls iptables and parses the data,
outputing it in a format like this:
  nmap_bytes{dest="0.0.0.0/0",src="0.0.0.0/0",protocol="udp",port="25565"} 0
  nmap_bytes{dest="0.0.0.0/0",src="10.1.10.0/24",protocol="tcp",port="22"} 7810
  nmap_bytes{dest="0.0.0.0/0",src="10.1.10.0/24",protocol="tcp",port="80"} 300
  ...
This format is designed to be read by prometheus node_exporter.
"""

import argparse
import subprocess

def output_prometheus_data(stats, prefix):
  """Convert the given dict into data formatted for prometheus to read."""
  output = ''
  for key, value in list(stats.items()):
    if isinstance(value, list):
      for item in value:
        labels = [lk+'="'+lv+'"' for lk, lv in list(item.items())
                  if not lk == 'value']
        output += prefix + key + '{' + ','.join(labels) + '} '
        output += str(item['value']) + '\n'
    else:
      output += prefix + key + ' ' + str(value) + '\n'
  return output

def get_iptables_data():
  """Call iptables, parse and return the data in a sensible dict."""
  portdata = {'packets': list(), 'bytes': list()}
  proc = subprocess.Popen('/sbin/iptables -n -L -x -v', shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  for line in proc.stdout.readlines():
    data = line.split()
    if len(data) == 10 and data[9][:4] == 'dpt:':
      portdata['packets'].append({
          'protocol': data[8], 'port': data[9][4:],
          'src': data[6], 'dest': data[7], 'value': data[0]})
      portdata['bytes'].append({
          'protocol': data[8], 'port': data[9][4:],
          'src': data[6], 'dest': data[7], 'value': data[1]})
  proc.wait()
  return portdata

def main():
  """Main function to call iptables and output stats."""
  parser = argparse.ArgumentParser(
      description='Use iptables to output data for Prometheus')
  parser.add_argument('--prefix', nargs='?', default='nmap',
                      help='Prefix for labels')
  args = parser.parse_args()

  portstats = get_iptables_data()
  print(output_prometheus_data(portstats, args.prefix + '_'))

if __name__ == '__main__':
  main()
