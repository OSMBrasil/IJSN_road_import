#! /usr/bin/python
# -*- coding: utf-8 -*-

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
from shapely.geometry import shape, mapping, LineString, MultiLineString, Point

if len(sys.argv) < 3:
    print("Usage: python compare_map.py shapefile jsonfile")
    sys.exit()
else:
    shapefile = sys.argv[1] # ogr2ogr sort for one municipality only
    jsonfile = sys.argv[2] # result of download_area.py (one municipality)
#    shapefile = unicode(sys.argv[1].encode('utf-8')) # ogr2ogr sort for one municipality only
#    jsonfile = unicode(sys.argv[2].encode('utf-8')) # result of download_area.py (one municipality)

# Global variables we will need

#print shapefile, jsonfile

nodeList = []
wayList = []

try:
    data=open(jsonfile)
    jsonFull = json.load(data)
    data.close()
except:
    print "ERROR: JSON file not valid"
    sys.exit(1)

try:
    data=open(shapefile)
    shapeFull = json.load(data)
    data.close()
except:
    print "ERROR: shapefile not valid"
    sys.exit(1)

try:
    jsonFull = json.loads(jsonFull)
except:
    pass

for element in jsonFull.get("elements"):
    try:
        version = element['version']
    except:
        version = None
    if (element['type'] == "way" ):
        if (version != None): wayList.append(element)
    if (element['type'] == "node" ):
        if (version != None): nodeList.append('{"type": "Point", "coordinates": [ '+ str(element['lon']) + ', ' + str(element['lat']) + '], "id": '+str(element['id']) + ' }')
nodeJSON = json.loads('{"nodes": [' + ','.join(nodeList)+'] }')

print(" Ways: " + str(len(wayList)) )
print("Nodes: " +str(len(nodeList)))


if len(wayList) is 0:
    print("No OSM Data available (data file contains 0 ways)")
    sys.exit(1)

JSONwayLength = 0
namedWayLength = 0
unNamedWayLength = 0
ShapeWayLength = 0
ShapeNamedWay = 0
ShapeUnnamedWay = 0
OverpassWays = []
ShapeWays = []
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
        tmpA.append( ( i[0] , i[1] ) )
    thisWay = LineString(tmpA)
    JSONwayLength = JSONwayLength + (thisWay.length * 60 * 1852)
    try:
        name = tags['name']
        namedWayLength = namedWayLength + (thisWay.length * 60 * 1852)
    except:
        unNamedWayLength = unNamedWayLength + (thisWay.length * 60 * 1852)
    OverpassWays.append(thisWay)

for way in shapeFull['features']:
    tags = way["properties"]
    myNodes = [ ]
    for wayNode in way["geometry"]["coordinates"]:
        myNodes.append( ( wayNode[0], wayNode[1] ))
    thisWay = LineString(myNodes)
    ShapeWayLength = ShapeWayLength + (thisWay.length * 60 * 1852)
    name = tags['name']
    if (name != None):
        ShapeNamedWay = ShapeNamedWay + (thisWay.length * 60 * 1852)
    else:
        ShapeUnnamedWay = ShapeUnnamedWay + (thisWay.length * 60 * 1852)
    ShapeWays.append(thisWay)

print("Total length of ways in JSON file: " + ('%.3f' % (JSONwayLength / 1000)) + "km (avg way lenght: " + ('%.2f' % (JSONwayLength / len(wayList))) + "m / node distance: " + ('%.2f' % (JSONwayLength / len(nodeList))) + "m)")
print("Named way: " + ('%.3f' % (namedWayLength / 1000)) + "km, unnamed: " + ('%.3f' % (unNamedWayLength / 1000)) + "km")
print("Total length of ways in Shapefile: " + ('%.3f' % (ShapeWayLength / 1000)) + "km (" + str(len(ShapeWays)) + " ways)")
print("Named way: " + ('%.3f' % (ShapeNamedWay / 1000)) + "km, unnamed: " + ('%.3f' % (ShapeUnnamedWay / 1000)) + "km")

newNodes = []
newWays = []
modifiedWays = []
createXML = ""
modifyXML = ""
manualCheck = []
bufferInMeter = 5
buffer = (bufferInMeter / (60 * 1852))

