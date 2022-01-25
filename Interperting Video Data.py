import doctest
from typing import List, Tuple, Dict, TextIO

# constants to identify columns within input file
INPUT_YOUTUBE_ID    = 0
INPUT_TRENDING_DT   = 1
INPUT_TITLE         = 2
INPUT_CHANNEL_TITLE = 3
INPUT_VIEWS         = 7
INPUT_LIKES         = 8
INPUT_DISLIKES      = 9

# constants to identify position of date values within input file date string
INPUT_YEAR  = 0
INPUT_DAY   = 1
INPUT_MONTH = 2

# represents a Gregorian date as: (year, month, day)
# where year is 2 digits reprensenting a year 2000 or later
# day is valid given the year and month
Date = Tuple[int, int, int]
YEAR  = 0
MONTH = 1
DAY = 2


# represents a video stat as (trending date, views, likes, dislikes)
# where all stats are >=0
VideoStats = Tuple[Date, int, int, int]


"""
Dictionaries to be used in this program
=========================================
Dict 1 - YouTube Id to video title:
Dict[str, str]
Precondition: the video title of a given YouTube Id never changes
Example:
{'VYOjWnS4cMY': 'Childish Gambino - This Is America (Official Video)',
'ffxKSjUwKdU': 'Ariana Grande - No Tears Left To Cry', 
'UwbO_xb1-Xo': 'KKW BEAUTY: Conceal  Bake  Brighten with Mario Dedivanovic',
'zPz-ogLUbqA': 'FIRST LOOK: #KKWxMARIO'}

Dict 2 - channel title to list of YouTube Ids that are on that channel:
Dict[str, List[str]]
Example:
{'Austin Evans': ['0Xi2rurVAvs'],
'Kim Kardashian West': ['zPz-ogLUbqA', 'UwbO_xb1-Xo']}

Dict 3 - YouTube Id to VideoStats on the latest trending date.
Dict[str, VideoStats]
Example:
{'G36BAjlL3pw': ((18, 6, 12), 2090150, 22799, 1241), 
'UwbO_xb1-Xo': ((18, 3, 25), 661775, 0, 0)}
NOTE: Duplicate entries of YouTube Id will be replaced if the new entry 
is a later trending date.  
For example, if lines of YouTube view data includes 3 lines that contain
the following title, Date, views, likes and dislikes
'UwbO_xb1-Xo', (18, 3, 25), 661775, 0, 0
'UwbO_xb1-Xo', (18, 4, 25), 661899, 3, 2
'UwbO_xb1-Xo', (17, 3, 25), 661115, 7, 7
(18, 4, 25) is the latest date, so the dictionary will have the following entry: 
'UwbO_xb1-Xo': ((18, 4, 25), 661899, 3, 2)
"""

def to_date(input_date: str) -> Date:
    """ converts the input_date to Date format and returns it
    
    Precondition: input_date is in form 'YY.DD.MM'
    >>> to_date('17.06.01')
    (17, 1, 6)
    >>> to_date('12.27.10')
    (12, 10, 27)
    """
    date_elements = input_date.split('.')
    result_date = (int(date_elements[INPUT_YEAR]), 
                   int(date_elements[INPUT_MONTH]), 
                   int(date_elements[INPUT_DAY]))
    
    return result_date 


def get_recent(new_date: Date, current_date: Date) -> bool or str:
    '''
    Determins if new_date is the more recent date compared to current_date.
    Returns True, False, or 'both'
    
    Precondition: new_date and current_date must not be empty tuples
    
    >>> get_recent((10, 2, 3), (10, 2, 4))
    False
    >>> get_recent((12, 2, 3), (10, 2, 4))
    True
    >>> get_recent((10, 2, 4), (10, 2, 4))
    'both'
    '''
    new_date_recent = False
    
    if new_date > current_date:
        new_date_recent = True
        
    elif new_date == current_date:
        new_date_recent = 'both'
    
    return new_date_recent


