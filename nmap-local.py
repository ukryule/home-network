#!/usr/bin/python 
import argparse
import nmap
import sys

def dummyStats():
  return {'nmap': {'scanstats': {'uphosts': u'20', 'timestr': u'Sat Feb 21 11:46:17 2015', 'downhosts': u'236', 'totalhosts': u'256', 'elapsed': u'43.17'}, 'scaninfo': {}, 'command_line': u'nmap -oX - -sP 10.1.10.0/24'}, 'scan': {u'10.1.10.8': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'C8:2A:14:0A:93:04', u'ipv4': u'10.1.10.8'}}, u'10.1.10.35': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'B0:34:95:E9:1F:35', u'ipv4': u'10.1.10.35'}}, u'10.1.10.2': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'C4:3D:C7:A3:FF:14', u'ipv4': u'10.1.10.2'}}, u'10.1.10.25': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'5C:C5:D4:0E:8B:A7', u'ipv4': u'10.1.10.25'}}, u'10.1.10.1': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'78:CD:8E:6C:F5:4A', u'ipv4': u'10.1.10.1'}}, u'10.1.10.3': {'status': {'state': u'up', 'reason': u'localhost-response'}, 'hostname': '', 'addresses': {u'ipv4': u'10.1.10.3'}}, u'10.1.10.4': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'C0:3F:0E:AF:3A:3D', u'ipv4': u'10.1.10.4'}}, u'10.1.10.29': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'20:0C:C8:51:7D:09', u'ipv4': u'10.1.10.29'}}, u'10.1.10.21': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'B0:34:95:0E:21:31', u'ipv4': u'10.1.10.21'}}, u'10.1.10.18': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'60:C5:47:05:08:8E', u'ipv4': u'10.1.10.18'}}, u'10.1.10.34': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'30:8C:FB:16:08:E8', u'ipv4': u'10.1.10.34'}}, u'10.1.10.20': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'E8:99:C4:83:76:AB', u'ipv4': u'10.1.10.20'}}, u'10.1.10.14': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'74:DA:38:0E:2A:40', u'ipv4': u'10.1.10.14'}}, u'10.1.10.15': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'70:62:B8:AC:92:D2', u'ipv4': u'10.1.10.15'}}, u'10.1.10.23': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'8C:3A:E3:70:C7:A1', u'ipv4': u'10.1.10.23'}}, u'10.1.10.17': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'18:B4:30:02:72:DA', u'ipv4': u'10.1.10.17'}}, u'10.1.10.10': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'00:24:1E:C7:2E:8B', u'ipv4': u'10.1.10.10'}}, u'10.1.10.11': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'40:F0:2F:59:9E:5B', u'ipv4': u'10.1.10.11'}}, u'10.1.10.12': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'20:0C:C8:47:2B:59', u'ipv4': u'10.1.10.12'}}, u'10.1.10.13': {'status': {'state': u'up', 'reason': u'arp-response'}, 'hostname': '', 'addresses': {u'mac': u'F8:8F:CA:12:49:A4', u'ipv4': u'10.1.10.13'}}}}

def scanHosts(hosts, args):
  nm = nmap.PortScanner()
  return nm.scan(hosts=hosts, arguments=args)

def deviceNames():
  names = {
    '78:CD:8E:6C:F5:4A': 'Main modem/router',
    'C4:3D:C7:A3:FF:14': 'Netgear WiFi',
    'C8:CB:B8:C5:2F:35': 'Home Server (HP)',
    'C0:3F:0E:AF:3A:3D': 'Nas',
    'C8:2A:14:0A:93:04': 'Mac Mini',
    '00:24:1E:C7:2E:8B': 'Wii',
    '40:F0:2F:59:9E:5B': 'Chromebook (Work)',
    '20:0C:C8:47:2B:59': 'Powerline #1',
    'F8:8F:CA:12:49:A4': 'Google Glass',
    '74:DA:38:0E:2A:40': 'Raspberry Pi',
    '70:62:B8:AC:92:D2': 'Garage powerplug',
    'A0:B3:CC:06:61:FC': 'Printer',
    '18:B4:30:02:72:DA': 'Nest',
    '60:C5:47:05:08:8E': 'Macbook Air',
    '30:85:A9:DC:DC:B7': 'Nexus 7',
    'E8:99:C4:83:76:AB': 'Ariel\'s Phone',
    'B0:34:95:0E:21:31': 'iPad',
    'A0:0B:BA:8F:99:AD': 'Alexander\'s Phone',
    '8C:3A:E3:70:C7:A1': 'Wonk\'s phone',
    'B8:76:3F:20:68:7F': 'Alexander\'s laptop',
    '5C:C5:D4:0E:8B:A7': 'Ariel\'s Chromebook',
    'D0:E7:82:7B:44:68': 'Chromecast \'livingroom\'',
    '6C:AD:F8:2B:42:F3': 'Chromecast Projector',
    '00:26:37:8A:15:74': 'Nexus S',
    '20:0C:C8:51:7D:09': 'Powerline #2',
    'F8:1E:DF:E8:87:B5': 'MacBookPro wireless',
    '34:15:9E:20:91:F8': 'MacBookPro wired',
    '30:8C:FB:16:08:E8': 'Dropcam',
    # Other devices
    '00:EE:BD:59:40:7C': 'Liang HuiChing\'s phone',
  }
  return names

def parseHostInfo(nminfo, local_mac):
  nmapstats = dict()
  nmapstats['uphosts'] = nminfo['nmap']['scanstats']['uphosts']
  nmapstats['readtime'] = nminfo['nmap']['scanstats']['elapsed']
  nmapstats['up'] = list()
  nmapstats['details'] = list()
  names = deviceNames()
  for ip in nminfo['scan'].keys():
    ipinfo = nminfo['scan'][ip]
    if 'addresses' in ipinfo:
      if 'mac' in ipinfo['addresses']:
        mac = ipinfo['addresses']['mac']
      elif ('status' in ipinfo and 'reason' in ipinfo['status'] and
            ipinfo['status']['reason'] == 'localhost-response'):
        mac = local_mac
      else:
        mac = ''
      if mac in names:
        name = names[mac]
        del(names[mac])
      else:
        name = 'UNKNOWN'
      isup = int('status' in ipinfo and 'state' in ipinfo['status']
                 and ipinfo['status']['state'] == 'up')
      if mac:
        nmapstats['up'].append({'mac': mac, 'name': name, 'value': isup})
      nmapstats['details'].append(
          {'mac': mac, 'name': name, 'ip': ip, 'value': isup})
  for mac,name in names.iteritems():
    nmapstats['up'].append({'mac': mac, 'name': name, 'value': 0})
  return nmapstats

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
  parser.add_argument('--netmask', nargs='?', default='10.1.10.0/24',
                      help='Netmask of network to be scanned')
  parser.add_argument('--mac', nargs='?', default='localhost',
                      help='MAC address of local machine')
  parser.add_argument('--prefix', nargs='?', default='nmap',
                      help='Prefix for labels')
  parser.add_argument('--dummy', nargs='?', default=False, type=bool,
                      help='Whether to use dummy data')
  args = parser.parse_args()

  if args.dummy:
    nminfo = dummyStats()
  else:
    nminfo = scanHosts(args.netmask, '-sP')
  nmapstats = parseHostInfo(nminfo, args.mac)
  print outputPrometheusData(nmapstats, args.prefix + '_')


if __name__ == '__main__':
  main()
