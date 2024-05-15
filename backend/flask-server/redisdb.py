import redis
import sys
sys.path.append('../shazam-temalab-2024')
import pipeline 

r = redis.Redis(
  host='redis-12735.c328.europe-west3-1.gce.redns.redis-cloud.com',
  port=12735,
  password='CdosbW224RF30eXdTs6z1F3O5ThPKMln')




def insert(hash,song,artist):
    r.hset(hash, mapping= {
        'song_name' : song,
        'artist' : artist
    })

def getElement(hash):
    return r.hgetall(hash)

def getList(list_of_hashes):
    dict = {}
    for x in list_of_hashes:
      result = getElement(x)
      
      if(result != {}):
         name = result[b'song_name'].decode('ASCII')
         artist = result[b'artist'].decode('ASCII')
         
         if name in dict.keys():
            dict[name][1] +=1
         else:
            dict[name]= [artist,1]
    
    for key in dict:
      
        dict[key][1] = dict[key][1]/len(list_of_hashes)

    return dict  

def insertList(list_of_dicts):
    num = 0
    for dict in list_of_dicts:
        
        print(f"{num}/{len(list_of_dicts)} of songs is done")
        num += 1
        for key in dict:
            insert(key,dict[key][1],dict[key][0])

def getHashListofFile(file_path):
    list = pipeline.pipeline_func_list(file_path)
    return getList(list)



