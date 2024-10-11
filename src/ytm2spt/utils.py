from thefuzz import process, fuzz
from .app_logger import setup_logger


utils_logger = setup_logger(__name__)

def artist_names_from_tracks(items: dict):
    artist_names = set()

    for idx, track in enumerate(items):
        artist_names.add(track['artists'][0]['name'])
    return artist_names


def fuzzy_match_artist(artist_names: set, track_input: str) -> bool: 
    match_grade = process.extract(track_input, artist_names, limit=3, scorer=fuzz.token_sort_ratio)
    try:
        if match_grade[0][1] > 70:
            print(f'Fuzy match found {match_grade}')
            return True
        else:
            print(f'Fuzy match not found {match_grade}')
            return False
    except IndexError:
        utils_logger.debug('Issue with ingest to fuzzmatch with data')
        utils_logger.debug(f'Track {track_input}')
        utils_logger.debug(f'{artist_names}')
        print("No data provided to matching process")
        return False
