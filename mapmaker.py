import arcpy
from sys import argv
import os

# takes the project folder and us_counties env var and create an updated schema for the streets file to match what is needed for the mapmaker program
# adds in turning restrictions with zlevel information to nref_lev and ref_lev fields
# calculates names and id's of cities counties and states
# recalculates oneway to specific mapmaker format
# recalculates cfcc (functional road classes) to mapmaker format
# makes assumtions on speed of road if there is no data in speed field
def convertStreets(Project_Folder, us_counties):
    arcpy.env.overwriteOutput = True

    Model_Inputs_gdb = os.path.join(Project_Folder, 'Model_Inputs.gdb')
    Model_Outputs_gdb = os.path.join(Project_Folder, 'Model_Outputs.gdb')

    streets = os.path.join(Model_Inputs_gdb, 'Streets')
    zlevels = os.path.join(Model_Inputs_gdb, 'Zlevels')
    adminbound4 = os.path.join(Model_Inputs_gdb, 'Adminbndy4')

    arcpy.env.workspace = Model_Inputs_gdb
    
    # Simplify AltStreets and Streets Lines
    streets_simple = arcpy.SimplifyLine_cartography(in_features=streets, out_feature_class=os.path.join(Model_Outputs_gdb, "Streets_Simple"), algorithm="POINT_REMOVE", tolerance="5 Feet", error_resolving_option="RESOLVE_ERRORS", collapsed_point_option="KEEP_COLLAPSED_POINTS", error_checking_option="CHECK", in_barriers=[])[0]
    
    arcpy.AddFields_management(in_table=streets_simple, field_description=[["REF_ZLEV", "LONG", "", "", "", ""], 
                                                                            ["NREF_ZLEV", "LONG", "", "", "", ""], 
                                                                            ["PlaceCodeL", "LONG", "", "", "", ""], 
                                                                            ["PlaceCodeR", "LONG", "", "", "", ""], 
                                                                            ["PlaceNamL", "TEXT", "", "255", "", ""], 
                                                                            ["PlaceNamR", "TEXT", "", "255", "", ""], 
                                                                            ["CountyCodeL", "LONG", "", "", "", ""], 
                                                                            ["CountyCodeR", "LONG", "", "", "", ""], 
                                                                            ["CountyNamL", "TEXT", "", "255", "", ""], 
                                                                            ["CountyNamR", "TEXT", "", "255", "", ""], 
                                                                            ["StateCodeL", "LONG", "", "", "", ""], 
                                                                            ["StateCodeR", "LONG", "", "", "", ""], 
                                                                            ["StateAbbrL", "TEXT", "", "255", "", ""], 
                                                                            ["StateAbbrR", "TEXT", "", "255", "", ""], 
                                                                            ["OneWay", "SHORT", "", "", "", ""], 
                                                                            ["Speed", "LONG", "", "", "", ""], 
                                                                            ["CFCC", "TEXT", "", "255", "", ""], 
                                                                            ["M_LINK_ID", "LONG", "", "", "", ""], 
                                                                            ["OLD_LINK_ID", "LONG", "", "", "", ""]])


    print('Fields added to Streets')
    
    arcpy.JoinField_management(in_data=streets_simple, in_field="REF_IN_ID", join_table=zlevels, join_field="NODE_ID", fields=["Z_LEVEL"])
    zlevelCalc ="""zlevCalc(!Z_LEVEL!)", expression_type="PYTHON3", code_block="def zlevCalc(z):
    if(z != 0):
        return z 
    else:
        return 0"""
    arcpy.CalculateField_management(in_table=streets_simple, field="REF_ZLEV", expression = "zlevCalc(!Z_LEVEL!)", expression_type="PYTHON3", code_block="""def zlevCalc(z):
    if(z != 0):
        return z 
    else:
        return 0""", field_type="TEXT")
    arcpy.DeleteField_management(in_table=streets_simple, drop_field=["ZLEVEL"])
    print('REF_ZLEV Calculated')
    
    # calculate NREF
    arcpy.JoinField_management(in_data=streets_simple, in_field="NREF_IN_ID", join_table=zlevels, join_field="NODE_ID", fields=["Z_LEVEL"])
    zNlevelCalc ="""def zlevCalc(z):
    if(z != 0):
        return z
    else:
        return 0"""
    arcpy.CalculateField_management(in_table=streets_simple, field="NREF_ZLEV", expression="zlevCalc(!Z_LEVEL!)", expression_type="PYTHON3", code_block="""def zlevCalc(z):
    if(z != 0):
        return z
    else:
        return 0""", field_type="TEXT")
    arcpy.DeleteField_management(in_table=streets_simple, drop_field=["ZLEVEL"])
    print('NREF_ZLEV Calculated')


    # Calculate Cities/AdminBndry4 fields
    # calculate R_AREA Cities
    arcpy.JoinField_management(in_data=streets_simple, in_field="R_AREA_ID", join_table=adminbound4, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceCodeR", expression="!AREA_ID!", expression_type="PYTHON3")
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceNameR", expression="placeNameCalc(!POLYGON_NM!)", expression_type="PYTHON3", code_block="""def placeNameCalc(name):
    if name == 'ST LOUIS':
        return 'ST LOUIS CITY'
    else:
        return name""")
    arcpy.DeleteField_management(in_table=streets_simple, drop_field=["AREA_ID", "POLYGON_NM"])
    
    # calculate L_AREA Cities
    arcpy.JoinField_management(in_data=streets_simple, in_field="L_AREA_ID", join_table=adminbound4, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceCodeL", expression_type="PYTHON3", expression="!AREA_ID!")
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceNameL", expression_type="PYTHON3", expression="placeNameCalc(!POLYGON_NM!)",  code_block="""def placeNameCalc(name):
    if name == 'ST LOUIS':
        return 'ST LOUIS CITY'
    else:
        return name.upper()""")
    arcpy.DeleteField_management(in_table=streets_simple, drop_field=["AREA_ID", "POLYGON_NM"])
    print('Cities Calculated')
    

    # Calculate County fields
    # CountyNameR, CountyNameL, CountyCodeL, CountyCodeR
    county_streets = arcpy.SpatialJoin_analysis(streets_simple, us_counties, "county_streets")[0]
    arcpy.JoinField_management(in_data=streets_simple, in_field="LINK_ID", join_table=county_streets, join_field="LINK_ID", fields=["GEOID", "NAME"])
    arcpy.CalculateField_management(in_table=streets_simple, field="CountyNameR", expression="placeNameCalc(!GEOID!, !NAME!)", expression_type="PYTHON3", code_block="""def placeNameCalc(geoid, name):
    if geoid == '29189':
        return 'ST LOUIS'
    elif geoid == '29510':
        return 'ST LOUIS CITY'
    elif geoid == '17163':
        return 'ST CLAIR'
    else:
        return name.upper()""")

    arcpy.CalculateField_management(in_table=streets_simple, field="CountyNameL", expression="placeNameCalc(!GEOID!, !NAME!)", expression_type="PYTHON3", code_block="""def placeNameCalc(geoid, name):
    if geoid == '29189':
        return 'ST LOUIS'
    elif geoid == '29510':
        return 'ST LOUIS CITY'
    elif geoid == '17163':
        return 'ST CLAIR'
    else:
        return name.upper()""")

    arcpy.CalculateField_management(in_table=streets_simple, field="CountyCodeR", expression="!GEOID!", expression_type="PYTHON3")
    arcpy.CalculateField_management(in_table=streets_simple, field="CountyCodeL", expression="!GEOID!", expression_type="PYTHON3")

    print("County Calculated")
    
    # Calculate State fields
    # StateAbbrL, StateAbbrR, StateCodeL, StateCodeR
    arcpy.CalculateField_management(in_table=streets_simple, field="StateCodeL", expression_type="PYTHON3", expression="!GEOID![0:2]")
    arcpy.CalculateField_management(in_table=streets_simple, field="StateAbbrL", expression_type="PYTHON3", expression="stateAbbr(!StateCodeL!)", code_block="""def stateAbbr(statecode):
    if statecode == 29:
        return 'MO'
    else:
        return 'IL' """)
    arcpy.CalculateField_management(in_table=streets_simple, field="StateCodeR", expression_type="PYTHON3", expression="!GEOID![0:2]")
    arcpy.CalculateField_management(in_table=streets_simple, field="StateAbbrR", expression_type="PYTHON3", expression="stateAbbr(!StateCodeR!)", code_block="""def stateAbbr(statecode):
    if statecode == 29:
        return 'MO'
    else:
        return 'IL' """)

    arcpy.DeleteField_management(in_table=streets_simple, drop_field=["GEOID", "NAME"])


    # One Way Calculation
    # T = > 
    # F = <
    # if blank is not a one way road and returns blank
    arcpy.CalculateField_management(in_table=streets_simple, field="OneWay", expression="oneWCalc(!DIR_TRAVEL!)", expression_type="PYTHON3", code_block="""def oneWCalc(dir):
    if(dir == "T"):
        return ">"
    elif(dir == "F"):
        return "<"
    else:
        return '' """)
    
    # calculated speed with to and from speeds
    # uses either to or from speed depending on direction for oneway speed calcs
    arcpy.CalculateField_management(in_table=streets_simple, field="Speed", expression="speedCalc(!DIR_TRAVEL!,!TO_SPD_LIM!,!FR_SPD_LIM!)", expression_type="PYTHON3", code_block="""def speedCalc(dir, toSpeed, fromSpeed):
    if(dir == 'T'):
        return toSpeed
    else:
        return fromSpeed """)
    print('OneWay Calculated')
    
    
    # Calculate Speeds based on category
    # Calculates speed fields that are empty with the speed calc field specs from HERE documentation
    arcpy.CalculateField_management(in_table=streets_simple, field="Speed", expression="nullSpeedCalc(!Speed!, !SPEED_CAT!)", expression_type="PYTHON3", code_block="""def nullSpeedCalc(speed, cat):
    if(speed is None):
        if(cat == '8'):
            return 15
        elif(cat == '7'):
            return 20
        elif(cat == '6'):
            return 25
        elif(cat == '5'):
            return 35 """)
    print('Speed Calculated')
    
    # Calculate Functional Classes
    # functional classes that adhear to the map maker specification
    arcpy.CalculateField_management(in_table=streets_simple, field="CFCC", expression="cfccCalc(!FUNC_CLASS!)", expression_type="PYTHON3", code_block="""def cfccCalc(fClass):
    if(fClass == 1):
        return 'A10'
    elif(fClass == 2):
        return 'A20'
    elif(fClass == 3):
        return 'A30'
    elif(fClass == 4 or fClass == 5):
        return 'A40' """)
    
    arcpy.CalculateFields_management(in_table=streets_simple, expression_type="PYTHON3", fields=[["M_LINK_ID", "!OBJECTID!"], ["OLD_LINK_ID", "!LINK_ID!"]], code_block="")[0]
    print('CFCC Calculated')

    # updated the schema to match mapmaker schema
    updateSchema(streets_simple)

    return arcpy.FeatureClassToFeatureClass_conversion(in_features=streets_simple, out_path=Model_Outputs_gdb, out_name="Streets_Final")[0]


# This fucntion is the way to change the HERE data spec to the mapmaker spec for the altstreets file (alias' file) for alternate street names
# this function takes in the project folder environemental variable as a single argument to find files that it needs
# this process runs after the extract() and that is where the files are extracted to their gdb's
# all data from this function is output to the Model_Output.gdb
def convertAltStreets(Project_Folder):
    arcpy.env.overwriteOutput = True

    Model_Inputs_gdb = os.path.join(Project_Folder, 'Model_Inputs.gdb')
    Model_Outputs_gdb = os.path.join(Project_Folder, 'Model_Outputs.gdb')

    streets_simple = os.path.join(Model_Outputs_gdb, 'Streets_Simple')
    altstreets = os.path.join(Model_Inputs_gdb, 'AltStreets')

    arcpy.env.workspace = Model_Inputs_gdb
    
    # Simplify AltStreets and Streets Lines
    # removes some of the nodes that make up the lines to make the files low resolution enough to be uploaded through mapmaker
    altstreets_simple = arcpy.SimplifyLine_cartography(in_features=altstreets, out_feature_class=os.path.join(Model_Outputs_gdb, "AltStreet_simple"), algorithm="POINT_REMOVE", tolerance="5 Feet", error_resolving_option="RESOLVE_ERRORS", collapsed_point_option="KEEP_COLLAPSED_POINTS", error_checking_option="CHECK", in_barriers=[])[0]
    
    # add ref_zlev and dom fields for alias classification and linking to streets file
    arcpy.AddFields_management(in_table=altstreets_simple, field_description=[["REF_ZLEV", "SHORT"], ["DOM", "LONG"]])
    print('added fields to altstreets')

    arcpy.AddIndex_management(altstreets_simple, fields=["LINK_ID"], index_name="LINK_ID", unique="NON_UNIQUE", ascending="ASCENDING")
    print('added altstreet index')

    arcpy.JoinField_management(in_data=altstreets_simple, in_field="LINK_ID", join_table=streets_simple, join_field="LINK_ID", fields=["NUM_STNMES"])
    print('joined altstreets to streets')

    # Filter out all of the altstreet rows that do not have multiple names
    altstreets_filter = arcpy.FeatureClassToFeatureClass_conversion(in_features=altstreets_simple, out_path=Model_Outputs_gdb, out_name="AltStreets_Filter", where_clause="NUM_STNMES > 1")
    print('altstreets filtered if less than 2')

    # Create Statistics Table from AltStreets_Simple
    altstreet_stats = os.path.join(Model_Outputs_gdb, "Altstreets_Stats")
    arcpy.Statistics_analysis(in_table=altstreets_filter, out_table=altstreet_stats, statistics_fields=[["LINK_ID", "FIRST"]], case_field=["LINK_ID", "ST_NAME"])

    # Join AltStreets_Simple with AltStreets_Stats
    arcpy.JoinField_management(in_data=altstreets_simple, in_field="LINK_ID", join_table=altstreet_stats, join_field="LINK_ID", fields=["NUM_STNMES"])

    arcpy.CalculateField_management(in_table=altstreets_simple, field="Dom", expression="1", expression_type="PYTHON3", code_block="", field_type="TEXT")

    # Alias streetname identifier calculation (Alias == -9)
    arcpy.CalculateField_management(in_table=altstreets_simple, field="REF_ZLEV", expression="-9", expression_type="PYTHON3", code_block="", field_type="TEXT")

    # updated the schema to match mapmaker schema
    updateSchema(altstreets_simple)

    return arcpy.FeatureClassToFeatureClass_conversion(in_features=altstreets_simple, out_path=Model_Outputs_gdb, out_name="AltStreets_Final")[0]

# # function to update to the 'M_' field schema that is documented in the documentation
# # adds fields then finds all fields that are not in the specified schema and removes them after moving to a new file
def updateSchema(streets_file):
    # list of fields that need to be added by the end
    add_fields = [{"new":'M_LINK_ID', "old": 'LINK_ID', "type": 'Double'}, 
    {"new": 'M_ST_PREF', "old": "ST_TYP_BEF", "type": 'Text'}, 
    {"new": 'M_SEG_NAME', "old": "ST_NM_BASE", "type": 'Text'},
    {"new":'M_ST_AFT', "old": "ST_TYP_AFT", "type": 'Text'}, 
    {"new": 'M_ST_NM', "old": 'ST_NAME', "type": 'Text'}, 
    {"new": 'M_CFCC', "old": "CFCC", "type": 'Text'}, 
    {"new": 'M_ALIAS', "old": "REF_ZLEV", "type": 'Long'}, 
    {"new": 'M_STATE', "old": "StateAbbrL", "type": 'Text'}, 
    {"new":'M_SPEED', "old": "Speed", "type": 'Long'}, 
    {"new": 'M_LEFT_PL', "old": "PlaceNamL", "type": 'Text'}, 
    {"new": 'M_RIGHT_PL', "old": "PlaceNamR", "type": 'Text'}, 
    {"new": 'M_F_ZLEV', "old": "REF_ZLEV", "type": 'Long'}, 
    {"new": 'M_T_ZLEV', "old": "NREF_ZLEV", "type": 'Long'},  
    {"new": 'M_ONEWAY', "old": "OneWay", "type": 'Text'},  
    {"new":'M_OLD_ID', "old": "M_LINK_ID", "type": 'Long'}, 
    ]

    # # create a list of all of the fields that are in the streets_file
    streets_file_fields = []
    for field in arcpy.ListFields(streets_file):
        streets_file_fields.append(field.name)

    # if the new field is not in the file add it and update the field from the old field name
    for field in add_fields:
        if field['new'] not in streets_file_fields and field['old'] in streets_file_fields:
            arcpy.AddField_management(streets_file, field['new'], field['type'])
            arcpy.CalculateField_management(streets_file, field['new'], f"!{field['old']}!", expression_type="PYTHON3")
    print(f'{streets_file} schema updated')


# file merges the altstreets and streets file that was output from the convertStreets() and convertAltStreets()
def mergeStreets(Project_Folder):
    Model_Outputs_gdb = os.path.join(Project_Folder, "Model_Outputs.gdb")

    streets_final= os.path.join(Model_Outputs_gdb, "Streets_Final")
    altstreets_final= os.path.join(Model_Outputs_gdb, "AltStreets_Final")
    
    arcpy.env.workspace = Model_Outputs_gdb

    # returns the file location in the Model_Outputs.gdb
    return arcpy.Merge_management(inputs=[streets_final, altstreets_final], output='AllStreets_Final')[0]

# takes in the old map location as the arguement to find rows that have been indicated under the 'M_EDIT' field as > 1
# outputs to Model_Outputs GDB as Previous_Edits
def findAndIsolateOldEdits(Project_Folder, prev_map):
    Model_Outputs_gdb = os.path.join(Project_Folder, "Model_Outputs.gdb")
    arcpy.FeatureClassToFeatureClass_conversion(prev_map, out_path=Model_Outputs_gdb, out_name="Previous_Edits", where_clause="M_EDIT > 0")