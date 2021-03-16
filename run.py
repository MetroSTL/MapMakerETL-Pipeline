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
    US_COUNTIES = os.path.join(os.getcwd(), r'county\cb_2017_us_county_500k.shp')

    # where the us couties shapefile lives
    # extract and clip files to STL region
    extract(Project_Folder, HERE_Data)

    # convert streets process
    # try:
    convertStreets(Project_Folder, US_COUNTIES)
    # except:
    #     print('Failed on Converting Streets')
    #     return

    # attempt to convert the 
    # try:
    #     convertAltStreets(Project_Folder)
    # except:
    #     print('Failed on Converting AltStreets')
    #     return

    # # attempt merging the streets with the altstreets file
    # try:
    #     mergeStreets(Project_Folder)
    # except:
    #     print('Failed on merged Streets and AltStreets')
    #     return


# run the damn thing
run()