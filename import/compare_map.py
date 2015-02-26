#! /usr/bin/python3

# Copyright (C) 2015 Aun Johnsen <skippern@gimnechiske.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
import ogr
import json
#import shapely
from shapely.geometry import shape, mapping, LineString

if len(sys.argv) < 3:
    print("Usage: python compare_map.py shapefile jsonfile")
    sys.exit()
else:
    shapefile = sys.argv[1] # ogr2ogr sort for one municipality only
    jsonfile = sys.argv[2] # result of download_area.py (one municipality)

# Global variables we will need
# Overpass.json node: {"type": "node", "id": 267436610, "lat": -20.6646228, "lon": -40.5008067, "tags": { "highway": "traffic_signals" } },
# Overpass.geojson node: {"type": "Feature", "id": "node/267436610", "properties": { "@id": "node/267436610", "highway": "traffic_signals" },"geometry": {"type": "Point", "coordinates": [ -40.5008067, -20.6646228 ] } },
# What we need: {"type": "Point", "id": 267436610, "coordinates": [ -40.5008067, -20.6646228 ] }
#node = '{"type": "Point", "id": $id, "coordinates": [ $lon, $lat ] }'

nodeList = []
wayList = []

print("Loading data from "+jsonfile)

data=open(jsonfile)
jsonFull = json.load(data)
data.close()

for element in jsonFull['elements']:
    if (element['type'] == "way" ): wayList.append(element)
    if (element['type'] == "node" ): nodeList.append('{"type": "Point", "coordinates": [ '+ str(element['lon']) + ', ' + str(element['lat']) + '], "id": '+str(element['id']) + ' }')
tmp = '{"nodes": [' + ','.join(nodeList)+'] }'
nodeJSON = json.loads(tmp)

print(" Ways: " + str(len(wayList)) )
print("Nodes: " +str(len(nodeList)))

JSONwayLength = 0
namedWayLength = 0
unNamedWayLength = 0

#here we need to make the way objects
for way in wayList:
    tags = way["tags"]
    myNodes = []
    for wayNode in way["nodes"]:
        thisNode = False
        nodeIndex = 0
        while (thisNode == False):
            if (nodeJSON['nodes'][nodeIndex]['id'] == wayNode):
                myNodes.append(nodeJSON['nodes'][nodeIndex]["coordinates"])
                nodeIndex = nodeIndex + 1
                thisNode = True
            else: nodeIndex = nodeIndex + 1
    #lets create a way
    tmpA = []
    for i in myNodes:
        tmp = ( i[0] , i[1] )
        tmpA.append(tmp)
    thisWay = LineString(tmpA)
    JSONwayLength = JSONwayLength + (thisWay.length * 60 * 1852)
    try:
        name = tags['name']
        namedWayLength = namedWayLength + (thisWay.length * 60 * 1852)
    except:
        unNamedWayLength = unNamedWayLength + (thisWay.length * 60 * 1852)

print("Total length of ways in JSON file: " + ('%.3f' % (JSONwayLength / 1000)) + "km (avg way lenght: " + ('%.2f' % (JSONwayLength / len(wayList))) + "m / node distane: " + ('%.2f' % (JSONwayLength / len(nodeList))) + "m)")
print("Named way: " + ('%.3f' % (namedWayLength / 1000)) + "km, unnamed: " + ('%.3f' % (unNamedWayLength / 1000)) + "km")

#s = shape(json.loads(nodeList[0]))
#print(s)
#print(json.dumps(mapping(s)))
