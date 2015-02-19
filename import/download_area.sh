#!/bin/sh

#  download_area.sh
#
# This script downloads all highways with belonging relations within
# one municipality.
#
#  Created by Aun Johnsen on 2/19/2015.
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

#  Arguments
# <area> - area for name search in Overpass

if [ "$1" == "" ]; then
    echo "Usage: ./downloade_area.sh <area>"
    exit 1
fi

# Assuming $1 contains name of area, if area consists of multiple words, use quotes on
# command line
city=$1

echo "Downloading roads, streets and highways in $city"

