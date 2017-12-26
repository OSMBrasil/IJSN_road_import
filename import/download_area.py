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

# Dependency: overpass-api-python-wrapper: see https://github.com/mvexel/overpass-api-python-wrapper
import overpass
import sys
import json

api = overpass.API()
#api = overpass.API(responseformat="json")

__version__ = "$Revision: 1 $"

area = "Unset"

if len(sys.argv) < 2:
    print "Usage: python download_area.py area"
    sys.exit()
else:
    area = unicode(sys.argv[1].decode("utf-8"))

print u"You have entered: ", area

# Building overpass query
searchString = u'relation["boundary"="administrative"]["admin_level"="8"]["name"~"'+unicode(area).encode('ascii', 'replace').replace("?", ".")+u'"](-21.5,-42.0,-17.5,-39.0);out ids;'
city = api.Get(searchString, responseformat="json")
cityID = city['elements'][0]['id']
print("Relation ID for " + area + ": " + str(cityID))
cityID = int(cityID) + 3600000000

api = overpass.API(timeout=600)
print("Downloading data.")
#searchString = 'way["highway"](area:'+str(cityID)+');(._;>;);out meta;'
searchString = 'way["highway"]["name"](area:'+str(cityID)+');(._;>;);out meta;'
#searchString = 'way["highway"][!"name"](area:'+str(cityID)+');(._;>;);out meta;'
highways = api.Get(searchString, responseformat="json")

print("Saving data to file")
filename = u"../shp/osm/"+area+u".json"
f = open(filename, 'w')
f.write(json.dumps(highways))
f.close()
#print(filename + " saved")
