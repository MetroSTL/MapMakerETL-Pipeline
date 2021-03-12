# HERE to Trapeze MapMaker Tool

## Intro
The purpose of this script is to have a fully operational process that allows for the processing of HERE centerline data that can be used to upload data threw the Trapeze MapMaker product. After this tool is run the file will be stored in a Model Output GDB and will need to be converted to Shapefile in order to be uploaded.

The Tool is broken out into a couple of different toolsets:
1. Extract and Copy
2. MapMaker Conversion
3. Custom Edits
4. AVL Basemap

It is important to note that this model was specifically designed for the Metro St Louis transit agnecy and makes some assumptions in some of the field calculations surrounding the Place, State, and County calculations. If this model is to be used for another region these calculations should be altered to reflect the region. 

## .env File
In order for this to work there needs to be a `.env` file that contains the variables pertaining to your system:
- PROJECT_DIR - The directory that you want to store the processed files in
- HERE_DIR - Where you are storing the HERE files in (Do not alter the file locations or names)
- US_COUNTIES - The Location on the directory of a shapefile of all of the US Counties download from Tiger (*Could be converted to use Adminbndy3)

## Python Environment
In order for you to run this file you will need to have an ArcGIS Python Environment running to access the ArcPy Modules. Other than that you will need to install [python-dotenv](https://pypi.org/project/python-dotenv/) into the same Python Environment.

To activate: 

 `activate C:\Users\%USER%\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone3`

Install `python dotenv`:

`pip install python-dotenv`

To Run:

 `python run()` 


## Extract and Copy
The Extract and Copy script does exactly that. It is pointed at a directory that has all of the files that make up the HERE dataset and pulls the files that it needs clips them to the specified boundary and the deposits them to a GDB (`./%Project_Folder%/Model_Inputs.gdb`). There is also a `Model_Outputs.gdb` that is created in this process that will hold the eventual output of subsiquent Python scripts.

## MapMaker Conversion
The MapMaker Converion script is the main piece of Python Script a part of this model. This will be how the Streets and AltStreets (Alias') will be formated, filtered and merged together to form the majority of the file that makes up the shapefile to be uploaded through the MapMaker Tool. 



## Custom Edits
While it is important to make sure that all edits are pushed to the [HERE MapCreator Application](https://mapcreator.here.com/) there will inevitably be edits that are not accepted through the application and will need to be put in manually. The Custom Edits Tool is meant to find specific custom edits from the old file, isolate them into a new file and then merge them into the new streets file after the `MapMaker Conversion` process is done running.

## AVL Basemap
While the Basemap for Pass and FX is done in MapMaker there is another completely different process that is run to convert the files for the AVL system. This is the basemap that scheduling maintains. These file are MidMif files and have to be converted over via another script. **However, ArcGIS and arcpy do not have the capability to export MidMif files so a 3rd party library or tool has to be used in order to make this happen.** One of the options for this is to use [Qgis](https://qgis.org/en/site/forusers/download.html). While this tool is outside the perview of this script, you can open up a Shapefile in Qgis > Right Click on the layer > Save As > MidMif > Profit!!! 

## Important Considerations and Common Issues

### Projections / Coordinate Systems

Because Trapeze is not a GIS system the data must always be uploaded in WGS1984. If forwhatever reason this is not the case you may need to [delete projection files](https://gis.stackexchange.com/questions/180551/how-to-remove-projection-in-terminal-from-shp-file-with-valid-prj-available). If the coordinate system is incorrect you can always use ArcMap or ArcPro's [Project (Data Management) Tool](https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/project.htm).
