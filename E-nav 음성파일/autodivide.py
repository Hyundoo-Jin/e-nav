import pandas as pd
import numpy as np
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import argparse

## Define Functions
def make_chunk(audio) :
    return split_on_silence(audio,
                # must be silent for at least 3 seconds or 3000 ms
                min_silence_len=3000,
                # consider it silent if quieter than -45 dBFS
                #Adjust this per requirement
                silence_thresh=-45)

def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

### Initialize
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--city', help = 'city that you want to cut .mp3', type = str)
args = parser.parse_args()
city = args.city
uncut_dir = os.path.join(os.getcwd(), city, 'uncut')
target_dir = os.path.join(os.getcwd(), city, 'cut')
num_uncut_dir = len(os.listdir(uncut_dir))
print('Initialized Done For ', city)

### Make cut mp3
for j, dir in enumerate(os.listdir(uncut_dir)) :
    if '.xlsx' in dir :
        continue
    temp_dir = os.path.join(uncut_dir, dir)
    to_dir = os.path.join(target_dir, dir)
    if not os.path.exists(to_dir) :
        os.mkdir(to_dir)

    for k, file in enumerate(os.listdir(temp_dir)) :
        num_files = len(os.listdir(temp_dir))
        audio = AudioSegment.from_mp3(os.path.join(temp_dir, file))
        chunks = make_chunk(audio)
        print('File : ', k + 1, '/', num_files, ' is ready.')

        for i, chunk in enumerate(chunks):
            #Create 1 seconds silence chunk
            silence_chunk = AudioSegment.silent(duration=1000)
            #Add  1 sec silence to beginning and end of audio chunk
            audio_chunk = silence_chunk + chunk + silence_chunk
            #Normalize each audio chunk
            normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
            #Export audio chunk with new bitrate
            print("exporting chunk{0}.mp3".format(i) )
            normalized_chunk.export(os.path.join(to_dir, "chunk{0}.mp3".format(i)), bitrate='192k', format="mp3")
    print('Dirs : ', j + 1, '/', num_uncut_dir, ' done.')
