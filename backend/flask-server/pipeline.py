import librosa
import os
import numpy as np

# filebol spetrogram
def spect_from_file(file): 
    scale, sr = librosa.load(file)
    spectrogram = librosa.stft(y=scale, n_fft=2048, hop_length=512) #1025 frequency bin kezdetben
    log_spectrogram = librosa.power_to_db(np.abs(spectrogram))
    return log_spectrogram[80:-550] # 500-5000Hz-ig

# n_buckets db vodorre bontja a spektrogram oszlopait, es vissza adja a vodrokon beluli maximumok oszlopon beluli helyenek listajat 
def bucket_func(input_mx, n_buckets): # parameterek: mel spektrogram matrixa, ahany vodorben akarjuk nezni a maximumokat
    input_mx = input_mx[:(len(input_mx) - (len(input_mx) % n_buckets))] # make the number of frequencies dividible by the number of buckets, throw away the remainder
    input_mx = list(zip(*input_mx)) # Transpose matrix 
    output_mx = [] 
    for row_i in range(len(input_mx)):
        sublists = [input_mx[row_i][i:i+len(input_mx[row_i])//n_buckets] for i in range(0, len(input_mx[row_i]), len(input_mx[row_i])//n_buckets)] # n number of buckets
        for bucket in sublists:
            output_mx.append([row_i, (sublists.index(bucket)*len(input_mx[row_i])//n_buckets) + bucket.index(max(bucket))]) # search the maxes in the buckets
    return output_mx

# Ez generalja a fingerprinteket (azaz minden pontbol kiszamolja a kovetkezo 'size' db pont tavolsagait, es az lesz egy fingerprint)
# Dictionaryben adja vissza
def calc_hashes_dict(mx, size, hash_value):
    mx = np.array(mx)
    output_dict = {}
    for i in range(len(mx)-(size+1)):
        output_dict_key = ''
        for j in range(1, size+1, 1):
             output_dict_key =  output_dict_key + str(abs(mx[i+j][0] - mx[i][0])) + str(abs(mx[i+j][1] - mx[i][1]))
        output_dict.update({int(output_dict_key): hash_value})
    return output_dict

# Ugyanaz, csak List-et at vissza
def calc_hashes_list(mx, size):
    output_mx = []
    mx = np.array(mx)
    for i in range(len(mx)-(size+1)):
        output_key = ''
        for j in range(1, size+1, 1):
            output_key =  output_key + str(abs(mx[i+j][0] - mx[i][0])) + str(abs(mx[i+j][1] - mx[i][1]))
        output_mx.append(int(output_key))
    return output_mx


## 2 fele pipelinet implementaltam, az egyik Dictionary-ben adja vissza, key-value pair kent a hasheket,
## A masik listaban csak a hasheket, nem tudom melyik kell nektek

#  1db file-bol general hasheket: egy dictionary-t ad vissza, aminek a kulcsai a hash-ek, a value-k pedig a parameterkent megadott hash_value
def pipeline_func_dict(file_name, hash_value=None):
    op = spect_from_file(file_name) 
    op = bucket_func(op, 6) 
    op = calc_hashes_dict(op, 7, hash_value) 
    return op

# Ugyanaz csak list-el
def pipeline_func_list(file_name, hash_value=None):
    op = spect_from_file(file_name)
    op = bucket_func(op, 6) 
    op = calc_hashes_list(op, 7) 
    return op


## PELDA a hasznalatra (a dict-es verzio)

## Ez a kod beolvas egy mappabol .wav-okat, utana kiszamolja es eltarolja a hashek parjait (hash - file nev) a 'hashes' valtozoban, kiirja az elso elemnek a hasjeit
 # mappa 




def getHashestoList(path):
    test_files = os.listdir(path) # file-ok a mappaban
    hashes = []
    for file in test_files:
        file_path = os.path.join(path, file)
        hashes.append(pipeline_func_dict(file_path, file))
    for x in hashes:
        for key in x:
            x[key] = x[key].rstrip(".wav").split(" - ")
    return hashes





