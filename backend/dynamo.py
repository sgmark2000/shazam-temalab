import boto3, config, string, random
from boto3.dynamodb.conditions import Key



dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=config.ACCESS_KEY_ID,
                            aws_secret_access_key=config.ACCESS_SECRET_KEY,
                              region_name=config.REGION)
table = dynamodb.Table('shazam')
print(list(dynamodb.tables.all()))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))



def create_table(table_size):
    table = [[] for x in range(table_size)]
    return table

def pseduo_hash(tuple,bucket):
    
    number = int(tuple[0])
    remainder = number%(len(bucket))
    
    bucket[remainder-1].append(tuple)
    
    



def read(bucket,value):
    response = table.get_item(
        Key={ 'hash_bucket': bucket,
             'hash_of_song': value}
    )
    print(response['Item'])

def query(bucket):
   response = table.query(KeyConditionExpression=Key("hash_bucket").eq(str(bucket)))
   print(response['Items'])

def insert(bucket,tuple):
    item = {
       'hash_bucket' : bucket,
       'hash_of_song' :tuple[0],
       'song_name' : tuple[1]}
    table.put_item(Item = item)
    
    
    return


hash_table = create_table(11)
list = [(str(x) , id_generator()) for x in range(30)]
for item in list:
  pseduo_hash(item,hash_table)

print(hash_table)
                
read('12345','123456')


for i in range(len(hash_table)):
   for j in range(len(hash_table[i])):
      insert(str(i),hash_table[i][j])
   
print(table.scan()['Items'])
query(10)