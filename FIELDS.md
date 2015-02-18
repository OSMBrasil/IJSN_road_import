This document contains Shapefile fields, values, and how to interpret them

Arruamento.shp
=========

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

`CGEO/IJSN`, all ways created by this import should have `source=IJSN`, for ways edited I suggest we dont change the `source` tag. All changesets should have the tag `source=IJSN`.

Trecho_Rodoviario_ES.shp
=======

nome
======

`NULL` should be tagged with `noname=yes`

`BR-nnn` where `nnn` is a 3 digit number, or `ES-nnn`, or several of these values separated by **/**, these values should be added to `ref` tag, separated by **;**

`Estrada Municipal` shold be treated as `NULL`

Names starting with `Rod.` should be changed to `Rodoviario` followed by the name: `Rodoviario Audifax Barcelos Neves`

nomePop
======

This name can be added to `alt_name`, but only if it is not equal to `ref` or `name`. Need special attention to names such as `BR-101 (Norte)`

sigla
======

With values `BR` for Federal roads, `ES` for state roads, and `MUN` for municipal roads, there are also a value `ES/BR` for coincided fedral/state roads

jurisdicao
=====

This is the key for financial/legal jurisdiction of the highway, with values `Federal`, `Estadual`, `Estadual/Federal` and `Municipal`, mostly same as `sigla`, but a few deviations

tipoTrech
======

`Caminhos do Campo`, `Rodoviario`, the first to be tagged `highway=track` + `tracktype=grade1`, the other should be either `highway=tertiary`, `highway=secundary`, `highway=primary`, `highway=trunk` or `highway=motorway`

revestim
======

This is the `surface` tag, and it have two values, `Não Pavimentada`=`unpaved` and `Pavimentada`=`paved`

situacFisi
======

`NULL` - ignore

`Ampliação do Projeto a Contratar` - ?

`Construída` - Constructed?

`Em Construção` - Under construction `highway=contruction`

`Em Obras` - Work going on (renovation?)

`Obra Paralizada` - Work stoped (but not completed?)

`Planejada` - Planned `highway=proposed`

`Projeto Elaboração - Ampliação` - Now, what is this?

administra
======

Unknown, all have value `NULL` - ignore

concession
======

Unknown, all have value `NULL` - ignore

operacion
=====

Unknown, all have value `NULL` - ignore

nrFaixas
=======

Integer value between 2 and 6 for number of `lanes`, be ware that it seems like it counts lanes in both directions on duplicated roads, even when being marked with separate tracks.

trafego
======

Unknown, all have value `NULL` - ignore

geocodigo
======

This is a numeric municipal geocode. - ignore

municipio
=======

Name of municipality where the road are located - kept during import in order to sort and split data logically according to municipality borders

macroEstad
======

Macroregion of the municipality - ignore

microEstad
=======

Microregion of the municipality - ignore

extencaoKm
=======

This is the length of the line in kilometers with 8 decimal precission. - ignore

origem
======

Unknown, all have value `NULL` - ignore

data
======

Source date, all is `03/08/2012`, already traced data from `DER-ES` is of newer date.

fonte
=====

`IJSN/DER-ES`, all ways created by this import should have `source=IJSN`, for ways edited I suggest we dont change the `source` tag. All changesets should have the tag `source=IJSN`.
