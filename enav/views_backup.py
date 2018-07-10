from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import time
# Create your views here.
class ChatProcess :
    def __init__(self) :
        self.mode = 0
        self.step = 0

def parse_ship_info(string) :
    txt = string.replace(',', '')
    txt = txt.strip()
    infomations = txt.split()
    return infomations

def keyboard(request) :
    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['센터', '선박']
    })

status = ChatProcess()

@csrf_exempt

def message(request) :
    global status
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    nowtime = time.strftime('%H:%M')


    # '기타' 선택했을 땐 바로 연결
    if content == '기타' :
        status.step = 'end'
        if status.mode == '센터' :
            return JsonResponse({
                'message' : {
                    'text' : '상대 선박에 전달할 메세지를 입력하세요.'
                },
                'keyboard' : {
                    'type' : 'text'}
            })
        if status.mode == '선박' :
            return JsonResponse({
                'message' : {
                    'text' : '상대 센터에 전달할 메세지를 입력하세요.'
                },
                'keyboard' : {
                    'type' : 'text'
                }
            })

    # ship_info
    if status.step == 0 :
        status.mode = content
        status.step = 'ship_info'
        if content == '센터' :
            return JsonResponse({
                'message' : {
                    'text' : '센터모드로 진행합니다.\n교신할 가상의 선박 정보(선박명, 호출명, 출발지, 목적지, ETA)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 부산, 울산, 0100'
                },
                'keyboard' : {
                    'type' : 'text'}
            })
        else :
            status.mode = content
            return JsonResponse({
                'message': {
                    'text': '선박모드로 진행합니다.\n교신할 가상의 선박 정보(선박명, 호출명, 출발지, 목적지, ETA)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 부산, 울산, 0100'
                },
                'keyboard': {
                    'type': 'text'}
            })

    # reporting
    elif status.step == 'ship_info' :
        name, callname, departure, destination, eta = parse_ship_info(content)
        status.step = 'reporting'
        if status.mode == '센터' :
            return JsonResponse({
                'message' : {
                    'text' : '{}\n{}에서 투묘 요청\n호출명 : {}\n출발지 : {}\n목적지 : {}\nETA : {}'.format(nowtime, name, callname, departure, destination, eta)
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['확인', '불허', '기타']
                }
            })

        if status.mode == '선박' :
            return JsonResponse({
                'message' : {
                    'text' : '델타라인 통과하였습니다. 센터에 투묘 보고 하시겠습니까?'
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['보고하기', '선박정보 수정', '기타']
                }
            })

    # reported
    elif status.step == 'reporting' :
        if status.mode == '센터'  :
            if content == '확인' :
                status.step = 'reported_checked'
                return JsonResponse({
                    'message' : {
                        'text' : '할당할 투묘지를 입력해주세요.'
                    },
                    'keyboard' : {
                        'type' : 'text'
                    }
                })

            else :
                status.step = 'reported_denied'
                return JsonResponse({
                    'message' : {
                        'text' : '불허사유를 입력해주세요.'
                    },
                    'keyboard' : {
                        'type' : 'text'
                    }
                })
        else :
            if content == '보고하기' :
                return JsonResponse({
                    'message' : {
                        'text' : '{}\n{}에서 투묘 보고\n호출명 : {}\n출발지 : {}\n목적지 : {}\nETA : {}'.format(nowtime, name, callname, departure, destination, eta)
                    }
                })

    # end
    else :
        status.step = None
        return JsonResponse({
            'mesage' : {
                'text' : 'Test가 종료되었습니다. 처음부터 다시 시작합니다.'
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['센터', '선박']
            }
        })

