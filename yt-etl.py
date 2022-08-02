import requests
import pandas as pd
import time, datetime
from datetime import datetime
import snowflake.connector
import configparser
import configparser

today = datetime.now()
today.strftime('%Y-%m-%d')

def get_raw_data(API_KEY: str):
  try: 
    request_url = "https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&chart=mostPopular&regionCode=PL&maxResults=50&key="+API_KEY
  except Exception as e:
    print('Something went wrong with loading data: ', e)
  finally:
    print('Loading raw data finished: ', datetime.now().strftime('%Y-%m-%d'))

  response = requests.get(request_url).json()
  time.sleep(5)
  raw = response

  return raw


def get_data_cleaned(df, raw):
  # get video snippet
  for item in raw["items"]: 
    # if item['kind'] == 'youtube#video':
      video_id = item['id']
      video_title = item['snippet']['title']
      upload_date = str(item['snippet']['publishedAt']).split('T')[0]
      category_id = item['snippet']['categoryId']
      # tags = item['snippet']['tags']
      views_count = item['statistics']['viewCount']
      like_count = item['statistics']['likeCount']
      comment_count = item['statistics']['commentCount']

      append_features = {"video_id":video_id,
                        "video_title" : video_title,
                        'upload_date': upload_date,
                        'view_count': views_count,
                        'like_count': like_count,
                        'comment_count': comment_count,
                        'category_id' : category_id,
                        }

      df = df.append(append_features,
                      ignore_index = True)

  return df


def get_categories(df_cat, API_KEY):
    try: 
        url = 'https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=PL&key='+API_KEY
    except Exception as e:
        print('Something went wrong with loading categories data: ', e)
    finally:
        print('Loading categories finished: ')

    cat_req = requests.get(url).json()
    for item in cat_req['items']: 
        category_id = item['id']
        category_name = item['snippet']['title']

        append_features = {"category_id" : category_id,
                        'category_name' : category_name}

        df_cat = df_cat.append(append_features,  ignore_index = True)
    
    return df_cat


def get_dislikes(df_dis, video_id: str):
    try:
        url = 'https://returnyoutubedislikeapi.com/votes?videoId='+video_id
    except Exception as e:
        print('Something went wrong with loading dislikes data: ', e)

    dis_req = requests.get(url).json()
    for dis in dis_req:
        dislike_count = dis_req['dislikes']
        rating = dis_req['rating'] 
        append_features = {'video_id': video_id,
                           'dislike_count': dislike_count,
                           'rating': rating}

        df_dis = df_dis.append(append_features, ignore_index = True)
      
    return df_dis
        

def merge_datasets(df, df_cat, df_dis):
    df_merged1 = pd.merge(df, df_cat, on = 'category_id')
    df_mergred = pd.merge(df_merged1, df_dis, on = 'video_id')
    # add columns for future data validation check
    df_merged['likes_availability'] = True
    print('Merging datasets finished', today)

    # TBA instead of nulls
    df_merged = df_merged.fillna('TBA')

    return df_merged


def df_to_csv(df): 
    file_csv = 'youtube-api-project/dataset.csv'
    df.to_csv(file_csv, sep=';', encoding='utf-8')

    return file_csv
  
  
  
  
def load(path_to_config, file_path):
  parser = configparser.ConfigParser()
  parser.read(path_to_config)
  username = parser.get('snowflake', 'user')
  password = parser.get('snowflake', 'password')
  account_name = parser.get('snowflake', 'account_name')

  snow_conn = snowflake.connector.connect(
      user = username,
      password = password,
      account = account_name
  )

  sql = '''
      COPY INTO youtube-videos
      FROM @my_s3_stage
        pattern = {file}
  '''.format(file = file_path)

  cur = snow_conn.cursor()
  cur.execute(sql)
  cur.close()


def main():
    # def extract creds
    parser = configparser.ConfigParser()
    parser.read('pipeline.conf')
    API_KEY = parser.get('api', 'youtube-key')
    df = pd.DataFrame(columns = ['video_id', 'video_title', 'upload_date', 'view_count', 'like_count', 'comment_count','category_id',])
    df_dis = pd.DataFrame(columns = ['video_id', 'dislike_count', 'rating'])
    df_cat = pd.DataFrame(columns = ['category_id', 'category_name'])

    raw = get_raw_data(API_KEY = API_KEY)
    df = get_data_cleaned(df =df, raw = raw)
    df_cat = get_categories(df_cat=df_cat, API_KEY=API_KEY)
    for ind in df.index:  
      df_dis = df_dis.append(get_dislikes(df_dis, df['video_id'][ind]))

    df_merged = merge_datasets(df = df, df_cat = df_cat, df_dis = df_dis)
    file_csv = df_to_csv(df = df_merged)
    
    load('pipeline.conf', file_csv)
    
    return file_csv


main()

