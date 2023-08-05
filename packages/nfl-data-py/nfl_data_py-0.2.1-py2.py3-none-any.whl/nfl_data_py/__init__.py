name = 'nfl_data_py'

import pandas
import numpy
import datetime
import appdirs

# module level doc string
__doc__ = """
nfl_data_py - a Python package for working with NFL data
=========================================================

**nfl_data_py** is a Python package that streamlines the importing
of a variety of different American football datasets. It also includes
tables to assist with the merging of datasets from various sources.

Functions
---------
import_pbp_data() - import play-by-play data
import_weekly_data() - import weekly player stats
import_seasonal_data() - import seasonal player stats
import_snap_counts() - import weekly snap count stats
import_ngs_data() - import NGS advanced analytics
import_qbr() - import QBR for NFL or college
import_pfr_passing() - import advanced passing stats from PFR
import_officials() - import details on game officials
import_schedules() - import weekly teams schedules
import_rosters() - import team rosters
import_depth_charts() - import team depth charts
import_injuries() - import team injury reports
import_ids() - import mapping of player ids for more major sites
import_win_totals() - import win total lines for teams
import_sc_lines() - import weekly betting lines for teams
import_draft_picks() - import draft pick history
import_draft_values() - import draft value models by pick
import_combine_data() - import combine stats
see_pbp_cols() - return list of play-by-play columns
see_weekly_cols() - return list of weekly stat columns
import_team_desc() - import descriptive data for team viz
clean_nfl_data() - clean df by aligning common name diffs
"""


def import_pbp_data(years, columns=None, downcast=True, cache=False, alt_path=None):
    """Imports play-by-play data
    
    Args:
        years (List[int]): years to get PBP data for
        columns (List[str]): only return these columns
        downcast (bool): convert float64 to float32, default True
        cache (bool): whether to use local cache as source of pbp data
        alt_path (str): path for cache if not nfl_data_py default
    Returns:
        DataFrame
    """
    
    # check variable types
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
        
    if min(years) < 1999:
        raise ValueError('Data not available before 1999.')
    
    if columns is None:
        columns = []
       
    # potential sources for pbp data
    url1 = r'https://github.com/nflverse/nflfastR-data/raw/master/data/play_by_play_'
    url2 = r'.parquet'
    appname = 'nfl_data_py'
    appauthor = 'cooper_dff'
    
    plays = pandas.DataFrame()

    # read in pbp data
    for year in years:
        
        # define path based on cache and alt_path variables
        if cache is True:
            if alt_path is None:
                alt_path = ''
                path = appdirs.user_cache_dir(appname, appauthor) + '\\pbp'
            else:
                url = alt_path
        else:
            path = url1 + str(year) + url2

        # load data
        try:
            if len(columns) != 0:
                data = pandas.read_parquet(path, columns=columns, engine='auto')
            else:
                data = pandas.read_parquet(path, engine='auto')
            
            raw = pandas.DataFrame(data)
            raw['season'] = year

            if len(plays) == 0:
                plays = raw
            else:
                plays = plays.append(raw)
            
            print(str(year) + ' done.')
            
        except:
            print('Data not available for ' + str(year))
    
    # converts float64 to float32, saves ~30% memory
    if downcast:
        print('Downcasting floats.')
        cols = plays.select_dtypes(include=[numpy.float64]).columns
        plays.loc[:, cols] = plays.loc[:, cols].astype(numpy.float32)
            
    return plays


