# Home Network Monitoring

This is a set of scripts for monitoring a home network. It assumes the use
of [Prometheus][1] as the underlying monitoring infrastructure, and exports
data in a suitable format.

## CheckIPTables
 - Calls iptables and exports resulting data.

## CheckNetwork
 - Requests the given URL and exports stats around success/failure/latency.

[1]: http://prometheus.io/
