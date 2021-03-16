import arcpy
from sys import argv
import os



# This function will run and Clip the full files that exist within the HERE_Data folder 
# (folder with all of the shapefiles that make up the Here dataset and output them to the output gdb)

# Project_Folder = Where things will end up
# HERE_DATA = Where the HERE data lives (directory)
# us_counties = US Census data file that has all of the counties in the united states --> https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip



def extract(Project_Folder, HERE_Data):  # 01-Extract and Copy

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = HERE_Data
    
    Model_Inputs_gdb = arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model_Inputs", out_version="CURRENT")[0]

    Model_Outputs_gdb = arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model_Outputs", out_version="CURRENT")[0]

    us_counties = os.path.join(HERE_Data, 'Adminbndy3.shp')

    fields = arcpy.ListFields(us_counties)

    region = arcpy.FeatureClassToFeatureClass_conversion(us_counties, Model_Inputs_gdb, "Region", where_clause="POLYGON_NM in ('ST CLAIR', 'ST LOUIS', 'ST LOUIS (CITY)')")[0]

    Streets = os.path.join(Model_Inputs_gdb, fr"Streets")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Streets.shp'), clip_features=region, out_feature_class=Streets, cluster_tolerance="")
    print('Streets Exported')

    AltStreets = os.path.join(Model_Inputs_gdb, fr"AltStreets")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'AltStreets.shp'), clip_features=region, out_feature_class=AltStreets, cluster_tolerance="")
    print('AltStreets Exported')
 
    Zlevels = os.path.join(Model_Inputs_gdb, fr"Zlevels")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Zlevels.shp'), clip_features=region, out_feature_class=Zlevels, cluster_tolerance="")
    print('ZLevels Exported')

    Adminbndy4 = os.path.join(Model_Inputs_gdb, fr"Adminbndy4")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Adminbndy4.shp'), clip_features=region, out_feature_class=Adminbndy4, cluster_tolerance="")
    print('Adminbndy4 Exported')

    NamedPlc = os.path.join(Model_Inputs_gdb, fr"NamedPlc")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'NamedPlc.shp'), clip_features=region, out_feature_class=NamedPlc, cluster_tolerance="")
    print('NamedPlc Exported')

    Adminbndy3 = os.path.join(Model_Inputs_gdb, fr"Adminbndy3")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Adminbndy3.shp'), clip_features=region, out_feature_class=Adminbndy3, cluster_tolerance="")
    print('Adminbndy3 Exported')

    return os.path.join(Project_Folder, Model_Inputs_gdb)