def get_recent_stats(youtube_id: str, new_date: Date, views: int, likes: int, dislikes: int, id_stats: Dict[str, VideoStats]) -> None:
    '''
    Mutates dictionary 
    if new stats are more recent than current stats, then use new stats and
    if video data not in id_stats, then append id_stats dictionary
    
    - id_stats: Dict[YouTube id, latest video stat]
    '''
    
    #if video data already is within id_stats
    if youtube_id in id_stats:
        current_stats = id_stats[youtube_id]
        current_date  = current_stats[0]
    
        #if new stats are more recent than current stats, then use new stats
        if get_recent(new_date, current_date):
            stats = (new_date, views, likes, dislikes)
            id_stats[youtube_id] = stats
    
    #if video data not in id_stats, then append id_stats dictionary       
    else:
        stats = (new_date, views, likes, dislikes)
        id_stats[youtube_id] = stats    


def get_channel_ids(youtube_id: str, channel: str, channel_ids: Dict[str, List[str]]) -> None:
    '''
    Mutates dictionary 
    if channel does not already exist in dictionary, then append dictionary and
    if channel does exist in dictionary, then append youtube ids of dictionary
    
    - channel_ids: Dict[channel title, list of YouTube ids]
    '''
    #if channel does not already exist in dictionary, then append dictionary
    if channel not in channel_ids:
        channel_ids[channel] = [youtube_id]
            
    #if channel does exist in dictionary, then append youtube ids of dictionary
    elif youtube_id not in channel_ids[channel]:
        channel_ids[channel].append(youtube_id)  
        
        
def get_video_info(video: list) -> (str, str, str, Date, int, int, int):
    '''
    Returns video information
    '''
    #main vid info
    youtube_id  = video[INPUT_YOUTUBE_ID]
    title       = video[INPUT_TITLE]
    channel     = video[INPUT_CHANNEL_TITLE]
    
    #stats
    trend_date = video[INPUT_TRENDING_DT]
    views      = int(video[INPUT_VIEWS])
    likes      = int(video[INPUT_LIKES])
    dislikes   = int(video[INPUT_DISLIKES])  
    
    return (youtube_id, title, channel, trend_date, views, likes, dislikes)

def file_to_dicts(file_handle: TextIO) -> (Dict[str, str],
                                           Dict[str, List[str]],
                                           Dict[str, VideoStats]):
    """ Populates and returns a tuple with the following 3 dictionaries
    based on data from file.
    
    Preconditions: The title of a specific YouTube video never changes:
    A YouTube id can be duplicated across lines in the file,
    but in this case the video titles will also be the same across those lines.
    
    The 1st line of file is a header row and it is ignored.
    Subsequent lines are in csv format with values according to header row.
    
    3 dictionaries returned as a tuple:
    - Dict[YouTube id, video title]
    - Dict[channel title, list of YouTube ids]
    - Dict[YouTube id, latest video stat]
    
    >>> nolines = open('EmptyFile.csv')
    >>> file_to_dicts(nolines)
    ({}, {}, {})
    >>> nolines.close()
    
    >>> sevenlines = open('SevenLines.csv')
    >>> file_to_dicts(sevenlines)
    ({'G36BAjlL3pw': 'Trump Makes The G7 Summit Awkwaaaard', 'UwbO_xb1-Xo': 'KKW BEAUTY: Conceal  Bake  Brighten with Mario Dedivanovic', 'VYOjWnS4cMY': 'Childish Gambino - This Is America (Official Video)', 'nlozE2m-NMc': "Deadpool Takes Over Stephen's Monologue", 'zPz-ogLUbqA': 'FIRST LOOK: #KKWxMARIO'}, {'The Late Show with Stephen Colbert': ['G36BAjlL3pw', 'nlozE2m-NMc'], 'Kim Kardashian West': ['UwbO_xb1-Xo', 'zPz-ogLUbqA'], 'ChildishGambinoVEVO': ['VYOjWnS4cMY']}, {'G36BAjlL3pw': ((18, 6, 12), 2090150, 22799, 1241), 'UwbO_xb1-Xo': ((18, 3, 25), 661775, 0, 0), 'VYOjWnS4cMY': ((18, 5, 13), 98938809, 3037318, 161813), 'nlozE2m-NMc': ((18, 6, 12), 3306528, 66034, 749), 'zPz-ogLUbqA': ((18, 3, 31), 565464, 0, 0)})
    >>> sevenlines.close()
    """
    # TODO: complete this function according to the documentation given
    
    youtube_video_data_list = file_handle.readlines()
    file_handle.close() 
    
    id_title    = {}
    channel_ids = {}
    id_stats    = {}
    
    num_videos = len(youtube_video_data_list)
    
    for index in range(1, num_videos):
        
        #makes list of video data
        video = youtube_video_data_list[index].split(',')
        
        #Returns video information
        youtube_id, title, channel, trend_date, views, likes, dislikes = get_video_info(video)
        
        #formats date
        new_date = to_date(trend_date)
        
        #appends id_stats dictionary and keep most recent stats for each video
        get_recent_stats(youtube_id, new_date, views, likes, dislikes, id_stats)
                
        #appends id_title dictionary
        id_title[youtube_id] = title
        
        #appends channel_ids and adds id to channel it belongs 
        get_channel_ids(youtube_id, channel, channel_ids)

            
    #puts dictionaries into tuple
    youtube_video_data = (id_title, channel_ids, id_stats)
    
    return youtube_video_data

