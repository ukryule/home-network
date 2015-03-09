#!/usr/bin/python 
import argparse
import csv
import httplib
import sys
import time

def buildName(name, domain, status):
  return 'network-' + name + '{domain="' + domain + '",status="' + status + '"}'

def requestUrl(domain, path):
  start_time = time.time()
  conn = httplib.HTTPConnection(domain, timeout=10)
  conn.request('GET', path)
  res = conn.getresponse()
  status = res.status
  data = res.read()
  end_time = time.time()
  latency = end_time - start_time
  return status, len(data), latency

def deviceNames(file):
  with open(file, mode='r') as infile:
    reader = csv.reader(infile)
    names = {rows[0].strip():rows[1].strip() for rows in reader
              if len(rows) > 1 and not rows[0] == "#"}
  return names

def outputPrometheusData(stats, prefix):
  output = ''
  for key,value in stats.iteritems():
    if type(value) is list:
      for item in value:
        labels = [lk+'="'+lv+'"' for lk,lv in item.iteritems()
                  if not lk == 'value']
        output += prefix + key + '{' + ','.join(labels) + '} '
        output += str(item['value']) + '\n'
    else:
      output += prefix + key + ' ' + str(value) + '\n'
  return output

def main():
  parser = argparse.ArgumentParser(
      description='Use nmap to output data for Prometheus')
  parser.add_argument('--file', default='/home/david/node_dir/network.prom',
                      nargs='?', help='File to read/write')
  parser.add_argument('--domain', default='www.google.com',
                      nargs='?', help='Domain to request')
  parser.add_argument('--path', default='/gen_204',
                      nargs='?', help='Path to request')
  parser.add_argument('--prefix', nargs='?', default='network',
                      help='Prefix for labels')
  args = parser.parse_args()

  with open(args.file, mode='r') as infile:
    reader = csv.reader(infile, delimiter=' ')
    names = {rows[0].strip():rows[1].strip() for rows in reader
              if len(rows) > 1 and not rows[0] == "#"}
    infile.close()
    status, data_length, timing = requestUrl(args.domain, args.path)
    latency = buildName('timing', args.domain, str(status))
    if latency not in names:
      names[latency] = 0.0
    names[latency] = float(names[latency]) + timing
    count = buildName('count', args.domain, str(status))
    if count not in names:
      names[count] = 0
    names[count] = int(names[count]) + 1
    length = buildName('length', args.domain, str(status))
    if length not in names:
      names[length] = 0
    names[length] = int(names[length]) + data_length

    with open(args.file, 'w') as f:
      for key,value in names.iteritems():
        #print key, value
        f.write(key + ' ' + str(value) + '\n')


if __name__ == '__main__':
  main()
