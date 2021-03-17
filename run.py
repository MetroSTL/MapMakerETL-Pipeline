import os
from dotenv import load_dotenv

from lib.admin import extract, mergeLines
from lib.water import convertWater
from lib.streets import convertStreets, convertAltStreets, findAndIsolateOldEdits
from lib.avl import processAVLFiles


def run():
    # define custom env variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Project Dir = Where you want everything to live.
    # AVL.gdb, Model_Input.gdb, Model_Output.gdb final shp file and mid/mif files live here
    Project_Folder = os.environ['PROJECT_DIR']

    # HERE Dir = Where the original HERE files are.
    # all of the files are shp files that just live in this directory
    HERE_Data = os.environ['HERE_DATA']
    PREV_MAP = os.environ['PREV_MAP']
    US_COUNTIES = os.path.join(os.getcwd(), r'county\cb_2017_us_county_500k.shp')

    # where the us couties shapefile lives
    # extract and clip files to STL region => Model_Input.gdb
    # streets, altstreets, water, zlevels
    extract(Project_Folder, HERE_Data)

    # convert streets process => model_outputs.gdb\\Streets_Final
    convertStreets(Project_Folder, US_COUNTIES)

    # convert altstreet process => model_outputs.gdb\\AltStreets_Final
    convertAltStreets(Project_Folder)
    
    # water conversions process => model_outputs.gdb\\Water_Final
    convertWater(Project_Folder)

    # find all of the edits in the former file =>  model_output.gdb\\Previous_Edits
    findAndIsolateOldEdits(Project_Folder, PREV_MAP)


    ## merge the streets, altstreets and water files => model_output.gdb\\MapMakerCenterline_final
    mergeLines(Project_Folder)

    processAVLFiles(Project_Folder)
    

# run the damn thing
run()