# Time to starte analyse
for Oway in wayList:
    iChanged = 0
    waysAreEqual = 0
    tags = Oway["tags"]
    try:
        Oname = tags['name']
    except:
        Oname = None
    try:
        OaltName = tags['alt_name']
    except:
        OaltName = None
    try:
        Oref = tags['ref']
    except:
        Oref = None
    try:
        Ohighway = tags['highway']
    except:
        Ohighway = None
    try:
        Osurface = tags['surface']
    except:
        Osurface = None
    try:
        Ononame = tags['noname']
    except:
        Ononame = None
    try:
        Obridge = tags['bridge']
    except:
        Obridge = None
    try:
        Ojunction = tags['junction']
    except:
        Ojunction = None
    try:
        Olanes = tags['lanes']
    except:
        Olanes = None
    try:
        Olayer = tags['layer']
    except:
        Olayer = None
    myNodes = []
    for wayNode in Oway["nodes"]:
        thisNode = False
        nodeIndex = 0
        while (thisNode == False):
            if (nodeJSON['nodes'][nodeIndex]['id'] == wayNode):
                myNodes.append(nodeJSON['nodes'][nodeIndex]["coordinates"])
                nodeIndex = nodeIndex + 1
                thisNode = True
            else: nodeIndex = nodeIndex + 1
    tmpA = []
    for i in myNodes:
        tmpA.append(( i[0] , i[1] ))
    thisOWay = LineString(tmpA)
    for Sway in shapeFull['features']:
        properties = Sway['properties']
        try:
            Sname = properties['name']
        except:
            Sname = None
        try:
            SaltName = properties['alt_name']
        except:
            SaltName = None
        try:
            Sref = properties['ref']
        except:
            Sref = None
        try:
            Shighway = properties['highway']
        except:
            Shighway = None
        try:
            Ssurface = properties['surface']
        except:
            Ssurface = None
        try:
            Snoname = properties['noname']
        except:
            Snoname = None
        try:
            Sbridge = properties['bridge']
        except:
            Sbridge = None
        try:
            Sjunction = properties['junction']
        except:
            Sjunction = None
        try:
            Slanes = properties['lanes']
        except:
            Slanes = None
        try:
            Slayer = properties['layer']
        except:
            Slayer = None
        myNodes = []
        for wayNode in Sway['geometry']['coordinates']:
            myNodes.append( ( wayNode[0], wayNode[1] ) )
        thisSWay = LineString(myNodes)
        # compare the two ways
        if thisOWay.within(thisSWay.buffer(buffer)):
            #print ("O", end=''),
            waysAreEqual = 1
#        if thisSWay.within(thisOWay.buffer(buffer)):
#            print ("S", end=''),
        if thisOWay.almost_equals(thisSWay, 5):
            #print ("5", end=''),
            waysAreEqual = 1
        if thisOWay.almost_equals(thisSWay, 4):
            #print ("4", end=''),
            waysAreEqual = 1
        if thisOWay.almost_equals(thisSWay, 3):
            #print ("3", end=''),
            waysAreEqual = 1
