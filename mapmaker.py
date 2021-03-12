import arcpy
from sys import argv
import os

def convertStreets(Project_Folder):
    Model_Inputs_gdb = os.path.join(Project_Folder, 'Model_Inputs.gdb')
    Model_Outputs_gdb = os.path.join(Project_Folder, 'Model_Outputs.gdb')

    streets = os.path.join(Model_Inputs_gdb, 'Streets')
    zlevels = os.path.join(Model_Inputs_gdb, 'Zlevels')
    adminbound4 = os.path.join(Model_Inputs_gdb, 'Adminbndy4')
    adminbound3 = os.path.join(Model_Inputs_gdb, 'Adminbndy3')

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
            
    
    
    # add some fields
    
    # add in zlevel data to streets
    # calculate REF
    arcpy.JoinField_management(in_data=streets_simple, in_field="REF_IN_ID", join_table=zlevels, join_field="NODE_ID", fields=["Z_LEVEL"])
    zlevelCalc ="""zlevCalc(!Z_LEVEL!)", expression_type="PYTHON3", code_block="def zlevCalc(z):
    if(z != 0):
        return z 
    else:
        return 0"""
    arcpy.CalculateField_management(in_table=streets_simple, field="REF_ZLEV", expression = "zlevCalc(!Z_LEVEL!)", expression_type="PYTHON3", code_block=zlevelCalc, field_type="TEXT")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["ZLEVEL"])
    
    
    # calculate NREF
    arcpy.JoinField_management(in_data=streets_simple, in_field="NREF_IN_ID", join_table=zlevels, join_field="NODE_ID", fields=["Z_LEVEL"])
    zNlevelCalc ="""def zlevCalc(z):
    if(z != 0):
        return z
    else:
        return 0"""
    arcpy.CalculateField_management(in_table=streets_simple, field="NREF_ZLEV", expression="zlevCalc(!Z_LEVEL!)", expression_type="PYTHON3", code_block=zNlevelCalc, field_type="TEXT")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["ZLEVEL"])



    # Calculate Cities
   
    # calculate R_AREA Cities
    arcpy.JoinField_management(in_data=streets_simple, in_field="R_ID_AREA", join_table=adminbound4, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceCodeR", expression="!AREA_ID!", expression_type="PYTHON3")
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceNameR", expression="placeNameCalc(!POLYGON_NM!)", expression_type="PYTHON3", code_block="""def placeNameCalc(name):
    if name == 'ST LOUIS':
        return 'ST LOUIS CITY'
    else:
        return name""")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["AREA_ID", "POLYGON_NM"])
    
    # calculate L_AREA Cities
    arcpy.JoinField_management(in_data=streets_simple, in_field="L_ID_AREA", join_table=adminbound4, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceCodeL", expression_type="PYTHON3", expression="!AREA_ID!")
    arcpy.CalculateField_management(in_table=streets_simple, field="PlaceNameL", expression_type="PYTHON3", expression="placeNameCalc(!POLYGON_NM!)",  code_block="""def placeNameCalc(name):
    if name == 'ST LOUIS':
        return 'ST LOUIS CITY'
    else:
        return name""")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["AREA_ID", "POLYGON_NM"])
    

    # Calculate County
   
    # calculate R_AREA County
    arcpy.JoinField_management(in_data=streets_simple, in_field="R_ID_AREA", join_table=adminbound3, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="CountyCodeR", expression="!AREA_ID!", expression_type="PYTHON3")
    arcpy.CalculateField_management(in_table=streets_simple, field="CountyNameR", expression="placeNameCalc(!POLYGON_NM!)", expression_type="PYTHON3", code_block="""def placeNameCalc(name):
    if name == 'ST LOUIS (CITY)':
        return 'ST LOUIS CITY'
    else:
        return name""")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["AREA_ID", "POLYGON_NM"])
    
    # calculate L_AREA County
    arcpy.JoinField_management(in_data=streets_simple, in_field="L_ID_AREA", join_table=adminbound3, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="CountyCodeL", expression_type="PYTHON3", expression="!AREA_ID!")
    arcpy.CalculateField_management(in_table=streets_simple, field="CountyNameL", expression_type="PYTHON3", expression="placeNameCalc(!POLYGON_NM!)", code_block="""def placeNameCalc(name):
    if name == 'ST LOUIS (CITY)':
        return 'ST LOUIS CITY'
    else:
        return name""")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["AREA_ID", "POLYGON_NM"])
    
    
    # Calculate State
   
    # calculate R_AREA State
    arcpy.JoinField_management(in_data=streets_simple, in_field="R_ID_AREA", join_table=adminbound3, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="StateCodeR", expression="!AREA_ID!", expression_type="PYTHON3")
    arcpy.CalculateField_management(in_table=streets_simple, field="StateAbbrR", expression="placeAbbrCalc(!AREA_ID!)", expression_type="PYTHON3", code_block="""def placeAbbrCalc(id):
    if id > 21000000:
        return 21
    else:
        return 17""")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["AREA_ID", "POLYGON_NM"])
    
    # calculate L_AREA State
    arcpy.JoinField_management(in_data=streets_simple, in_field="L_ID_AREA", join_table=adminbound3, join_field="AREA_ID", fields=["AREA_ID", "POLYGON_NM"])
    arcpy.CalculateField_management(in_table=streets_simple, field="StateCodeL", expression_type="PYTHON3", expression="!AREA_ID!")
    arcpy.CalculateField_management(in_table=streets_simple, field="StateAbbrL", expression_type="PYTHON3", expression="placeAbbrCalc(!AREA_ID!)", code_block="""def placeAbbrCalc(id):
    if id > 21000000:
        return 21
    else:
        return 17""")
    arcpy.DeleteField_management(in_table=streets_simple, fields=["AREA_ID", "POLYGON_NM"])
    



    # One Way Calculation
    arcpy.CalculateField_management(in_table=streets_simple, field="OneWay", expression="oneWCalc(!DIR_TRAVEL!)", expression_type="PYTHON3", code_block="""def oneWCalc(dir):
    if(dir == "T"):
        return ">"
    elif(dir == "F"):
        return "<"
    else:
        return '' """)
    
    # calculated speed with to and from speeds
    arcpy.CalculateField_management(in_table=streets_simple, field="Speed", expression="speedCalc(!DIR_TRAVEL!,!TO_SPD_LIM!,!FR_SPD_LIM!)", expression_type="PYTHON3", code_block="""def speedCalc(dir, toSpeed, fromSpeed):
    if(dir == 'T'):
        return toSpeed
    else:
        return fromSpeed""")
    
    
    # Calculate Speeds based on category
    arcpy.CalculateField_management(in_table=streets_simple, field="Speed", expression="nullSpeedCalc(!Speed!, !SPEED_CAT!)", expression_type="PYTHON3", code_block="""def nullSpeedCalc(speed, cat):
    if(speed is None):
        if(cat == '8'):
            return 15
        elif(cat == '7'):
            return 20
        elif(cat == '6'):
            return 25
        elif(cat == '5'):
            return 35""")
    
    # Calculate Functional Classes
    arcpy.CalculateField_management(in_table=streets_simple, field="CFCC", expression="cfccCalc(!FUNC_CLASS!)", expression_type="PYTHON3", code_block="""def cfccCalc(fClass):
    if(fClass == 1):
        return 'A10'
    elif(fClass == 2):
        return 'A20'
    elif(fClass == 3):
        return 'A30'
    elif(fClass == 4 or fClass == 5):
        return 'A40'""")
    
    arcpy.CalculateFields_management(in_table=streets_simple, expression_type="PYTHON3", fields=[["M_LINK_ID", "!OBJECTID!"], ["OLD_LINK_ID", "!LINK_ID!"]], code_block="")[0]

    return arcpy.FeatureClassToFeatureClass_conversion(in_features="Streets_Final", out_path=Model_Outputs_gdb, out_name="Streets_Final")[0]



def convertAltStreets(Project_Folder):
    Model_Inputs_gdb = os.path.join(Project_Folder, 'Model_Inputs.gdb')
    Model_Outputs_gdb = os.path.join(Project_Folder, 'Model_Outputs.gdb')

    streets_simple = os.path.join(Model_Outputs_gdb, 'Streets_Simple')
    altstreets = os.path.join(Model_Inputs_gdb, 'AltStreets')

    arcpy.env.workspace = Model_Inputs_gdb
    
    # Simplify AltStreets and Streets Lines
    altstreets_simple = arcpy.SimplifyLine_cartography(in_features=altstreets, out_feature_class=os.path.join(Model_Outputs_gdb, "AltStreet_simple"), algorithm="POINT_REMOVE", tolerance="5 Feet", error_resolving_option="RESOLVE_ERRORS", collapsed_point_option="KEEP_COLLAPSED_POINTS", error_checking_option="CHECK", in_barriers=[])[0]
    
    arcpy.AddFields_management(in_table=altstreets_simple, field_description=[["REF_ZLEV", "SHORT", "", "", "", ""], 
                                                                            ["DOM", "LONG", "", "", "", ""]])

    arcpy.AddIndex_management(altstreets_simple, ["LINK_ID"], "#", "NON_UNIQUE", "ASCENDING")

    arcpy.JoinField_management(in_data=altstreets_simple, in_field="LINK_ID", join_table=streets_simple, join_field="LINK_ID", fields=["NUM_STNMES"])

    # Filter out all of the altstreet rows that do not have multiple names
    altstreets_filter = arcpy.FeatureClassToFeatureClass_conversion(in_features=altstreets_simple, out_path=Model_Outputs_gdb, out_name="AltStreets_Filter", where_clause="NUM_STNMES > 1")

    # Create Statistics Table from AltStreets_Simple
    altstreet_stats = os.path.join(Model_Outputs_gdb, "Altstreets_Stats")
    arcpy.Statistics_analysis(in_table=altstreets_filter, out_table=altstreet_stats, statistics_fields=[["LINK_ID", "FIRST"]], case_field=["LINK_ID", "ST_NAME"])

    # Join AltStreets_Simple with AltStreets_Stats
    arcpy.JoinField_management(in_data=altstreets_simple, in_field="LINK_ID", join_table=altstreet_stats, join_field="LINK_ID", fields=["NUM_STNMES"])

    arcpy.CalculateField_management(in_table=altstreets_simple, field="Dom", expression="1", expression_type="PYTHON3", code_block="", field_type="TEXT")
    arcpy.CalculateField_management(in_table=altstreets_simple, field="REF_ZLEV", expression="-9", expression_type="PYTHON3", code_block="", field_type="TEXT")

    return arcpy.FeatureClassToFeatureClass_conversion(in_features="AltStreets_Final", out_path=Model_Outputs_gdb, out_name="AltStreets_Final")[0]


def mergeStreets(Project_Folder):
    Model_Outputs_gdb = os.path.join(Project_Folder, "Model_Outputs.gdb")

    streets_final= os.path.join(Model_Outputs_gdb, "Streets_Final")
    altstreets_final= os.path.join(Model_Outputs_gdb, "AltStreets_Final")
    
    arcpy.env.workspace = Model_Outputs_gdb
    
    return arcpy.Merge_management(inputs=[streets_final, altstreets_final], output='AllStreets_Final')[0]