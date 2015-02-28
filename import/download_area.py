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

# Dependency: overpass-api-python-wrapper: see https://github.com/mvexel/overpass-api-python-wrapper
import overpass
import sys
import json

api = overpass.API()

__version__ = "$Revision: 1 $"

area = "Unset"

if len(sys.argv) < 2:
    print("Usage: python download_area.py area")
    sys.exit()
else:
    area = sys.argv[1]


#print("You have entered: ", area)

# Building overpass query
searchString = 'relation["boundary"="administrative"]["admin_level"="8"]["name"="'+area+'"](-21.5,-42.0,-17.5,-39.0)'
city = api.Get(searchString)

# Now to get the relation ID from the output
cityID = 1828867 # tricky formula (relation for Divino de São Lourenço)
jsonString = json.dumps(city)
IDsource = json.loads(jsonString)
myElements = json.dumps(IDsource['elements'])
IDsource = json.loads(myElements)
myID = json.dumps(IDsource[0][u'id'])
cityID = int(myID)
cityID = cityID + 3600000000

api = overpass.API(timeout=600)
#api = overpass.API(responseformat=xml) # OSM XML output -- not supported in wrapper at the moment

searchString = '(way(area:'+str(cityID)+')["highway"]; >; ); out meta '
#print(searchString)
highways = api.Get(searchString)

filename = "../shp/osm/"+area+".json"
f = open(filename, 'w')
f.write(json.dumps(highways))
f.close()

