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

import ogr

__version__ = "$Revision: 1 $"

driver = ogr.GetDriverByName('ESRI Shapefile')

file = "../shp/streets/Arruamento.shp"

dataSource = driver.Open(file, 1)

layer = dataSource.GetLayer()
layerdef = layer.GetLayerDefn()
new_field = ogr.FieldDefn("name", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("alt_name", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("ref", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("lanes", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("surface", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("highway", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("bridge", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("junction", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("layer", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("noname", ogr.OFTString)
layer.CreateField(new_field)
feature = layer.GetNextFeature()

while feature:
    name = feature.GetField("nome")
    if (name != None):
        if (name.find(" Projetada") > 0):
            name = None
    if (name == None):
        feature.SetField("noname", "yes")
    if (name != None):
        name = name.replace("N.S.", "Nossa Senhora")
        name = name.replace("N.s.", "Nossa Senhora")
        name = name.replace("Ns ", "Nossa Senhora ")
        name = name.replace("Eng.", "Engineiro")
        name = name.replace("Pres.", "Presidente")
        name = name.replace("Dr.", "Doutor")
        name = name.replace("Cel.", "Coronel")
        name = name.replace("Cap.", "Capitão")
        name = name.replace("Prof.", "Professor")
        name = name.replace("Ver.", "Vereador")
        name = name.replace("Mal.", "Marechal")
        name = name.replace("Gov.", "Governador")
        name = name.replace("R.", "Rua")
        name = name.replace("Av.", "Avenida")
        name = name.replace("Ac.", "Acesso")
        name = name.replace("Rod.", "Rodovia")
        name = name.replace("Al.", "Alameda")
        name = name.replace("Cam.", "Caminho")
        name = name.replace("Esc.", "Escadaria")
        name = name.replace("Est.", "Estrada")
        name = name.replace("Estr.", "Estrada")
        name = name.replace("Pç.", "Praça")
        name = name.replace("Rmp.", "Rampa")
        name = name.replace("Tr.", "Travessa")
        name = name.replace("Tv.", "Travessa")
        name = name.replace("Srv.", "Servidão")
        name = name.replace("Vdo.", "Viaduto")
        name = name.replace("Bc.", "Beco")
        name = name.replace("Ld.", "Ladeira")
        name = name.replace("Lad.", "Ladeira")
        name = name.replace("Largo.", "Largo")
        name = name.replace("Pte.", "Ponte")
        name = name.replace("Rot.", "Rotatória")
        name = name.replace("Trv.", "Trevo")
        feature.SetField("name", name)
    surface = feature.GetField("revestimen")
    if (surface == "Pavimentada"):
        feature.SetField("surface", "paved")
    else:
        feature.SetField("surface", "unpaved")
    feature.SetField("lanes", feature.GetField("nrFaixas"))
    wayT = feature.GetField("tipoArruam")
    feature.SetField("highway", "residential")
    if (wayT == "Escadaria"): feature.SetField("highway", "steps")
    if (wayT == "Rodovia"): feature.SetField("highway", "tertiary")
    if (wayT == "Servidão"): feature.SetField("highway", "service")
    if (wayT == "Rotatória"): feature.SetField("junction", "roundabout")
    if (wayT == "Caminho"): feature.SetField("highway", "track")
    if (wayT == "Trilha"): feature.SetField("highway", "path")
    if (wayT == "Ciclovia"): feature.SetField("highway", "cycleway")
    if (wayT == "Acesso"): feature.SetField("highway", "primary_link")
    if (wayT == "Rampa"): feature.SetField("highway", "primary_link")
    if (wayT == "Viaduto"):
        feature.SetField("bridge", "viaduct")
        feature.SetField("layer", "1")
    if (wayT == "Ponte"):
        feature.SetField("bridge", "yes")
        feature.SetField("layer", "1")
    if (wayT == "Beco"): feature.SetField("highway", "pedestrian")
    if (wayT == "Via"): feature.SetField("highway", "unclassified")
    if (wayT == "Estrada"): feature.SetField("highway", "unclassified")
    if (wayT == "Trevo"):
        feature.SetField("highway", "tertiary")
        feature.SetField("junction", "yes")
    if (feature.GetField("situacFisi") == "Projetada"): feature.SetField("highway", "proposed")
    municipio = feature.GetField("municipio")
    if (municipio != None):
        municipio = municipio.replace(' ', '')
        feature.SetField("municipio", municipio)
    layer.SetFeature(feature)
    feature = layer.GetNextFeature()

dataSource.Destroy()

file = "../shp/highways/Trecho_Rodoviario_ES.shp"

dataSource = driver.Open(file, 1)

layer = dataSource.GetLayer()
layerdef = layer.GetLayerDefn()
new_field = ogr.FieldDefn("name", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("alt_name", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("ref", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("lanes", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("surface", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("highway", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("bridge", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("junction", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("layer", ogr.OFTString)
layer.CreateField(new_field)
new_field = ogr.FieldDefn("noname", ogr.OFTString)
layer.CreateField(new_field)
feature = layer.GetNextFeature()

while feature:
    feature.SetField("highway", "primary")
    if (feature.GetField("tipoTrech") == "Caminhos do Campo"): feature.SetField("highway", "track")
    ref = ""
    name = feature.GetField("nome")
    if (name != None): name = name.replace("BR- ", "BR-")
    if (name == "Estrada Municipal"): name = None
    if (name != None):
        if (name.find(" Projetada") > 0):
            name = None
    if (name != None):
        if (name.find("BR-") > -1):
            ref = ref + " " + name
            name = None
    if (name != None):
        if (name.find("ES-") > -1):
            ref = ref + " " + name
            name = None
    altName = feature.GetField("nomePop")
    if (altName != None): altName = altName.replace("BR- ", "BR-")
    if (altName == "Estrada Municipal"): altName = None
    if (altName != None):
        if (len(altName) < 3):
            ref = ref + " " + altName
            altName = None
    if (altName != None):
        if (altName.find("BR-") > -1):
            ref = ref + " " + altName
            altName = None
    if (altName != None):
        if (altName.find("ES-") > -1):
            ref = ref + " " + altName
            altName = None
    ref = ref.replace("/", " - ")
    ref = ref.replace(" - ", "-")
    ref = ref.replace("-ES", "- ES")
    myRefs = ref.split()
    ref = ""
    junk = []
    newRef = []
    for i in range(len(myRefs)):
        if (len(myRefs[i])> 6): junk.append(myRefs[i])
        elif (myRefs[i].find("BR") == -1):
            if (myRefs[i].find("ES") == -1): junk.append(myRefs[i])
            else: newRef.append(myRefs[i])
        else: newRef.append(myRefs[i])
    newRef = list(set(newRef))
    newRef.sort()
    junkCombined = ""
    if (len(newRef) > 0): ref = ';'.join(newRef)
    if (len(junk) > 0):
        junkCombined = str(" ".join(junk))
        junkCombined = junkCombined.replace("-", " - ")
        if (altName != None):
            altName = altName + ";" + junkCombined
        else: altName = junkCombined
    if (name != None):
        name = name.replace("Rod.", "Rodovia")
        name = name.replace("Faz.", "Fazenda")
        name = name.replace("Estr.", "Estrada")
        name = name.replace("Faz ", "Fazenda ")
        name = name.replace("Com ", "Comunidade ")
        name = name.replace("Comun.", "Comunidade")
        name = name.replace("Laborat.", "Laboratorio")
        name = name.replace("S.", "São")
        feature.SetField("name", name)
    if (altName != None):
        altName = altName.replace("Rod.", "Rodovia")
        altName = altName.replace("Faz.", "Fazenda")
        altName = altName.replace("Estr.", "Estrada")
        altName = altName.replace("Faz ", "Fazenda ")
        altName = altName.replace("Com ", "Comunidade ")
        altName = altName.replace("Comun.", "Comunidade")
        altName = altName.replace("Laborat.", "Laboratorio")
        altName = altName.replace("S.", "São")
        if (name == None):
            feature.SetField("name", altName)
            altName = None
        else: feature.SetField("alt_name", altName)
    if (len(ref) > 0): feature.SetField("ref", ref)
    feature.SetField("lanes", feature.GetField("nrFaixas"))
    surface = feature.GetField("revestim")
    if (surface == "Pavimentada"):
        feature.SetField("surface", "paved")
    else:
        feature.SetField("surface", "unpaved")
    if (feature.GetField("situacFisi") == "Planejada"): feature.SetField("highway", "proposed")
    if (feature.GetField("situacFisi") == "Em Construção"): feature.SetField("highway", "construction")
    layer.SetFeature(feature)
    feature = layer.GetNextFeature()

dataSource.Destroy()