#        if thisOWay.almost_equals(thisSWay, 2):
#            print ("2", end=''),
#        if thisOWay.intersects(thisSWay):
#            print ("i", end=''),
#        if thisOWay.touches(thisSWay):
#            print ("t", end=''),
#        if thisOWay.crosses(thisSWay):
#            print ("c", end=''),
        # Let us build a new object, something have changed
        if (waysAreEqual == 1):
            if (Sname != Oname):
                iChanged = 1
                if (OaltName != None):
                    if (Oname != None): OaltName = Oname + ";" + OaltName
                elif (Oname == Sname): break
                else: OaltName = Oname
                Oname = Sname
            if (SaltName != None):
                iChanged = 1
                if (OaltName == None): OaltName = SaltName
                else: OaltName = OaltName + ";" + SaltName
            if (Sref != None):
                if (Oref == None):
                    Oref = Sref
                    iChanged = 1
                elif (Oref != Sref): manualCheck.append(json.loads('{"id": '+str(Oway['id'])+', "reason": "ref='+str(Oref)+' not equal ' +str(Sref)+'"}'))
            if (Ohighway == "road"):
                Ohighway = Shighway
                iChanged = 1
            if (Ohighway != Shighway): manualCheck.append(json.loads('{"id": '+str(Oway['id'])+', "reason": "highway='+str(Ohighway)+' not equal ' +str(Shighway)+'"}'))
            if (Osurface == None):
                if (Ssurface != None):
                    Osurface = Ssurface
                    iChanged = 1
            else:
                if (Osurface != Ssurface): manualCheck.append(json.loads('{"id": '+str(Oway['id'])+', "reason": "surface='+str(Osurface)+' not equal '+str(Ssurface)+'"}'))
            if (Sbridge != None):
                if (Obridge == None):
                    Obridge = Sbridge
                    iChanged = 1
                else:
                    if (Obridge != Sbridge): manualCheck.append(json.loads('{"id": '+str(Oway['id'])+', "reason": bridge='+str(Obridge)+' not equal '+str(Sbridge)+'"}'))
            if (Sjunction != None):
                if (Ojunction == None):
                    Ojunction = Sjunction
                    iChanged = 1
            if (Olanes == None):
                if (Slanes != None):
                    Olanes = Slanes
                    iChanged = 1
            else:
                if (Olanes != Slanes): manualCheck.append(json.loads('{"id": '+str(Oway['id'])+', "reason": "lanes='+str(Olanes)+' not equal ' +str(Slanes)+'"}'))
            if (Slayer != None):
                if (Olayer == None):
                    Olayer = Slayer
                    iChanged = 1
        waysAreEqual = 0
        if (iChanged == 1):
            if (Oname != None): Oway['tags']['name'] = Oname
            if (OaltName != None): Oway['tags']['alt_name'] = OaltName
            if (Oref != None): Oway['tags']['ref'] = Oref
            if (Ohighway != None): Oway['tags']['highway'] = Ohighway # if this change we have a bug!
            if (Olanes != None): Oway['tags']['lanes'] = Olanes
            if (Olayer != None): Oway['tags']['layer'] = Olayer
            if (Obridge != None): Oway['tags']['bridge'] = Obridge
            if (Ojunction != None): Oway['tags']['junction'] = Ojunction
            if (Osurface != None): Oway['tags']['surface'] = Osurface
            if (Oname == None):
                if (Ononame == None): Ononame = "yes"
            if (Ononame != None): Oway['tags']['noname'] = Ononame
            if Oway not in modifiedWays:
                modifiedWays.append(Oway)
            iChanged = 0
            break

oldWay = MultiLineString(OverpassWays).buffer(buffer)
for Sway in shapeFull['features']:
    myNodes = []
    for wayNode in Sway['geometry']['coordinates']:
        myNodes.append( ( wayNode[0], wayNode[1] ) )
    thisSWay = LineString(myNodes)
    myNodes = []
    if (thisSWay.intersects(oldWay) == False):
        for i in Sway['geometry']['coordinates']:
            proximity = Point( ( float(i[0]), float(i[1]) ) ).buffer( buffer )
            nodeID = None
            while nodeID is None:
                for j in newNodes:
                    if (Point( (j['lon'], j['lat'])).within(proximity)):
                        nodeID = j['id']
                for j in nodeJSON['nodes']:
                    if (Point( ( float(j['coordinates'][0]), float(j['coordinates'][1]) ) ).within(proximity)):
                        nodeID = j['id']
                if (nodeID == None):
                    nodeID = ( (len(newNodes) + len(newWays) + 1) * -1)
            if (nodeID < 0):
                tmp =  {"id": nodeID, "lat": i[1], "lon": i[0], "tags": { "source": "IJSN" } }
                if tmp not in newNodes:
                    newNodes.append( tmp )
            myNodes.append(nodeID)
        tags = []
        newWayID = ( (len(newNodes) + len(newWays) + 1) * -1)
        if (Sway['properties']['highway'] != None): tags.append(["highway", Sway['properties']['highway']])
        if (Sway['properties']['surface'] != None): tags.append(["surface", Sway['properties']['surface']])
        if (Sway['properties']['name'] != None): tags.append(["name", Sway['properties']['name']])
        if (Sway['properties']['alt_name'] != None): tags.append(["alt_name", Sway['properties']['alt_name']])
        if (Sway['properties']['ref'] != None): tags.append(["ref", Sway['properties']['ref']])
        if (Sway['properties']['noname'] != None): tags.append(["noname", Sway['properties']['noname']])
        if (Sway['properties']['layer'] != None): tags.append(["layer", Sway['properties']['layer']])
        if (Sway['properties']['lanes'] != None): tags.append(["lanes", Sway['properties']['lanes']])
        if (Sway['properties']['bridge'] != None): tags.append(["bridge", Sway['properties']['bridge']])
        if (Sway['properties']['junction'] != None): tags.append(["junction", Sway['properties']['junction']])
        tags.append(["source", "IJSN"])
        newWays.append( {"id": newWayID, "nodes": myNodes, "tags": tags } )

