#!/bin/sh

#  execute.sh
#  IJSN_road_import
#
#  Created by Aun Johnsen on 2/22/2015.
#

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

# Make municipality list, run the list in loop.
# For each municipality, do:
# 1) Select only municipality from each shapefile into temporary shapes
# 2) Correct field names and values
# 3) Convert to a format for processing
# 4) Download area with download_area.py
# 5) Compare data with existing data, analyze and create diff files
# 6) Health check diff files
# 7) Upload diff files
# 8) Done
./convert_shapes.sh

for i in "Afonso Cláudio" "Alegre" "Alfredo Chaves" "Alto Rio Novo" "Anchieta" "Apiacá" "Aracruz" "Atílio Vivácqua" "Água Doce do Norte" "Águia Branca" "Baixo Guandu" "Barra de São Francisco" "Boa Esperança" "Bom Jesus do Norte" "Brejetuba" "Cachoeiro de Itapemirim" "Cariacica" "Castelo" "Colatina" "Conceição da Barra" "Conceição do Castelo" "Divino de São Lourenço" "Domingos Martins" "Dores do Rio Preto" "Ecoporanga" "Fundão" "Governador Lindenberg" "Guaçuí" "Guarapari" "Ibatiba" "Ibiraçu" "Ibitirama" "Iconha" "Irupi" "Itaguaçu" "Itapemirim" "Itarana" "Iúna" "Jaguaré" "Jerônimo Monteiro" "João Neiva" "Laranja da Terra" "Linhares" "Mantenópolis" "Marataízes" "Marechal Floriano" "Marilândia" "Mimoso do Sul" "Montanha" "Mucurici" "Muniz Freire" "Muqui" "Nova Venécia" "Pancas" "Pedro Canário" "Pinheiros" "Piúma" "Ponto Belo" "Presidente Kennedy" "Rio Bananal" "Rio Novo do Sul" "Santa Leopoldina" "Santa Maria de Jetibá" "Santa Teresa" "São Domingos do Norte" "São Gabriel da Palha" "São José do Calçado" "São Mateus" "São Roque do Canaã" "Serra" "Sooretama" "Vargem Alta" "Venda Nova do Imigrante" "Viana" "Vila Pavão" "Vila Valério" "Vila Velha" "Vitória";
    do echo "=== $i ==="
    date
    k=`echo $i|sed 's/ //g'`
    ogr2ogr -overwrite -select 'name, alt_name, ref, surface, lanes, municipio, highway, layer, bridge, junction, noname' -where "municipio like \"$k\"" ../shp/shape/$k.shp  ../shp/Total_highways.shp Total_highways 2>/dev/null
#    ogr2ogr -overwrite -select 'name, alt_name, ref, surface, lanes, municipio, highway, layer, bridge, junction, noname' -where "municipio like \"$k\"" -f 'ESRI Shapefile' ../shp/shape/$k.shp  ../shp/Total_highways.shp
#    ogr2ogr -overwrite -where "municipio like \"$k\"" -f 'ESRI Shapefile' ../shp/shape/$k.shp  ../shp/Total_highways.shp
    mv "../shp/json/$i.json" "../shp/json/$i.json~" 2>/dev/null
#    ogr2ogr -overwrite -f "GeoJSON" "../shp/json/$i.json" "../shp/shape/$k.shp" "$k"
    ogr2ogr -overwrite -f "GeoJSON" "../shp/json/$i.json" "../shp/shape/$k.shp" "$k" 2>/dev/null
    cp "../shp/osm/$i.json" "../shp/osm/$i.json~" 2>/dev/null
    ./download_area.py "$i"
    cp "../shp/flare/$k.json" "../shp/osm/$k.json~" 2>/dev/null
    cp "../shp/osmC/$k.xml" "../shp/osmC/$k.xml~" 2>/dev/null
    cp "../shp/osmC/$k.osc" "../shp/osmC/$k.osc~" 2>/dev/null
    ./compare_map.py "../shp/json/$i.json" "../shp/osm/$i.json"
#    exit 0
done
