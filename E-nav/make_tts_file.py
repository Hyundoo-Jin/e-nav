# google TTS
from gtts import gTTS
import os
import pickle
import argparse
import pandas as pd
from tqdm import tqdm
import urllib


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--method')
parser.add_argument('-c', '--city')
parser.add_argument('-v', '--voice', help ='Clova TTS vocies. mijin, jinho', default = None)
args = parser.parse_args()

method = args.method
city = args.city

with open('{}/script_data.pickle'.format(city), 'rb') as f :
    script_data = pickle.load(f)
data = script_data['data']
shipname_list = script_data['shipname_list']
print('***************data for {} loading DONE!***************'.format(city))

save_dir = os.path.join(os.getcwd(), method)

error_script = ''

if method.lower() == 'google' :
    for index in tqdm(range(data.shape[0])) :
        script_num = data.Script_num.iloc[index]
        script = str(data.Script.iloc[index])
        script = ''.join(i for i in script if not i.isdigit())
        try :
            tts = gTTS(text = script, lang = 'ko')
            tts.save(os.path.join(save_dir, '{}.mp3'.format(script_num)))

        except :
            error_script += script_num + '\n'
    print('Audio saved.')
    with open('error_script.txt', 'w') as f :
        f.write(error_script)
    print('Error log saved.')

elif method.lower() == 'clova' :
    from random import randint

    # load keys
    with open('secret.pickle', 'rb') as f :
        client_id, client_secret, url = pickle.load(f)


    # set voice(mijin, jinho)
    voice = args.voice

    for index in tqdm(range(data.shape[0])) :
        speed = randint(-2, 2)
        script_num = data.Script_num.iloc[index]
        script = data.Script.iloc[index]

        try :
            enc_text = urllib.parse.quote(script)
            parsed_data = 'speaker={}&speed={}&text='.format(voice, speed) + enc_text
            request = urllib.request.Request(url)
            request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
            request.add_header("X-NCP-APIGW-API-KEY", client_secret)

            response = urllib.request.urlopen(request, data = parsed_data.encode('utf-8'))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                file_path = os.path.join(save_dir, '{}_{}.mp3'.format(script_num, voice))
                with open(file_path, 'wb') as f:
                    f.write(response_body)
                print("TTS mp3 save")

        except :
             error_script += script_num + '\n'
    with open('error_script.txt', 'w') as f :
         f.write(error_script)
    print('Error log saved.')


elif mothod.lower() == 'amazon' :
    import boto3

    client = boto3.client('polly', region_name = 'ap-northeast-3')

    response = client.synthesize_speech(
        OutputFormat = 'mp3',
        Text = '테스트입니다.'
    )



else :
    print('Argument "method" is not defined.')
