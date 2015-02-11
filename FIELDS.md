Arruamento.shp
=========

This document contains Shapefile fields, values, and how to interpret them

CEP
=====

All values are 0.0000000000, if they had contained useful information this would have been `addr:postcode` - ignore

nome
=======

Names of the roads, `NULL` is to be substituted with `noname=yes`. `Caminho`, `R. Projetada` and `R. Projetada #` is treated as `NULL`, other values are processed to unabreviate the name. `R.`=`Rua`, `Av.`=`Avenida`, `Ac.`=`Acesso`, `Rod.`=`Rodovia`, `Al.`=`Alameda`, `Cam.`=`Caminho`, `Esc`=`Escadaria`, `Est`=`Estrada`, `Pç.`=`Praça`, `Rmp.`=`Rampa`, `Tr.`=`Travessa`, `Srv.`=`Servidão`, `Vdo.`=`Viaduto`, `Bc.`=`Beco`, `Ld.`=`Ladeira`, `Lad.`=`Ladeira`, `Largo.`=`Largo`, `Pte.`=`Ponte`, `Rot`=`Rotatória`

revestimen
=======

This is the `surface` tag, and it have two values, `Não Pavimentada`=`unpaved` and `Pavimentada`=`paved`


tipoArruam
=======

The following values: `Acesso`, `Alameda`, `Avenida`, `Beco`, `Caminho`, `Ciclovia`, `Contorno`, `Escadaria`, `Estrada`, `Ladeira`, `Largo`, `Passagem`, `Ponte`, `Praça`, `Rampa`, `Retorno`, `Rodovia`, `Rotatória`, `Rua`, `Servidão`, `Travessa`, `Trevo`, `Trilha`, `Via`, `Viaduto`

`Escadaria` should be tagged `highway=steps`

`Ponte` should have aditional tag `bridge=yes` + `layer=1`

`Servidão` should be tagged `highway=service`

`Rotatória` should be tagged `junction=roundabout` and form a closed circle

`Caminho` and `Trilha` should be tagged `highway=track` + `tracktype=1`

`Ciclovia` should be tagged `highway=cycleway`

`Rodovia` should be tagged as `highway=tertiary`, `highway=secondary`, `highway=primary`, `highway=trunk` or `highway=motorway`

`Acesso` and `Rampa` should be tagged as `_link` of the category of the way with highest class connected to it

`Viaduto` should be tagged `bridge=viaduct` + `layer=1`

If `Praça` forms a closed area, the tag `area=yes` should be added. These objects should be listed in a separate log file so they can be controlled to see if a `multipoligon` should be created (i.e. a garden in the middle of the square or similar).

`Beco` should in most cases be `highway=pedestrian`, but might also be `highway=service` + `service=alley`

`Via`, `Estrada` and `Rua` outside populated areas, not previously mapped should be `highway=unclassified`

All other roads not previously mapped should be `highway=residential`

extenM
=======

This is the length of the line in meters with 11 decimal precission. - ignore

situacFisi
========

Physical situation, `NULL` or `Projetada`. If value is `Projetada`, than tag as `highway=proposed`

nrFaixas
=======

Integer value between 1 and 6 for number of `lanes`, be ware that it seems like it counts lanes in both directions on duplicated roads, even when being marked with separate tracks.

trafego
=======

Unknown, all have value `NULL` - ignore

geocodMun
=======

This is a numeric municipal geocode. - ignore

municipio
========

Name of municipality where the road are located - kept during import in order to sort and split data logically according to municipality borders

microEstad
=======

Microregion of the municipality - ignore

macroEstad
=======

Macroregion of the municipality - ignore

data
======

Month and Year of data - ignore

anoReferen
======

Year of data - ignore

origem
======

Two values, `NULL` and `Restituição` - ignore

fonte
======

`CGEO/IJSN`, all ways created by this import should have `source=IJSN`, for ways edited I suggest we dont change the `source` tag.

