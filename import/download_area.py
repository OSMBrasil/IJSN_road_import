#! /usr/bin/python3
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

# Dependency: overpass-api-python-wrapper: see https://github.com/mvexel/overpass-api-python-wrapper
import overpass
import overpy
import sys
import json

api = overpass.API()
#api = overpass.API(responseformat="json")
#api = overpass.API(responseformat="geojson")
#api = overpy.Overpass()

__version__ = "$Revision: 1 $"

area = "Unset"

if len(sys.argv) < 2:
    print("Usage: python download_area.py area")
    sys.exit()
else:
    area = sys.argv[1]


#print("You have entered: ", area)

# Building overpass query
searchString = '[out:json];relation["boundary"="administrative"]["admin_level"="8"]["name"="'+area+'"](-21.5,-42.0,-17.5,-39.0);'
#searchString = 'relation["boundary"="administrative"]["admin_level"="8"]["name"="'+area+'"](-21.5,-42.0,-17.5,-39.0);'
#print("Search String: " + searchString)
city = api.Get(searchString)
#result = api.query(searchString)
#print(len(result.relations))
#relation = result.relations[0]
#print(relation)
#print("city: " + city)

# Now to get the relation ID from the output
cityID = 1828867 # tricky formula (relation for Divino de São Lourenço)
#jsonString = json.dumps(city)
#print(jsonString)
#IDsource = json.loads(jsonString)
#print("IDsource: " + IDsource)
#myElements = json.dumps(IDsource['elements'])
#myElements = json.dumps(city[0])
#print("myElements: " + myElements)
#IDsource = json.loads(myElements)
#myID = json.dumps(IDsource[0][u'id'])
#tmp = json.dumps(city[0])
#myID = json.dumps(tmp)
myElements = json.loads(city)['elements']
#print(myElements)
myElements = json.dumps(myElements)
#print(myElements)
myID = json.loads(myElements)[0]['id']
#print(str(myID))
#myID = city[0]['elements']['id']
print("Relation ID for " + area + ": " + str(myID))
#cityID = int(myID)
cityID = cityID + 3600000000

api = overpass.API(timeout=600)
print("Downloading data")
searchString = '[out:json];(way(area:'+str(cityID)+')["highway"]; >; ); out meta '
#print("Search String" + searchString)
highways = api.Get(searchString)

print("Saving data to file")
filename = "../shp/osm/"+area+".json"
f = open(filename, 'w')
f.write(json.dumps(highways))
f.close()
print(filename + " saved")