def cache_pbp(years, downcast=True, alt_path=None):
    """Cache pbp data in local location to allow for faster loading
    
    Args:
        years (List[int]): years to cache PBP data for
        downcast (bool): convert float64 to float32, default True
        alt_path (str): path for cache if not nfl_data_py default
    Returns:
        DataFrame
    """
    
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
        
    if min(years) < 1999:
        raise ValueError('Data not available before 1999.')
    
    if alt_path is None:
        alt_path = ''
    
    plays = pandas.DataFrame()

    url1 = r'https://github.com/nflverse/nflfastR-data/raw/master/data/play_by_play_'
    url2 = r'.parquet'
    appname = 'nfl_data_py'
    appauthor = 'cooper_dff'
    
    # define path for caching
    if len(alt_path) > 0:
        path = alt_path
    else:
        path = appdirs.user_cache_dir(appname, appauthor) + '\\pbp'

    # read in pbp data
    for year in years:

        try:

            data = pandas.read_parquet(url1 + str(year) + url2, engine='auto')

            raw = pandas.DataFrame(data)
            raw['season'] = year

            if downcast:
                cols = raw.select_dtypes(include=[numpy.float64]).columns
                raw.loc[:, cols] = raw.loc[:, cols].astype(numpy.float32)

            # write parquet to path, partitioned by season
            raw.to_parquet(path, partition_cols='season')

            print(str(year) + ' done.')

        except:
            next
            

def import_weekly_data(years, columns=None, downcast=True):
    """Imports weekly player data
    
    Args:
        years (List[int]): years to get weekly data for
        columns (List[str]): only return these columns
        downcast (bool): convert float64 to float32, default True
    Returns:
        DataFrame
    """
    
    # check variable types
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
        
    if min(years) < 1999:
        raise ValueError('Data not available before 1999.')
    
    if columns is None:
        columns = []
        
    # read weekly data
    data = pandas.read_parquet(r'https://github.com/nflverse/nflfastR-data/raw/master/data/player_stats.parquet', engine='auto')
    data = data[data['season'].isin(years)]

    if len(columns) > 0:
        data = data[columns]

    # converts float64 to float32, saves ~30% memory
    if downcast:
        print('Downcasting floats.')
        cols = data.select_dtypes(include=[numpy.float64]).columns
        data.loc[:, cols] = data.loc[:, cols].astype(numpy.float32)

    return data


def import_seasonal_data(years, s_type='REG'):
    """Imports seasonal player data
    
    Args:
        years (List[int]): years to get seasonal data for
        s_type (str): season type to include in average ('ALL','REG','POST')
    Returns:
        DataFrame
    """
    
    # check variable types
    if not isinstance(years, (list, range)):
        raise ValueError('years input must be list or range.')
        
    if min(years) < 1999:
        raise ValueError('Data not available before 1999.')
        
    if s_type not in ('REG','ALL','POST'):
        raise ValueError('Only REG, ALL, POST allowed for s_type.')
    
    # import weekly data
    data = pandas.read_parquet(r'https://github.com/nflverse/nflfastR-data/raw/master/data/player_stats.parquet', engine='auto')
    
    # filter to appropriate season_type
    if s_type == 'ALL':
        data = data[data['season'].isin(years)]
        
    else:
        data = data[(data['season'].isin(years)) & (data['season_type'] == s_type)]
    
    # calc per game stats
    pgstats = data[['recent_team', 'season', 'week', 'attempts', 'completions', 'passing_yards', 'passing_tds',
                      'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs',
                      'fantasy_points_ppr']].groupby(
        ['recent_team', 'season', 'week']).sum().reset_index()
    pgstats.columns = ['recent_team', 'season', 'week', 'atts', 'comps', 'p_yds', 'p_tds', 'p_ayds', 'p_yac', 'p_fds',
                       'ppr_pts']
    all_stats = data[
        ['player_id', 'player_name', 'recent_team', 'season', 'week', 'carries', 'rushing_yards', 'rushing_tds',
         'rushing_first_downs', 'rushing_2pt_conversions', 'receptions', 'targets', 'receiving_yards', 'receiving_tds',
         'receiving_air_yards', 'receiving_yards_after_catch', 'receiving_first_downs', 'receiving_epa',
         'fantasy_points_ppr']].merge(pgstats, how='left', on=['recent_team', 'season', 'week']).fillna(0)
    season_stats = all_stats.drop(['recent_team', 'week'], axis=1).groupby(
        ['player_id', 'player_name', 'season']).sum().reset_index()

    # calc custom receiving stats
    season_stats['tgt_sh'] = season_stats['targets'] / season_stats['atts']
    season_stats['ay_sh'] = season_stats['receiving_air_yards'] / season_stats['p_ayds']
    season_stats['yac_sh'] = season_stats['receiving_yards_after_catch'] / season_stats['p_yac']
    season_stats['wopr'] = season_stats['tgt_sh'] * 1.5 + season_stats['ay_sh'] * 0.8
    season_stats['ry_sh'] = season_stats['receiving_yards'] / season_stats['p_yds']
    season_stats['rtd_sh'] = season_stats['receiving_tds'] / season_stats['p_tds']
    season_stats['rfd_sh'] = season_stats['receiving_first_downs'] / season_stats['p_fds']
    season_stats['rtdfd_sh'] = (season_stats['receiving_tds'] + season_stats['receiving_first_downs']) / (
                season_stats['p_tds'] + season_stats['p_fds'])
    season_stats['dom'] = (season_stats['ry_sh'] + season_stats['rtd_sh']) / 2
    season_stats['w8dom'] = season_stats['ry_sh'] * 0.8 + season_stats['rtd_sh'] * 0.2
    season_stats['yptmpa'] = season_stats['receiving_yards'] / season_stats['atts']
    season_stats['ppr_sh'] = season_stats['fantasy_points_ppr'] / season_stats['ppr_pts']

    data.drop(['recent_team', 'week'], axis=1, inplace=True)
    szn = data.groupby(['player_id', 'player_name', 'season', 'season_type']).sum().reset_index().merge(
        data[['player_id', 'season', 'season_type']].groupby(['player_id', 'season']).count().reset_index().rename(
            columns={'season_type': 'games'}), how='left', on=['player_id', 'season'])

    szn = szn.merge(season_stats[['player_id', 'season', 'tgt_sh', 'ay_sh', 'yac_sh', 'wopr', 'ry_sh', 'rtd_sh',
                                  'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh']], how='left',
                    on=['player_id', 'season'])

    return szn


