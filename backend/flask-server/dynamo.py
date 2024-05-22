from decimal import Decimal
import os
import boto3, config, string, random
from boto3.dynamodb.conditions import Key
import sys
sys.path.append('../shazam-temalab-2024')
import pipeline 




dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=config.ACCESS_KEY_ID,
                            aws_secret_access_key=config.ACCESS_SECRET_KEY,
                              region_name=config.REGION)
table = dynamodb.Table('Shazam')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))



def getAll():
   response = table.scan()
   return response["Items"]


    
    



def read(value):
    response = table.get_item(
        Key={ 'hash_value': value
             }
    )
    if 'Item' in response.keys():
      return response['Item']
    else:
       return None



def insert(hash,name,artist):
    item = {
       'hash_value' : hash,
       
       'song_name' :name,
       'artist':artist}
    table.put_item(Item = item)
    
    
    return
# Egy dict lista elemeit felteszi az adatbázisba olyan szerkezettel, hogy a kulcs a hash és egy listát tárol a dict aminek első eleme az előadó a második pedig a zene címe
def insertList(list_of_dicts):
   num = 0
   with table.batch_writer(overwrite_by_pkeys=['hash_value']) as batch:
         
      for dict in list_of_dicts:
         print(f" {num}/{len(list_of_dicts)} of songs is done")
         
         for key in dict:
            
      
            hash = key
            artist = dict[key][0]
            song = dict[key][1]
   
            batch.put_item( Item = {
               'hash_value': key,
               'song_name':  song,
               'artist': artist} )
               
               

def search(list_of_hashes):
   
  dict = {}
  for x in list_of_hashes:
      result = read(x)
      
      if(result != None):
         name = result['song_name']
         artist = result['artist']
         
         if name in dict.keys():
            dict[name][1] +=1
         else:
            dict[name]= [artist,1]
    
  for key in dict:
      
        dict[key][1] = dict[key][1]/len(list_of_hashes)

  return dict     


def searchFile(file_path):
   list = pipeline.pipeline_func_list(file_path)
   return search(list)

   

def selectAll():
   dict = {}

   response = table.scan()
   items = response['Items']
   while 'LastEvaluatedKey' in response:
      
      response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
      items.extend(response['Items'])
   
   for x in items:
      dict[x['hash_value']] = [x['song_name'],x['artist']]

   keys = sorted(list(dict.keys()))
   sorted_dict = { i : dict[i] for i in keys}
   print("Database loaded to memory, ready to look up songs")
   return sorted_dict


dict_of_songs = selectAll()

def searchinDict(list_of_hashes):
   dict = {}
   for x in list_of_hashes:
         try:
            result = dict_of_songs[x]
            name = result[0]
            artist = result[1]
            
            if name in dict.keys():
               dict[name][1] +=1
            else:
               dict[name]= [artist,1]
         
         except KeyError:
            continue     
      
   for key in dict:
         
         dict[key][1] = dict[key][1]/len(list_of_hashes)

   max = 0
   maxi = None
   
   for key in dict:
      if dict[key][1] > max:
         max = dict[key][1]
         maxi = key
         try:
            response = {dict[maxi][0] :maxi}
         except KeyError:
            return {"Error": "No songs found"}
   return response







