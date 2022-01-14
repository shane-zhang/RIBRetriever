# python bgp-anycast-arg-pre.py 1641873600000 1641997800000 20220111PeeringRes.plk 184.164.235.0/24
from _pybgpstream import BGPStream
import pickle as plk
import sys

# Create a new bgpstream instance and a reusable bgprecord instance
stream = BGPStream(collectors = [ "route-views2", "route-views.linx", "route-views4", "route-views2.saopaulo", "route-views.eqix", "route-views.amsix", "route-views.chicago", "route-views.sg", "route-views.telxatl", "route-views.sydney", "route-views.sfmix", "route-views.flix", "route-views.napafrica", "route-views.isc", "route-views.saopaulo", "route-views.rio", "route-views.fortaleza", "route-views.wide", "route-views.nwax", "route-views.perth", "route-views.chile", "route-views.kixp" ] )

# Consider RIPE RRC 10 only
#stream.add_filter("prefix","8.8.8.0/24")
#stream.add_filter('collector',[ "route-views2", "route-views.linx", "route-views4", "route-views2.saopaulo", "route-views.eqix", "route-views.amsix", "route-views.chicago", "route-views.sg", "route-views.telxatl", "route-views.sydney", "route-views.sfmix", "route-views.flix", "route-views.napafrica", "route-views.isc", "route-views.saopaulo", "route-views.rio", "route-views.fortaleza", "route-views.wide", "route-views.nwax", "route-views.perth", "route-views.chile", "route-views.kixp" ])
stream.add_filter('prefix',sys.argv[4])
#stream.add_filter('prefix','199.7.91.0/24')

# Consider this time interval:
# Sat Aug  1 08:20:11 UTC 2015

stream.add_filter('project', 'routeviews')
stream.add_interval_filter(int(sys.argv[1])//1000, int(sys.argv[2])//1000)

# Start the stream
stream.start()

bgp_info = []

# Get next record
rec = stream.get_next_record()
while(rec):
    # Print the record information only if it is not a valid record
#    print (rec.project,"|", rec.collector,"|", rec.type,"|", rec.time,"|", rec.status)
    elem = rec.get_next_elem()
    while(elem):
        # Print record and elem information
#        print (rec.project,"|", rec.collector,"|", rec.type,"|", rec.time,"|" ,rec.status,"|",elem.type,"|", elem.peer_address,"|", elem.peer_asn,"|", elem.fields)
        bgp_info.append([rec.project, rec.collector, rec.type, rec.time, rec.status,elem.type, elem.peer_address, elem.peer_asn, elem.fields])
        elem = rec.get_next_elem()
    rec = stream.get_next_record()
plk.dump(bgp_info,open(sys.argv[3],"wb"))
