#!/bin/sh

unzip Arruamento.zip -d streets
#unzip Trecho_Rodoviario.zip -d highways

# convert to WGS84, selecting fields and streets with name value
ogr2ogr -select 'nome, revestimen, nrFaixas, municipio' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'nome is not null' \
    -f 'ESRI Shapefile' streets/streets.shp \
    streets/Arruamento.shp

# convert to WGS84, selecting fields and streets with no name value
ogr2ogr -select 'nome, revestimen, nrFaixas, municipio' \
    -a_srs EPSG:4326 -t_srs EPSG:4326 \
    -where 'nome is null' \
    -f 'ESRI Shapefile' streets/streets-no-name.shp \
    streets/Arruamento.shp

rm streets/Arruamento.*
