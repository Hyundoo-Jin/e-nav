from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import time
from . import options

# Create your views here.
class ChatProcess :
    def __init__(self) :
        self.mode = 'init'
        self.step = 'init'
        self.name = None
        self.callname = None
        self.departure = None
        self.destination = None
        self.eta = None
        self.speed = None
        self.ship = None
        self.others = None

    def clear(self) :
        self.mode = 'init'
        self.step = 'init'

def parse_ship_info(string) :
    txt = string.strip()
    txt = txt.replace(',', ' ')
    infomations = txt.split()
    return infomations

def keyboard(request) :
    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['투묘', '추월']
    })

if 'status' not in globals() :
    status = ChatProcess()

@csrf_exempt

def message(request) :
    global status
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    nowtime = time.strftime('%H:%M')

    if status.step == 'init' :
        status.mode = content

    if status.mode == '투묘' :
        result, status = options.anchor(content, nowtime, status)
    
    if status.mode == '추월' :
        result, status = options.overtake(content, nowtime, status)

    return result