def see_pbp_cols():
    """Identifies list of columns in pbp data
    
    Returns:
        list
    """
    
    # load pbp file, identify columns
    data = pandas.read_parquet(r'https://github.com/nflverse/nflfastR-data/raw/master/data/play_by_play_2020.parquet', engine='auto')
    cols = data.columns

    return cols


def see_weekly_cols():
    """Identifies list of columns in weekly data
    
    Returns:
        list
    """
    
    # load weekly file, identify columns
    data = pandas.read_parquet(r'https://github.com/nflverse/nflfastR-data/raw/master/data/player_stats.parquet', engine='auto')
    cols = data.columns

    return cols


def import_rosters(years, columns=None):
    """Imports roster data
    
    Args:
        years (List[int]): years to get rosters for
        columns (List[str]): list of columns to return with DataFrame
        
    Returns:
        DataFrame
    """

    # check variable types
    if not isinstance(years, (list, range)):
        raise ValueError('years input must be list or range.')

    if min(years) < 1999:
        raise ValueError('Data not available before 1999.')

    if columns is None:
        columns = []

    rosters = []

    # imports rosters for specified years
    for y in years:
        temp = pandas.read_csv(r'https://github.com/mrcaseb/nflfastR-roster/blob/master/data/seasons/roster_' + str(y)
                               + '.csv?raw=True', low_memory=False)
        rosters.append(temp)

    rosters = pandas.DataFrame(pandas.concat(rosters)).rename(
        columns={'full_name': 'player_name', 'gsis_id': 'player_id'})
    rosters.drop_duplicates(subset=['season', 'player_name', 'position', 'player_id'], keep='first', inplace=True)

    if len(columns) > 0:
        rosters = rosters[columns]

    # define function for calculating age in season and then calculate
    def calc_age(x):
        ca = pandas.to_datetime(x[0])
        bd = pandas.to_datetime(x[1])
        return ca.year - bd.year + numpy.where(ca.month > bd.month, 0, -1)

    if 'birth_date' in columns and 'current_age' in columns:
    
        rosters['current_age'] = rosters['season'].apply(lambda x: datetime.datetime(int(x), 9, 1))
        rosters['age'] = rosters[['current_age', 'birth_date']].apply(calc_age, axis=1)
        rosters.drop(['current_age'], axis=1, inplace=True)
        rosters.dropna(subset=['player_id'], inplace=True)

    return rosters


