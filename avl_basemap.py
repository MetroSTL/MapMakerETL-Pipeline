import arcpy
from sys import argv
import os
import geopandas as gpd


def filterAndSeparate(Final_MM_Shapefile, Project_Folder):  # AVL Basemap Export

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    avl_gdb = os.path.join(Project_Folder, 'AVL.gdb')
    output_gdb = os.path.join(Project_Folder, 'Output_Folder.gdb')
    basemap = os.path.join(output_gdb, "AllStreets")

    arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model Inputs", out_version="CURRENT")

    # Filter and export interstates
    arcpy.conversion.FeatureClassToFeatureClass(in_features=basemap, out_path=avl_gdb, out_name=f"Interstates", where_clause="((M_CFCC LIKE 'A2%' Or M_CFCC LIKE 'A1%') AND M_SPEED > 25) AND (M_SEG_NAME NOT LIKE '%ON-RAMP%' OR M_SEG_NAME NOT LIKE '%OFF-RAMP%')",  config_keyword="")

    # Filter and export streets
    arcpy.conversion.FeatureClassToFeatureClass(in_features=basemap, out_path=avl_gdb, out_name=f"Streets", where_clause="(M_CFCC NOT LIKE 'A1%') AND (M_CFCC NOT LIKE 'A2%' And (M_SEG_NAME LIKE '%ON-RAMP%' OR M_SEG_NAME LIKE '%OFF-RAMP%')) OR ((M_CFCC LIKE 'A2%' OR M_CFCC LIKE 'A3%') And M_SPEED < 25) OR M_CFCC NOT LIKE 'H%' OR M_CFCC NOT LIKE 'B%' OR M_CFCC NOT LIKE 'A7%'", config_keyword="")

    # Filter and export major roads
    _Output_MajorRoads = arcpy.conversion.FeatureClassToFeatureClass(in_features=basemap, out_path=avl_gdb, out_name=f"MajorRoads", where_clause="(((M_CFCC LIKE 'A3%' OR M_CFCC LIKE 'A2%') And M_SPEED > 25) Or (M_CFCC LIKE 'A2%' AND M_SPEED > 25) And (M_SEG_NAME NOT LIKE '%ON-RAMP%' OR M_SEG_NAME NOT LIKE '%OFF-RAMP%'))",  config_keyword="")[0]
    # Further filter major roads
    _Output_MajorRoads_Layer,  = arcpy.management.SelectLayerByAttribute(in_layer_or_view=_Output_MajorRoads, selection_type="NEW_SELECTION", where_clause="M_SPEED < 25 Or M_SEG_NAME LIKE '%ON-RAMP%' Or M_SEG_NAME LIKE '%OFF-RAMP%' And M_SEG_NAME LIKE 'I-%'", invert_where_clause="")
    arcpy.management.DeleteRows(in_rows=_Output_MajorRoads_Layer)

def convertToMidMif(Project_Folder):
    avl_gdb = os.path.join(Project_Folder, 'AVL.gdb')

    # cycle through the files in the AVL GDB file and convert to MidMif Files
    for fc in arcpy.ListFeatureClasses(avl_gdb):
        # convert to geodataframe
        gdf = gpd.GeoDataFrame(fc)
        # export to MidMif file 
        gdf.to_file(f'{fc}.mif', driver='MapInfo File')