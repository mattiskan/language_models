import requests
import urllib.parse
import re
import os
from os import listdir
import json
from nltk.tokenize import sent_tokenize
from gevent.pool import Pool

from pyquery import PyQuery


DEBUG = os.environ.get('DEBUG', False)


CONNECTION_LIMIT = 10
adapter = requests.adapters.HTTPAdapter(pool_connections=CONNECTION_LIMIT, 
                                        pool_maxsize=CONNECTION_LIMIT)


with open('keys.json', 'r') as rfile:
    keys = json.load(rfile)
    GOOGLE_API_KEY = keys['GOOGLE_API_KEY']
    CX = keys['GOOGLE_CX']

def crawl_times():
    session = requests.session()
    session.mount('http://', adapter)

    # or do your work with gevent
    
    gevent_pool = Pool(10)

    try:
        with open('data/crawler_raw_responses/time.com/google_next_index.int', 'r') as rfile:
            start_index = rfile.read()
            assert int(start_index)
    except:
        start_index = 0
                

    q = 'donald+trump+transcripts+full+text+site%3Atime.com'
    
    google_search_url = f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={CX}&q={q}'

    google_response = session.get(google_search_url + (f'&start={start_index}' if start_index else ''))

    try:
        while True:
            search_response = json.loads(google_response.text)
            
            try:
                start_index = search_response['queries']['nextPage'][0]['startIndex']
            except KeyError:
                import ipdb; ipdb.set_trace()

            assert int(start_index)

            with open('data/crawler_raw_responses/time.com/google_next_index.int', 'w') as wfile:
                wfile.write(str(start_index))
            
            
            for item in search_response['items']:
                url = item['link']
                
                link_id = url.split('/')[-3]
                assert int(link_id)
            
                if os.path.isfile(f'data/crawler_raw_responses/time.com/{link_id}'):
                    print(f'already fetched: {url}')
                    continue
            
                pool.spawn(fetch_transcript, url, session)

            with open('data/crawler_raw_responses/time.com/last_search_response.json', 'w') as wfile:
                wfile.write(google_response.text)

                
            google_response = session.get(google_search_url + f'&start={start_index}')
    except KeyboardInterrupt:
        print('waiting for scrapers to stop')
        gevent_pool.join()



def fetch_transcript(url, session):
    print(f'fetching {url}')
    
    response = session.get(url)

    if response.status_code != 200:
        print(f'unexpected status code: {response.status_code}')
        return []

    link_id = url.split('/')[-3]
    assert int(link_id)
    with open(f'data/crawler_raw_responses/time.com/{link_id}', 'w') as wfile:
        wfile.write(response.text)


def parse_transcript_basic(rfile):
    pq = PyQuery(rfile.read())
    
    if pq('blockquote'):
        text = pq('blockquote').text()
        
        sents = sent_tokenize(text)
        result = Parser.parse_list(sents)
        return result

    # let's start searching for other crap ..
    for script_tag in pq('script'):
        try:
            payload = json.loads(script_tag.text)
            
            if payload.get('articleBody'):
                results = Parser.parse_list(sent_tokenize(payload['articleBody']))

                if results:
                    return results

                # some keywords may hint that the enitre thing is a speech
                keywords = {kw.lower() for kw in payload.get('keywords', [])}
                if all(req in keywords for req in ['donald-trump']):
                    return sent_tokenize(payload['articleBody'])

                if DEBUG:
                    import ipdb; ipdb.set_trace()
                    pass
                else:
                    print('nothing in', rfile.name)

        except json.decoder.JSONDecodeError:
            pass


class Parser(object):

    last_was_trump = False
    new_speaker = re.compile("^.*[A-Z \(\)]+\s?:.*")
    random_crap_pattern = "\([A-Za-z ]+\)"
    random_crap_pattern2 = "\[[A-Za-z ]+\]"
    trump_speaks = re.compile("^\s*T[RUMPrump]+:.*")
    
    @classmethod
    def parse_list(cls, text_list):

        results = []
        for line in text_list:

            before = line[:]
            line = re.sub(cls.random_crap_pattern, '', line)
            
            if before != line and DEBUG:
                print('before', before)
                print('after', line)
                print()
            
            if cls.last_was_trump:
                if cls.new_speaker.match(line):
                    cls.last_was_trump = False
                    continue
    
                results.append(line)
            else:
                if cls.trump_speaks.match(line):
                    cls.last_was_trump = True
                    results.append(line[len('TRUMP:'):])
                    continue
                
        return results


if __name__ == '__main__':
    #crawl_times()

    total = 0
    for fname in ([] or listdir('data/crawler_raw_responses/time.com/')):
        try:
            if int(fname):
                with open('data/crawler_raw_responses/time.com/' + fname, 'r') as rfile:
                    results = parse_transcript_basic(rfile)

                partial = sum(len(sent.split()) for sent in results)
                print(rfile.name)
                total += partial

                with open('data/crawler_responses/time.com/' + fname, 'w') as wfile:
                    wfile.write(json.dumps(results))
        except TypeError:
            pass
    print('read total of', total)
                    




