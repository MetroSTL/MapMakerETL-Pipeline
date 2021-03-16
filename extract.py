import arcpy
from sys import argv
import os



# This function will run and Clip the full files that exist within the HERE_Data folder 
# (folder with all of the shapefiles that make up the Here dataset and output them to the output gdb)

# Project_Folder = Where things will end up
# HERE_DATA = Where the HERE data lives (directory)
# us_counties = US Census data file that has all of the counties in the united states --> https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip


# this function takes in the project folder env variable and here data directory env variable and clips out the data that you need for the region
# this clipped data is then put into the project folder in the model_inputs.gdb and used for subsquent processing. to update the bounds us the region
# variable's where clause to define the bounds by the county information in the AdminBndry3 file. In this function the names of the three counties are used
# to isolate the area by using, "POLYGON_NM in ('ST CLAIR', 'ST LOUIS', 'ST LOUIS (CITY)')"
def extract(Project_Folder, HERE_Data):  # 01-Extract and Copy

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = HERE_Data
    
    # create the Input and Output gdb's in the project_folder
    Model_Inputs_gdb = arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model_Inputs", out_version="CURRENT")[0]
    Model_Outputs_gdb = arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model_Outputs", out_version="CURRENT")[0]

    # location of the counties file
    Adminbndy3 = os.path.join(HERE_Data, 'Adminbndy3.shp')

    # define the region and export using the AdminBdry3 file and where_clause to reference data in that table
    region = arcpy.FeatureClassToFeatureClass_conversion(Adminbndy3, Model_Inputs_gdb, "Region", where_clause="POLYGON_NM in ('ST CLAIR', 'ST LOUIS', 'ST LOUIS (CITY)')")[0]

    # Clip the streets file usin region and export to Model_Inputs.gdb
    Streets = os.path.join(Model_Inputs_gdb, fr"Streets")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Streets.shp'), clip_features=region, out_feature_class=Streets, cluster_tolerance="")
    print('Streets Exported')

    # Clip the altstreets file usin region and export to Model_Inputs.gdb
    AltStreets = os.path.join(Model_Inputs_gdb, fr"AltStreets")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'AltStreets.shp'), clip_features=region, out_feature_class=AltStreets, cluster_tolerance="")
    print('AltStreets Exported')
 
    # Clip the zlevels file usin region and export to Model_Inputs.gdb
    Zlevels = os.path.join(Model_Inputs_gdb, fr"Zlevels")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Zlevels.shp'), clip_features=region, out_feature_class=Zlevels, cluster_tolerance="")
    print('ZLevels Exported')

    # Clip the AdminBndry4 (City) file usin region and export to Model_Inputs.gdb
    Adminbndy4 = os.path.join(Model_Inputs_gdb, fr"Adminbndy4")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Adminbndy4.shp'), clip_features=region, out_feature_class=Adminbndy4, cluster_tolerance="")
    print('Adminbndy4 Exported')

    # Clip the Place file usin region and export to Model_Inputs.gdb
    NamedPlc = os.path.join(Model_Inputs_gdb, fr"NamedPlc")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'NamedPlc.shp'), clip_features=region, out_feature_class=NamedPlc, cluster_tolerance="")
    print('NamedPlc Exported')

    # Clip the AdminBndry3 (County) file usin region and export to Model_Inputs.gdb
    Adminbndy3 = os.path.join(Model_Inputs_gdb, fr"Adminbndy3")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Adminbndy3.shp'), clip_features=region, out_feature_class=Adminbndy3, cluster_tolerance="")
    print('Adminbndy3 Exported')
    
    water = os.path.join(Model_Inputs_gdb, fr"Water")
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'WaterSeg.shp'), clip_features=region, out_feature_class=water, cluster_tolerance="")
    print('WaterSeg Exported')

    return os.path.join(Project_Folder, Model_Inputs_gdb)