def import_team_desc():
    """Import team descriptive data
    
    Returns:
        DataFrame
    """
    
    # import desc data
    df = pandas.read_csv(r'https://github.com/nflverse/nflfastR-data/raw/master/teams_colors_logos.csv')
    
    return df


def import_schedules(years):
    """Import schedules
    
    Args:
        years (List[int]): years to get schedules for
        
    Returns:
        DataFrame
    """
    
    # check variable types
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
    
    if min(years) < 1999:
        raise ValueError('Data not available before 1999.')
    
    scheds = pandas.DataFrame()
    
    # import schedule for specified years
    scheds = pandas.read_csv(r'http://www.habitatring.com/games.csv')    
    scheds = scheds[scheds['season'].isin(years)]
        
    return scheds
    

def import_win_totals(years):
    """Import win total projections
    
    Args:
        years (List[int]): years to get win totals for
        
    Returns:
        DataFrame
    """

    # check variable types
    if not isinstance(years, (list, range)):
        raise ValueError('years variable must be list or range.')
    
    # import win totals
    df = pandas.read_csv(r'https://raw.githubusercontent.com/nflverse/nfldata/master/data/win_totals.csv')
    
    df = df[df['season'].isin(years)]
    
    return df
    

def import_officials(years=None):
    """Import game officials
    
    Args:
        years (List[int]): years to get officials for
        
    Returns:
        DataFrame
    """

    # check variable types
    if years is None:
        years = []
    
    if not isinstance(years, (list, range)):
        raise ValueError('years variable must be list or range.')

    # import officials data
    df = pandas.read_csv(r'https://raw.githubusercontent.com/nflverse/nfldata/master/data/officials.csv')
    df['season'] = df['game_id'].str[0:4].astype(int)
    
    if len(years) > 0:
        df = df[df['season'].isin(years)]
    
    return df
    
    
def import_sc_lines(years=None):
    """Import weekly scoring lines
    
    Args:
        years (List[int]): years to get scoring lines for
       
    Returns:
        DataFrame
    """

    # check variable types
    if years is None:
        years = []
    
    if not isinstance(years, (list, range)):
        raise ValueError('years variable must be list or range.')
    
    # import data
    df = pandas.read_csv(r'https://raw.githubusercontent.com/nflverse/nfldata/master/data/sc_lines.csv')
    
    if len(years) > 0:
        df = df[df['season'].isin(years)]
    
    return df
    
    
def import_draft_picks(years=None):
    """Import draft picks
    
    Args:
        years (List[int]): years to get draft picks for
    
    Returns:
        DataFrame
    """

    # check variable types
    if years is None:
        years = []
    
    if not isinstance(years, (list, range)):
        raise ValueError('years variable must be list or range.')

    # import draft pick data
    df = pandas.read_csv(r'https://raw.githubusercontent.com/nflverse/nfldata/master/data/draft_picks.csv')
    
    if len(years) > 0:
        df = df[df['season'].isin(years)]  
    
    return df
    

def import_draft_values(picks=None):
    """Import draft pick values from variety of models
    
    Args:
        picks (List[int]): subset of picks to return values for
        
    Returns:
        DataFrame
    """

    # check variable types
    if picks is None:
        picks = []
    
    if not isinstance(picks, (list, range)):
        raise ValueError('picks variable must be list or range.')

    # import data
    df = pandas.read_csv(r'https://raw.githubusercontent.com/nflverse/nfldata/master/data/draft_values.csv')

    if len(picks) > 0:
        df = df[df['pick'].between(picks[0], picks[-1])]

    return df      


