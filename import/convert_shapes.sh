#!/bin/sh
# This script converts a shapefile to WGS84, selecting fields and streets

# Copyright (C) 2015  Wille Marcel <wille@wille.blog.br>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


unzip -o ../shp/Arruamento.zip -d ../shp/streets
unzip -o ../shp/Trecho_Rodoviario.zip -d ../shp/highways

python3.5 shapefile_process.py

# convert to WGS84, selecting fields and streets with name value
ogr2ogr -select 'name, alt_name, ref, surface, lanes, municipio, highway, layer, bridge, junction, noname' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'name is not null' -overwrite \
    -f 'ESRI Shapefile' ../shp/streets/streets.shp \
    ../shp/streets/Arruamento.shp

# convert to WGS84, selecting fields and streets with no name value
ogr2ogr -select 'name, alt_name, ref, surface, lanes, municipio, highway, layer, bridge, junction, noname' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'name is null' -overwrite \
    -f 'ESRI Shapefile' ../shp/streets/streets-no-name.shp \
    ../shp/streets/Arruamento.shp

# convert to WGS84, selecting fields and streets with name value
ogr2ogr -select 'name, alt_name, ref, surface, lanes, municipio, highway, layer, bridge, junction, noname' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'name is not null' -overwrite \
    -f 'ESRI Shapefile' ../shp/highways/highways.shp \
    ../shp/highways/Trecho_Rodoviario_ES.shp

# convert to WGS84, selecting fields and streets with no name value
ogr2ogr -select 'name, alt_name, ref, surface, lanes, municipio, highway, layer, bridge, junction, noname' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'name is null' -overwrite \
    -f 'ESRI Shapefile' ../shp/highways/highways-no-name.shp \
    ../shp/highways/Trecho_Rodoviario_ES.shp

# merging
ogr2ogr -overwrite -f 'ESRI Shapefile' ../shp/Total_highways.shp ../shp/streets/streets.shp
ogr2ogr -f 'ESRI Shapefile' -update -append ../shp/Total_highways.shp ../shp/streets/streets-no-name.shp -nln Total_highways
ogr2ogr -f 'ESRI Shapefile' -update -append ../shp/Total_highways.shp ../shp/highways/highways.shp -nln Total_highways
ogr2ogr -f 'ESRI Shapefile' -update -append ../shp/Total_highways.shp ../shp/highways/highways-no-name.shp -nln Total_highways

rm ../shp/streets/Arruamento.*
rm ../shp/highways/Trecho_Rodoviario_ES.*