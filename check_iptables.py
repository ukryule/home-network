#!/usr/bin/python 
import argparse
import subprocess
import sys

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

def getIptablesData():
  portdata = { 'packets': list(), 'bytes': list() }
  p = subprocess.Popen('/sbin/iptables -n -L -x -v', shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  for line in p.stdout.readlines():
    data = line.split()
    if len(data) == 10 and data[9][:4] == 'dpt:':
      portdata['packets'].append({
          'protocol': data[8], 'port': data[9][4:],
          'src': data[6], 'dest': data[7], 'value': data[0]})
      portdata['bytes'].append({
          'protocol': data[8], 'port': data[9][4:],
          'src': data[6], 'dest': data[7], 'value': data[1]})
  retval = p.wait()
  return portdata
  
def main():
  parser = argparse.ArgumentParser(
      description='Use iptables to output data for Prometheus')
  parser.add_argument('--prefix', nargs='?', default='nmap',
                      help='Prefix for labels')
  args = parser.parse_args()

  portstats = getIptablesData()
  print outputPrometheusData(portstats, args.prefix + '_')

if __name__ == '__main__':
  main()