def import_combine_data(years=None, positions=None):
    """Import combine results for all position groups
    
    Args:
        years (List[str]): years to get combine data for
        positions (List[str]): list of positions to get data for
        
    Returns:
        DataFrame
    """
    
    # check variable types
    if years is None:
        years = []
        
    if positions is None:
        positions = []
        
    if not isinstance(years, (list, range)):
        raise ValueError('years variable must be list or range.')
        
    if not isinstance(positions, list):
        raise ValueError('positions variable must be list.')
        
    # import data
    df = pandas.read_csv(r'https://raw.githubusercontent.com/cooperdff/nfl_data_py/main/data/combine.csv')
    
    # filter to years and positions
    if len(years) > 0 and len(positions) > 0:
        df = df[(df['season'].isin(years)) & (df['position'].isin(positions))]
    elif len(years) > 0:
        df = df[df['season'].isin(years)]
    elif len(positions) > 0:
        df = df[df['position'].isin(positions)]

    return df    


def import_ids(columns=None, ids=None):
    """Import mapping table of ids for most major data providers
    
    Args:
        columns (List[str]): list of columns to return
        ids (List[str]): list of specific ids to return
        
    Returns:
        DataFrame
    """
    
    # create list of id options
    avail_ids = ['mfl_id', 'sportradar_id', 'fantasypros_id', 'gsis_id', 'pff_id',
       'sleeper_id', 'nfl_id', 'espn_id', 'yahoo_id', 'fleaflicker_id',
       'cbs_id', 'rotowire_id', 'rotoworld_id', 'ktc_id', 'pfr_id',
       'cfbref_id', 'stats_id', 'stats_global_id', 'fantasy_data_id']
    avail_sites = [x[:-3] for x in avail_ids]
    
    # check variable types
    if columns is None:
        columns = []
    
    if ids is None:
        ids = []

    if not isinstance(columns, list):
        raise ValueError('columns variable must be list.')
        
    if not isinstance(ids, list):
        raise ValueError('ids variable must be list.')
        
    # confirm id is in table
    if False in [x in avail_sites for x in ids]:
        raise ValueError('ids variable can only contain ' + ', '.join(avail_sites))
        
    # import data
    df = pandas.read_csv(r'https://raw.githubusercontent.com/dynastyprocess/data/master/files/db_playerids.csv')
    
    rem_cols = [x for x in df.columns if x not in avail_ids]
    tgt_ids = [x + '_id' for x in ids]
        
    # filter df to just specified columns
    if len(columns) > 0 and len(ids) > 0:
        df = df[set(tgt_ids + columns)]
    elif len(columns) > 0 and len(ids) == 0:
        df = df[set(avail_ids + columns)]
    elif len(columns) == 0 and len(ids) > 0:
        df = df[set(tgt_ids + rem_cols)]
    
    return df
    
    
def import_ngs_data(stat_type, years=None):
    """Imports seasonal NGS data
    
    Args:
        stat_type (str): type of stats to pull (receiving, passing, rushing)
        years (List[int]): years to get PBP data for, optional
    Returns:
        DataFrame
    """
    
    # check variable types
    if years is None:
        years = []
        
    if stat_type not in ('receiving','passing','rushing'):
        raise ValueError('stat_type must be one of receiving, passing, rushing.')
        
    if not isinstance(years, (list, range)):
        raise ValueError('years variable must be list or range.')
    
    # import data
    url = r'https://github.com/nflverse/ngs-data/raw/main/data/ngs_{}.csv.gz'
    url = url.format(stat_type)
    
    data = pandas.read_csv(url)
    
    # filter if years varaible provided
    if len(years) > 0:
        data = data[data['season'].between(min(years), max(years))]
        
    # return
    return data
    