def get_type_stat(stat: str) -> int:
    '''
    returns type of stat
    
    Precondition: stat can only be 'views', 'likes', 'dislikes', 'date'
    
    >>> get_type_stat('views')
    1
    >>> get_type_stat('likes')
    2
    >>> get_type_stat('dislikes')
    3
    >>> get_type_stat('date')
    0
    '''
    #if stat argument is views use position 1
    if stat == 'views':
        stat_type = 1
    #if stat argument is likes use position 2
    elif stat == 'likes':
        stat_type = 2
    #if stat argument is dislikes use position 3
    elif stat == 'dislikes':
        stat_type = 3
    #if stat argument is date use position 3
    else:
        stat_type = 0
        
    return stat_type

def get_chan_vids_w_term(id_title: Dict[str, str], chan_vids_ids: List[str], terms: List[str]) -> List[str]:
    '''
    looks for videos with searched terms in channel's videos and returns video 
    ids as list
    
    - id_title: Dict[YouTube id, video title]
    '''
    
    chan_vids_w_term = [] #channel videos with term
    
    num_terms  = len(terms)
    index = 0
    
    # goes through each video of channel
    for youtube_id in chan_vids_ids:
        title = id_title[youtube_id]
        
        #sees if a term is in title
        while index < num_terms:
            term = terms[index]
            index += 1
            
            #if term is in title, append channel videos with term
            if term.lower() in title.lower():
                chan_vids_w_term.append(youtube_id)
                index = num_terms
                
        index = 0  
        
    return chan_vids_w_term

def get_highest_stat_vids(id_stats: Dict[str, VideoStats], chan_vids_w_term: List[str], stat_type: int) -> List[str]:
    '''
    looks for highest stat videos of chan_vids_w_term and returns video ids 
    as list
    
    - id_stats: Dict[YouTube id, latest video stat]
    '''
    
    highest_stat_vids  = []
    
    recent_date = (0, 0, 0)
    max_stat = 0    
    
    #goes through each youtube id of chan_vids_w_term
    for youtube_id in chan_vids_w_term:
        stats = id_stats[youtube_id]
        
        #if stat is not date
        if stat_type != INPUT_TRENDING_DT - 1:
            stat = stats[stat_type]
            
            #if stat is greater than max stat, then reset and append highest_stat_vids
            if stat > max_stat:
                max_stat = stats[stat_type]
                
                highest_stat_vids = []
                highest_stat_vids.append(youtube_id)
                
            #if stat is equal to max stat, then append highest_stat_vids
            elif stats[stat_type] == max_stat:
                highest_stat_vids.append(youtube_id)
        
        #if stat is date
        else:
            new_date = stats[stat_type]
            
            #if new date is more recent than recent_date, then reset and append highest_stat_vids
            if get_recent(new_date, recent_date) == True:
                recent_date = stats[stat_type]
                
                highest_stat_vids = []
                highest_stat_vids.append(youtube_id)
                
            #if new date is just as recent as recent_date, then append highest_stat_vids
            elif get_recent(new_date, recent_date) == 'both':
                highest_stat_vids.append(youtube_id) 
                
    return highest_stat_vids

