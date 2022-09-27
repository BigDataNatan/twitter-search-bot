import json
import os
import datetime as dt
from pathlib import Path
import pandas as pd
from twitter_config import connect_to_endpoint


def search_tweets(search_url, query_params):
    json_response = connect_to_endpoint(search_url, query_params)
    return json_response

def data_lake_raw(json, page, data,hashtag):

    df = pd.json_normalize(json)
    df.reset_index()
    outdir = Path(f'/tmp/search-bot/serasa-prd-raw/year={dt.datetime.today().year}/month={dt.datetime.today().month}/day={dt.datetime.today().day}/hashtag={hashtag[1:]}/page_{page}')
    if os.path.isdir(outdir) == False:
        outdir.mkdir(parents=True, exist_ok=True)

    df.to_csv(f'{outdir}/{data}.csv')

    json = None
    df = None

def main():
    query = os.environ.get("QUERY")
    hashtags = eval(os.environ.get("HASHTAGS"))
    for hashtag in hashtags:
        response = search_tweets("https://api.twitter.com/2/tweets/search/recent", {
                            'query': hashtag + ' ' + query
                            ,'tweet.fields': 'author_id,public_metrics'
                            ,'expansions' : 'author_id'
                            ,'max_results':100})               
        for page in range(10): 
            users = json.dumps(response['includes']['users'], indent=4, sort_keys=True)  
            users_json = json.loads(users) 
            data = json.dumps(response['data'], indent=4, sort_keys=True)  
            data_json = json.loads(data)
            data_lake_raw(users_json[1:], page, 'users',hashtag)
            data_lake_raw(data_json[1:], page, 'data',hashtag)

            try:
                next_token = response['meta']['next_token']
                response = search_tweets("https://api.twitter.com/2/tweets/search/recent?next_token="+next_token, {
                            'query': query
                            ,'tweet.fields': 'author_id'
                            ,'expansions' : 'author_id'
                            ,'max_results':100})
            except:
                break
            
if __name__ == '__main__':
    main()


