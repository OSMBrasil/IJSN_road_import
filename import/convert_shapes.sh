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


unzip ../shp/Arruamento.zip -d ../shp/streets
#unzip Trecho_Rodoviario.zip -d highways

# convert to WGS84, selecting fields and streets with name value
ogr2ogr -select 'nome, revestimen, nrFaixas, municipio' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'nome is not null' \
    -f 'ESRI Shapefile' ../shp/streets/streets.shp \
    ../shp/streets/Arruamento.shp

# convert to WGS84, selecting fields and streets with no name value
ogr2ogr -select 'nome, revestimen, nrFaixas, municipio' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'nome is null' \
    -f 'ESRI Shapefile' ../shp/streets/streets-no-name.shp \
    ../shp/streets/Arruamento.shp

rm ../shp/streets/Arruamento.*
