import arcpy
import os
from dotenv import load_dotenv

from .extract import extract
from .mapmaker import convertStreets, convertAltStreets, mergeStreets


def run(project_dir, here_dir, us_counties):
    extract()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
# Project Dir = Where you want everything to live.
project_dir = os.path.dirname(__file__)
# HERE Dir = Where the original HERE files are.

# US Counties = Where the US Counties are located (Download from Tiger site) 
# https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/tl_2020_us_county.zip
