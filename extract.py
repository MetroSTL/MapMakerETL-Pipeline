import arcpy
from sys import argv
import os



# This function will run and Clip the full files that exist within the HERE_Data folder 
# (folder with all of the shapefiles that make up the Here dataset and output them to the output gdb)

# Project_Folder = Where things will end up
# HERE_DATA = Where the HERE data lives (directory)
# us_counties = US Census data file that has all of the counties in the united states --> https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip



def extract(Project_Folder, HERE_Data, us_counties):  # 01-Extract and Copy
    Select_State="\"STATEFP\" IN ('17', '29')"
    Select_Counties="\"NAMELSAD\" IN ('St. Louis city', 'St. Louis County', 'St. Clair County' )"

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = HERE_Data
    

    # Process: Create File Geodatabase (Create File Geodatabase) 
    Model_Inputs_gdb = arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model Inputs", out_version="CURRENT")[0]

    # Process: Create File Geodatabase (2) (Create File Geodatabase) 
    Model_Outputs_gdb = arcpy.CreateFileGDB_management(out_folder_path=Project_Folder, out_name="Model Outputs", out_version="CURRENT")[0]

    # Process: Select_Data (Select Data) 
    # Select Data Utility is not implemented 

    # Process: Select (Select) 
    tl_2017_us_county_state_selected = fr"{Project_Folder}\Model Inputs.gdb\tl_2017_us_county_state_selected"
    arcpy.Select_analysis(in_features=os.path.join(Project_Folder, us_counties), out_feature_class=tl_2017_us_county_state_selected, where_clause=f"{Select_State}")

    # Process: Select (2) (Select) 
    tl_2017_us_county_counties_selected = fr"{Project_Folder}\Model Inputs.gdb\tl_2017_us_county_counties_selected"
    arcpy.Select_analysis(in_features=tl_2017_us_county_state_selected, out_feature_class=tl_2017_us_county_counties_selected, where_clause=f"{Select_Counties}")

    # Process: Clip (Clip) 
    Streets = fr"{Project_Folder}\Model Inputs.gdb\Streets"
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Streets.shp'), clip_features=tl_2017_us_county_counties_selected, out_feature_class=Streets, cluster_tolerance="")

    # Process: Select_Data_2_ (Select Data) 
    # Select Data Utility is not implemented 

    # Process: Clip (2) (Clip) 
    AltStreets = fr"{Project_Folder}\Model Inputs.gdb\AltStreets"
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'AltStreets.shp'), clip_features=tl_2017_us_county_counties_selected, out_feature_class=AltStreets, cluster_tolerance="")

    # Process: Select_Data_3_ (Select Data) 
    # Select Data Utility is not implemented 

    # Process: Clip (3) (Clip) 
    Zlevels = fr"{Project_Folder}\Model Inputs.gdb\Zlevels"
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Zlevels.shp'), clip_features=tl_2017_us_county_counties_selected, out_feature_class=Zlevels, cluster_tolerance="")

    # Process: Select_Data_4_ (Select Data) 
    # Select Data Utility is not implemented 

    # Process: Clip (4) (Clip) 
    Adminbndy4 = fr"{Project_Folder}\Model Inputs.gdb\Adminbndy4"
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Adminbndy4.shp'), clip_features=tl_2017_us_county_counties_selected, out_feature_class=Adminbndy4, cluster_tolerance="")

    # Process: Select_Data_5_ (Select Data) 
    # Select Data Utility is not implemented 

    # Process: Clip (5) (Clip) 
    NamedPlc = fr"{Project_Folder}\Model Inputs.gdb\NamedPlc"
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'NamedPlc.shp'), clip_features=tl_2017_us_county_counties_selected, out_feature_class=NamedPlc, cluster_tolerance="")

    # Process: Select_Data_6_ (Select Data) 
    # Select Data Utility is not implemented 

    # Process: Clip (6) (Clip) 
    Adminbndy3 = fr"{Project_Folder}\Model Inputs.gdb\Adminbndy3"
    arcpy.Clip_analysis(in_features=os.path.join(HERE_Data, 'Adminbndy3.shp'), clip_features=tl_2017_us_county_counties_selected, out_feature_class=Adminbndy3, cluster_tolerance="")

    return os.path.join(Project_Folder, Model_Inputs_gdb)

