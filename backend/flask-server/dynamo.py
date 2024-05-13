import boto3, config, string, random
from boto3.dynamodb.conditions import Key



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



list = [(x , "Plug Walk","Rich the Kid") for x in range(30)]



                


list.append((30,"3korty","Azahriah"))
for j in list:
   insert(j[0],j[1],j[2])
   




list1 = [x for x in range(20,31)]
list1.append(36)
list1.append(38)
list1.append(39)
list1.append(40)

print(getAll())