print ("New ways created: " + str(len(newWays)) + " with " + str(len(newNodes)) + " new nodes")
print ("Ways with modified properties: " + str(len(modifiedWays)))
print ("Individual error messages for manual control: " + str(len(manualCheck)))

if len(newNodes) > 0:
    for i in newNodes:
        createXML = createXML + u'    <node id="'+unicode(i['id'])+u'" timestamp="0000-00-00T00:00:00.0Z" lat="'+unicode(i['lat'])+u'" lon="'+unicode(i['lon'])+u'" changeset="-1" version="0" visible="true" uid="0" user="0">\n'
        for j in i['tags']:
            createXML = createXML + u'      <tag k="'+unicode(j)+u'" v="'+unicode(i['tags'][j])+u'" />\n'
        createXML = createXML + u'    </node>\n'

if len(newWays) > 0:
    for i in newWays:
        createXML = createXML + u'    <way id="'+unicode(i['id'])+u'" timestamp="0000-00-00T00:00:00.0Z" changeset="-1" version="0" visible="true" uid="0" user="0" >\n'
        for j in i['nodes']:
            createXML = createXML + u'      <nd ref="'+unicode(j)+u'" />\n'
        for k in i['tags']:
            createXML = createXML + u'      <tag k="'+unicode(k[0])+u'" v="'+unicode(k[1])+u'" />\n'
        createXML = createXML + u'    </way>\n'

if len(modifiedWays) > 0:
    for i in modifiedWays:
        modifyXML = modifyXML + u'    <way id="'+unicode(i['id'])+u'" timestamp="'+i['timestamp']+u'" changeset="'+unicode(i['changeset'])+u'" version="'+unicode(i['version'])+u'" visible="true" uid="'+unicode(i['uid'])+u'" user="'+unicode(i['user'])+u'" >\n'
        for j in i['nodes']:
            modifyXML = modifyXML + u'      <nd ref="'+unicode(j)+u'" />\n'
        for k in i['tags']:
            modifyXML = modifyXML + u"      <tag k='"+unicode(k)+u"' v='"+unicode(i['tags'][k])+u"' />\n"
        modifyXML = modifyXML + u'    </way>\n'

## Create and Modify
#osmChange = u'<?xml version="1.0" encoding="UTF-8"?>\n<osmChange version="0.6" generator="IJSN importer" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n  <create>\n' + unicode(createXML) + u'  </create>\n  <modify>\n' + unicode(modifyXML) + u'  </modify>\n</osmChange>'
## Create only
#osmChange = u'<?xml version="1.0" encoding="UTF-8"?>\n<osmChange version="0.6" generator="IJSN importer" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n  <create>\n' + unicode(createXML) + u'  </create>\n  <modify>\n  </modify>\n</osmChange>'
## Modify only
osmChange = u'<?xml version="1.0" encoding="UTF-8"?>\n<osmChange version="0.6" generator="IJSN importer" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n  <create> </create>\n  <modify>\n' + unicode(modifyXML) + u'  </modify>\n</osmChange>'

area = shapeFull['features'][0]['properties']['municipio']

#print osmChange

filename = "../shp/osmC/"+area+".osc"
f = open(filename, 'wb')
f.write(osmChange.encode('utf8'))
f.close()

filename = "../shp/flare/"+area+".json"
f = open(filename, 'wb')
f.write(json.dumps( manualCheck , indent=3))
f.close()
