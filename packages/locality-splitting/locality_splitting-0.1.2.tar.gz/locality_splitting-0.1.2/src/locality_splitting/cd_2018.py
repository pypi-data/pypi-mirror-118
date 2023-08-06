import pandas as pd
import pkg_resources

def get_block_equivalency_file():

    # get path to data file
    path = pkg_resources.resource_stream(__name__, 'cd_2018_block_equiv.csv')

    # read in file from data
    cd_2018_block_equiv = pd.read_csv(path, dtype={'GEOID' : str, 'pop' : int, 'cd_2018' : str})

    # make GEOID str and zfill to 15 chars
    cd_2018_block_equiv['GEOID'] = cd_2018_block_equiv['GEOID'].astype(str).str.zfill(15)
    if not all(cd_2018_block_equiv['GEOID'].str.len() == 15):
        raise ValueError("census block GEOIDs did not properly zfill to length 15")

    # return DataFrame
    return cd_2018_block_equiv
