import arcpy
import os
from dotenv import load_dotenv

from extract import extract
from mapmaker import convertStreets, convertAltStreets, mergeStreets


def run():
    # define custom env variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Project Dir = Where you want everything to live.
    Project_Folder = os.environ['PROJECT_DIR']

    # HERE Dir = Where the original HERE files are.
    HERE_Data = os.environ['HERE_DATA']

    # where the us couties shapefile lives
    us_counties = os.environ['US_COUNTIES']

    # extract and clip files to STL region
    extract(Project_Folder, HERE_Data, us_counties)

    # convert streets process
    try:
        convertStreets(Project_Folder)
    except:
        print('Failed on Converting Streets')
        return

    # attempt to convert the 
    try:
        convertAltStreets(Project_Folder)
    except:
        print('Failed on Converting AltStreets')
        return

    # attempt merging the streets with the altstreets file
    try:
        mergeStreets(Project_Folder)
    except:
        print('Failed on merged Streets and AltStreets')
        return


# run the damn thing
run()