def import_depth_charts(years=None):
    """Imports team depth charts
    
    Args:
        years (List[int]): years to return depth charts for, optional
    Returns:
        DataFrame
    """

    # check variable types
    if years is None:
        years = []
        
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
    
    if len(years) > 0:
        if min(years) < 2001:
            raise ValueError('Data not available before 2001.')
    
    # import data
    url = r'https://github.com/nflverse/nflfastR-roster/blob/master/data/nflfastR-depth_charts.csv.gz?raw=True'

    df = pandas.read_csv(url, compression='gzip')
            
    # filter to desired years
    if len(years) > 0:
        df = df[df['season'].between(min(years), max(years))]
    
    return df
    

def import_injuries(years=None):
    """Imports team injury reports
    
    Args:
        years (List[int]): years to return injury reports for, optional
    Returns:
        DataFrame
    """

    # check variable types
    if years is None:
        years = []
        
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
    
    if len(years) > 0:
        if min(years) < 2009:
            raise ValueError('Data not available before 2009.')
    
    #import data
    url = r'https://github.com/nflverse/nflfastR-roster/blob/master/data/nflfastR-injuries.csv.gz?raw=True'

    df = pandas.read_csv(url, low_memory=False, compression='gzip')
    
    # filter to relevant years
    if len(years) > 0:
        df = df[df['season'].between(min(years), max(years))]
    
    return df
    

def import_qbr(years=None, level='nfl', frequency='season'):
    """Import NFL or college QBR data
    
    Args:
        years (List[int]): list of years to return data for, optional
        level (str): level to pull data, nfl or college, default to nfl
        frequency (str): frequency to pull data, weekly or season, default to season
    Returns:
        DataFrame
    """

    # check variable types and specifics
    if years is None:
        years = []
        
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
    
    if len(years) > 0:
        if min(years) < 2006:
            raise ValueError('Data not available before 2006.')
    
    if level not in ('nfl','college'):
        raise ValueError('level must be nfl or college')
        
    if frequency not in ('season','weekly'):
        raise ValueError('frequency must be season or weekly')
    
    # import data
    url = r'https://raw.githubusercontent.com/nflverse/espnscrapeR-data/master/data/qbr-{}-{}.csv'.format(level, frequency)

    df = pandas.read_csv(url)
            
    # filter to desired years
    if len(years) > 0:
        df = df[df['season'].between(min(years), max(years))]
    
    return df
    
    
def import_pfr_passing(years=None):
    """Import PFR advanced passing statistics
    
    Args:
        years (List[int]): years to return data for, optional
    Returns:
        DataFrame
    """

    # check variables types
    if years is None:
        years = []
        
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
    
    if len(years) > 0:
        if min(years) < 2019:
            raise ValueError('Data not available before 2019.')
    
    # import data
    url = r'https://raw.githubusercontent.com/nflverse/pfr_scrapR/master/data/pfr_advanced_passing.csv'

    df = pandas.read_csv(url)
            
    # filter to desired years
    if len(years) > 0:
        df = df[df['season'].between(min(years), max(years))]
    
    return df
    
    
def import_snap_counts(years):
    """Import snap count data for individual players
    
    Args:
        years (List[int]): years to return snap counts for
    Returns:
        DataFrame
    """

    # check variables types
    if years is None:
        years = []
        
    if not isinstance(years, (list, range)):
        raise ValueError('Input must be list or range.')
    
    if len(years) > 0:
        if min(years) < 2013:
            raise ValueError('Data not available before 2013.')
    
    df = pandas.DataFrame()
    
    # import data
    for yr in years:
        
        url = r'https://raw.githubusercontent.com/nflverse/pfr_scrapR/master/data/snap_counts_{}.csv'.format(yr)

        temp = pandas.read_csv(url)
            
        if len(df) > 0:
            df = df.append(temp)
        else:
            df = temp.copy()
    
    return df

    