def get_youtube_ids(filename: str, channel: str, terms: List[str], stat: str
                    ) -> List[str]:
    """ returns a list of sorted YouTube ids of only those YouTube videos that 
    - are on the given channel
    - contain at LEAST ONE of the given terms
    - have the highest given stat where stat is one of the following strings:
    'date', 'views', 'likes' or 'dislikes'
    
    You MUST call file_to_dicts and use look ups in the returned dictionaries 
    to help solve this problem in order to receive marks.
    You can and should design additional helper functions to solve this problem.
    
    >>> get_youtube_ids('EmptyFile.csv', 'Austin Evans', ['fortnite'], 'likes')
    []
    
    >>> get_youtube_ids('SevenLines.csv', 'Austin Evans', [], 'likes')
    []
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West', [], 'likes')
    []
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West',\
    ['not there', 'not either'], 'dislikes')
    []
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West',\
    ['beauty', 'not there', 'not there either'], 'date')
    ['UwbO_xb1-Xo']
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West',\
    ['not there', 'beauty', 'not there either'], 'likes')
    ['UwbO_xb1-Xo']
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West',\
    ['not there there', 'not either', 'beauty'], 'dislikes')
    ['UwbO_xb1-Xo']
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West',\
    ['mario', 'not there', 'beauty'], 'views')
    ['UwbO_xb1-Xo']
    
    >>> get_youtube_ids('SevenLines.csv', 'Kim Kardashian West',\
    ['mario', 'beauty', 'not there'], 'dislikes')
    ['UwbO_xb1-Xo', 'zPz-ogLUbqA']
    
    >>> get_youtube_ids('SevenLines.csv', 'The Late Show with Stephen Colbert',\
    ['Trump', 'DEADPOOL'], 'dislikes')
    ['G36BAjlL3pw']
    
    >>> get_youtube_ids('SevenLines.csv', 'The Late Show with Stephen Colbert',\
    ['Trump', 'DEADPOOL'], 'likes')
    ['nlozE2m-NMc']
    
    >>> get_youtube_ids('SevenLines.csv', 'The Late Show with Stephen Colbert',\
    ['Trump', 'DEADPOOL'], 'date')
    ['G36BAjlL3pw', 'nlozE2m-NMc']
    
    >>> get_youtube_ids('CAvideos.csv', 'Saturday Night Live',\
    ['Pete Davidson', 'cut for time'], 'date')
    ['WeX5VO0aXS0']
    
    >>> get_youtube_ids('CAvideos.csv', 'Austin Evans',\
    ['fortnite', 'laptop'], 'views')
    ['3f8ovcPu6Qk']
    
    >>> get_youtube_ids('CAvideos.csv', 'Kim Kardashian West',\
    ['tutorial', 'beauty'], 'likes')
    ['UwbO_xb1-Xo', 'uETlOZViR7o']
    
    >>> get_youtube_ids('CAvideos.csv', 'The Late Show with Stephen Colbert',\
    ['trump', 'election'], 'dislikes')
    ['EsaHiIdsKpE']
    
    >>> get_youtube_ids('CAvideos.csv', 'The Late Show with Stephen Colbert',\
    ['trump', 'election'], 'date')
    ['UVxE_MM94tA']
    """
    # TODO: complete this function according to the documentation given
    
    file_handle = open(filename, 'r', encoding = 'utf-8')
    
    youtube_video_data = file_to_dicts(file_handle)
    file_handle.close()
    
    #gets dictionaries
    id_title    = youtube_video_data[0]
    channel_ids = youtube_video_data[1]
    id_stats    = youtube_video_data[2]
    
    #gets type of stat
    stat_type = get_type_stat(stat)
    
    chan_vids_ids = [] #channel videos' ids
    
    #gets videos of searched channel
    if channel in channel_ids:
        chan_vids_ids = channel_ids[channel]
    
    #looks for videos with searched terms in channel's videos
    chan_vids_w_term = get_chan_vids_w_term(id_title, chan_vids_ids, terms)
    
    #looks for highest stat videos of chan_vids_w_term
    searched_video_ids = get_highest_stat_vids(id_stats, chan_vids_w_term, stat_type)
    
    searched_video_ids.sort()
    
    return searched_video_ids