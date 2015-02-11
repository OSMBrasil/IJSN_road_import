IJSN Road Import
=============

The purpose of this project is to work with the two supplied shapefiles in order to extract the useful information and add to the OpenStreetMap database. This import is complicated as most of the affected roads already exist in the database, and many of them already are named, maybe with different spelling of the same name, or with different extension of the name. There might also be some conflicts in surface, but occational conflict might also appear on lanes.

What is to import?
==============

From the highway file, only `name` if it is not something with reference to the `ref` tag, if a `name` tag exist than no value will be imported, and fill in missing `surface`, which should affect only a few minor trenches. `lanes` should also be added.

From the urban file things are much more complicated. Here it is needed to check names in a much more complicated way. First the data in the shapefile must be extended so that the `name` values starting with *R.* are exchanged with *Rua* and *Av.* with *Avenida*. Next step will be to compare the names with the ones existing in OSM, if there is a difference in the spelling or in the name we need to establish rules how to handle the cases. The tags `surface` and `lanes` are treated the same way as for highways, just that there will be more of it.

Projection
=============

The Shapefiles presented are as downloaded from [IJSN website](http://www.ijsn.es.gov.br/Sitio/index.php?option=com_content&view=article&id=3780&Itemid=330). They are presented in [SIRGAS 2000](http://georepository.com/crs_4674/SIRGAS-2000.html) projection, which is close to, but not exactly the same as [WGS84](http://georepository.com/crs_4979/WGS-84.html). Shapes should be converted to WGS84 before final product and upload.

Requirements
==============

Scripts must be of syntax and languages that can be safely executed from `Mac OS X 10.10` without unexpected results. Additional software can be installed for correct interpretation of the scripts. This project will not prioritize any language or script over others. Known to execute on the system are `shell`, `perl`, `python` and `ruby`, though other options might also be available.

Issues
==============

All issues identified during preparations of import is to be addressed in this repositorys issue tracking system, and will be addressed accordingly

Pre-processing
========

All scripts must be thuroughly tested, either with no upload, or with upload to sandbox, before the import is to take place. No upload should be done to the live server before all issues have been satisfactory sorted out.

Processing scripts
=========

Processing scripts should deal with limited areas but complete data as much as possible from both shape files. For the smaller municipalities, entire municipality could be a single changeset, while the larger municipalities and the metropolitan areas must be devided even further. One idea might be to make a grid, and process each square as different changefile.

Uploading of data
=========

Once a section are processed, the data should be uploaded without delay, this to ensure no conflicts during the upload. Since this is data that is likely to be edited by other users. We want the time from downloading data for processing to uploading processed data to be as short as possible for this reason.

The upload script should also specifically tag the changesets with `source=IJSN` + `created_by=IJSN Road Import Script/1` + `comment=IJSN Mechanical Import: square <number>, see <link to topic on imports mailing list>`