def clean_nfl_data(df):
    """Cleans descriptive data for players and teams to help with consistency across datasets
    
    Args:
        df (DataFrame): DataFrame to be cleaned
        
    Returns:
        DataFrame
    """

    name_repl = {
        'Gary Jennings Jr': 'Gary Jennings',
        'DJ Chark': 'D.J. Chark',
        'Cedrick Wilson Jr.': 'Cedrick Wilson',
        'Deangelo Yancey': 'DeAngelo Yancey',
        'Ardarius Stewart': 'ArDarius Stewart',
        'Calvin Johnson  HOF': 'Calvin Johnson',
        'Mike Sims-Walker': 'Mike Walker',
        'Kenneth Moore': 'Kenny Moore',
        'Devante Parker': 'DeVante Parker',
        'Brandon Lafell': 'Brandon LaFell',
        'Desean Jackson': 'DeSean Jackson',
        'Deandre Hopkins': 'DeAndre Hopkins',
        'Deandre Smelter': 'DeAndre Smelter',
        'William Fuller': 'Will Fuller',
        'Lavon Brazill': 'LaVon Brazill',
        'Devier Posey': 'DeVier Posey',
        'Demarco Sampson': 'DeMarco Sampson',
        'Deandrew Rubin': 'DeAndrew Rubin',
        'Latarence Dunbar': 'LaTarence Dunbar',
        'Jajuan Dawson': 'JaJuan Dawson',
        "Andre' Davis": 'Andre Davis',
        'Johnathan Holland': 'Jonathan Holland',
        'Johnnie Lee Higgins Jr.': 'Johnnie Lee Higgins',
        'Marquis Walker': 'Marquise Walker',
        'William Franklin': 'Will Franklin',
        'Ted Ginn Jr.': 'Ted Ginn',
        'Jonathan Baldwin': 'Jon Baldwin',
        'T.J. Graham': 'Trevor Graham',
        'Odell Beckham Jr.': 'Odell Beckham',
        'Michael Pittman Jr.': 'Michael Pittman',
        'DK Metcalf': 'D.K. Metcalf',
        'JJ Arcega-Whiteside': 'J.J. Arcega-Whiteside',
        'Lynn Bowden Jr.': 'Lynn Bowden',
        'Laviska Shenault Jr.': 'Laviska Shenault',
        'Henry Ruggs III': 'Henry Ruggs',
        'KJ Hamler': 'K.J. Hamler',
        'KJ Osborn': 'K.J. Osborn',
        'Devonta Smith': 'DeVonta Smith',
        'Terrace Marshall Jr.': 'Terrace Marshall',
        "Ja'Marr Chase": 'JaMarr Chase'
    }

    col_tm_repl = {
        'Ole Miss': 'Mississippi',
        'Texas Christian': 'TCU',
        'Central Florida': 'UCF',
        'Bowling Green State': 'Bowling Green',
        'West. Michigan': 'Western Michigan',
        'Pitt': 'Pittsburgh',
        'Brigham Young': 'BYU',
        'Texas-El Paso': 'UTEP',
        'East. Michigan': 'Eastern Michigan',
        'Middle Tenn. State': 'Middle Tennessee State',
        'Southern Miss': 'Southern Mississippi',
        'Louisiana State': 'LSU'
    }

    pro_tm_repl = {
        'GNB': 'GB',
        'KAN': 'KC',
        'LA': 'LAR',
        'LVR': 'LV',
        'NWE': 'NE',
        'NOR': 'NO',
        'SDG': 'SD',
        'SFO': 'SF',
        'TAM': 'TB'
    }
    
    na_replace = {
        'NA':numpy.nan
    }

    for col in df.columns:
        df.replace({col:na_replace}, inplace=True)

    if 'name' in df.columns:
        df.replace({'name': name_repl}, inplace=True)

    if 'col_team' in df.columns:
        df.replace({'col_team': col_tm_repl}, inplace=True)

        if 'name' in df.columns:
            for z in player_col_tm_repl:
                df[df['name'] == z[0]] = df[df['name'] == z[0]].replace({z[1]: z[2]})

    return df
