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

api = overpass.API()

print("Welcome to download_area.py")
print("This program is made to download all highways with accosiated nodes and relations within a defined area")

__version__ = "$Revision: 1 $"

area = "Unset"

if len(sys.argv) < 2:
    print("Usage: python download_area.py area")
    sys.exit()
else:
    area = sys.argv[1]


print("You have entered: ", area)

# Building overpass query
"""
    20:26 Skippern-MWS: tem duvida que highways = api.Get('way["highway"] in $area') vai dar certo
    20:27 wille: @skippern-mws tem um segredo: pega o id da relação do municipio que vc quer
    20:27 wille: e soma com 3600000000
    20:28 Skippern-MWS: entao pega nome do municipio do shapefile ou um lista, buscar o id do relacao, e entrar no query?
    20:28 wille: tipo brasília: eu uso esse comando
    """
#highways = api.Get('way["highway"] in $area')


