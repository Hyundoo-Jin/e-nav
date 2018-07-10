from django.http import JsonResponse
from random import randint

def parse_ship_info(string) :
    txt = string.strip()
    txt = txt.replace(',', ' ')
    infomations = txt.split()
    return infomations

def anchor(content, nowtime, status) :
    if content == '기타' :
        status.step = 'end'
        if status.ship == '센터' :
            return [JsonResponse({
                'message' : {
                    'text' : '상대 선박에 전달할 메세지를 입력하세요.'
                },
                'keyboard' : {
                    'type' : 'text'}
            }), status]
        if status.ship == '선박' :
            return [JsonResponse({
                'message' : {
                    'text' : '상대 센터에 전달할 메세지를 입력하세요.'
                },
                'keyboard' : {
                    'type' : 'text'
                }
            }), status]

    # init
    if status.step == 'init' :
        status.step = 'anchor_mode'
        return [JsonResponse({
            'message' : {
                'text' : '투묘 시나리오를 선택하였습니다.\n센터, 선박 중 어떤 입장으로 Test할지 선택해 주세요.'
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['센터', '선박']}
        }), status]

    # anchor_mode
    elif status.step == 'anchor_mode' :
        status.ship = content
        status.step = 'ship_info'
        if content == '센터' :
            return [JsonResponse({
                'message' : {
                    'text' : '센터모드로 진행합니다.\n교신할 가상의 선박 정보(선박명, 호출명, 출발지, 목적지, ETA)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 부산, 울산, 0100'
                },
                'keyboard' : {
                    'type' : 'text'}
            }), status]
        else :
            return [JsonResponse({
                'message': {
                    'text': '선박모드로 진행합니다.\n교신할 가상의 선박 정보(선박명, 호출명, 출발지, 목적지, ETA)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 부산, 울산, 0100'
                },
                'keyboard': {
                    'type': 'text'}
            }), status]

    # reporting
    elif status.step == 'ship_info' :
        if len(parse_ship_info(content)) == 5 : 
            status.name, status.callname, status.departure, status.destination, status.eta = parse_ship_info(content)
        else :
            return [JsonResponse({
                'message' : {
                    'text' : '잘못된 형식의 입력입니다.\n교신할 가상의 선박 정보(선박명, 호출명, 출발지, 목>적지, ETA)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 부산, 울산, 0100'
                },
                'keyboard' : {
                    'type' : 'text'
                }
            }), status]
        status.step = 'reporting'
        if status.ship == '센터' :
            return [JsonResponse({
                'message' : {
                    'text' : '{}\n{}에서 투묘 보고\n호출명 : {}\n출발지 : {}\n목적지 : {}\nETA : {}'.format(nowtime, status.name, status.callname, status.departure, status.destination, status.eta)
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['확인', '불허', '기타']
                }
            }), status]

        else :
            return [JsonResponse({
                'message' : {
                    'text' : '델타라인 통과하였습니다. 센터에 투묘 보고 하시겠습니까?'
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['보고하기', '선박정보 수정', '기타']
                }
            }), status]

    # reported
    elif status.step == 'reporting' :
        if status.ship == '센터' :
            if content == '확인' :
                status.step = 'reported_checked'
                return [JsonResponse({
                    'message' : {
                        'text' : '할당할 투묘지와 주의사항을 입력해주세요.\n\nex) 마이크3에 투묘하십시오. 지금 나가는 어선 많습니다. 주의하세요.'
                    },
                    'keyboard' : {
                        'type' : 'text'
                    }
                }), status]

            if content == '불허' :
                status.step = 'reported_disallowed'
                return [JsonResponse({
                    'message' : {
                        'text' : '불허사유와 추가사항을 입력해주세요.\n\nex) 지금 항만에 배가 너무 많습니다. 10분 뒤에 다시 보고해주세요.'
                    },
                    'keyboard' : {
                        'type' : 'text'
                    }
                }), status]
        else :
            if content == '보고하기' :
                status.clear()
                return [JsonResponse({
                    'message' : {
                        'text' : '{}\n{}에서 투묘 보고\n호출명 : {}\n출발지 : {}\n목적지 : {}\nETA : {}\n\nTest가 종료되었습니다. 처음부터 다시 시작합니다.'.format(nowtime, status.name, status.callname, status.departure, status.destination, status.eta)
                    },
                    'keyboard' : {
                        'type' : 'buttons',
                        'buttons' : ['투묘', '추월']
                    }
                }), status]
            else :
                status.step = 'ship_info'
                return [JsonResponse({
                    'message': {
                        'text': '선박모드로 진행합니다.\n교신할 가상의 선박 정보(선박명, 호출명, 출발지, 목적지, ETA)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 부산, 울산, 0100'
                    },
                    'keyboard': {
                        'type': 'text'}
                }), status]

    # reported_checked
    elif status.step == 'reported_checked' :
        status.clear()
        return [JsonResponse({
            'message' : {
                'text' : '{}\n{} 투묘 보고 완료\n호출명 : {}\nETA : {}\n메세지 : {}\n\nTest가 종료되었습니다. 처음부터 다시 시작합니다.'.format(nowtime, status.name, status.callname, status.eta, content)
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['투묘', '추월']
            }
        }), status]

    # reported_denied
    elif status.step == 'reported_disallowed' :
        status.clear()
        return [JsonResponse({
            'message' : {
                'text' : '{}\n{}에서 보고된 투묘는 다음과 같은 이유로 불가능합니다.\n\n사유 : {}\n\nTest가 종료되었습니다. 처음부터 다시 시작합니다.'.format(nowtime, status.name, content)
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['투묘', '추월']
            }
        }), status]


    # end
    else :
        status.clear()
        return [JsonResponse({
            'message' : {
                'text' : '{}\n\n메세지 : {}\n\nTest가 종료되었습니다. 처음부터 다시 시작합니다.'.format(nowtime, content)
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['투묘', '추월']
            }
        }), status]



def overtake(content, nowtime, status) :
    if status.step == 'init' :
        status.step = 'overtake'
        return [JsonResponse({
            'message' : {
                'text' : '추월 시나리오를 선택하였습니다.\n어떤 선박으로 Test할지 선택해 주세요'
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['추월선', '피추월선']
            }
        }), status]

    # overtake
    elif status.step == 'overtake' :
        status.ship = content
        status.step = 'ship_info_ot'
        return [JsonResponse({
            'message' : {
                'text' : '추월선의 선박 정보(선박명, 호출명, 속도, 목적지)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 10노트, 부산'
            },
            'keyboard' : {
                'type' : 'text'
            }
        }), status]

    # 'ship_info_ot'
    elif status.step == 'ship_info_ot':
        if len(parse_ship_info(content)) == 4 :
            status.name, status.callname, status.speed, status.destination = parse_ship_info(content)
        else :
            return [JsonResponse({
                'message' : {
                    'text' : '잘못된 형식의 입력입니다.\n추월선의 선박 정보(선박명, 호출명, 속도, 목적지)를 순서대로 입력해주세요.\nex) Enav호, ENAV2018, 10노트, 부산'
                },
                'keyboard' : {
                    'type' : 'text'
                }
            }), status]

        if status.ship == '피추월선' :
            status.step = 'answer_agree'
            rand = randint(0, 1)
            if rand :
                status.others = '좌현'
            else :
                status.others = '우현'
            return [JsonResponse({
                'message' : {
                    'text' : '{}\n{}에서 귀선 {}측 추월 요청\n\n동의하시겠습니까?\n\n선박명 : {}\n호출명 : {}\n속도 : 10노트\n목적지 : {}\n위치 : 130도'.format(nowtime, status.name, status.others, status.name, status.callname, status.destination)
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['Yes', 'No']
                }
            }), status]
        else :
            status.step = 'select_direction'
            return [JsonResponse({
                'message' : {
                    'text' : '어느 방향으로 추월할지 선택하십시오.'
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['좌현', '우현']
                }
            }), status]

    # answer_agree
    elif status.step == 'answer_agree' :
        if content == 'Yes' :
            status.clear()
            return [JsonResponse({
                'message' : {
                    'text' : '{}\n{}에서 귀선의 {}측으로 추월합니다.\n\nTest가 종료되었습니다. 초기로 돌아갑니다.'.format(nowtime, status.name, status.others)
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['투묘', '추월']
                }
            }), status]

        else :
            status.step = 'answer_disagree'
            return [JsonResponse({
                'message' : {
                    'text' : '추월이 불가능한 이유는 무엇입니까?'
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['{} 방향에 물체(선박, 암초 등)이 있습니다.'.format(status.others), '{} 방향으로 변침이 어렵습니다.'.format(status.others), '직접입력']
                }
            }), status]

    # answer_disagree
    elif status.step == 'answer_disagree' :
        status.step = 'disagree_reason'
        if content == '직접입력' :
            return [JsonResponse({
                'message' : {
                    'text' : '추월이 불가능한 사유 및 조치사항을 입력해주세요.\n상대 선박에 직접 전송됩니다.'
                },
                'keyboard' : {
                    'type' : 'text'
                }
            }), status]

        else :
            if status.others == '좌현' :
                temp = '우현'
            else :
                temp = '좌현'
            return [JsonResponse({
                'message' : {
                    'text' : '상대 선박에 어떤 추가조치를 취하시겠습니까?'
                },
                'keyboard' : {
                    'type' : 'buttons',
                    'buttons' : ['{}으로 추월하십시오.'.format(temp), '추월이 불가능합니다.', '직접입력']
                }
            }), status]

    # select_direction
    elif status.step == 'select_direction' :
        status.clear()
        return [JsonResponse({
            'message' : {
                'text' : '{}\n{}에서 {}으로 추월을 요청합니다.\n\nTest가 종료되었습니다. 초기화면으로 돌아갑니다.'.format(nowtime, status.name, content)
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['투묘', '추월']
            }
        }), status]

    # disagree_reason
    else :
        status.clear()
        return [JsonResponse({
            'message' : {
                'text' : '{}\n\n상대 선박의 추월 요청이 거부되었습니다.\n\n사유 및 추가조치 : {}\n\nTest가 종료되었습니다. 초기화면으로 돌아갑니다.'.format(nowtime, content)
            },
            'keyboard' : {
                'type' : 'buttons',
                'buttons' : ['투묘', '추월']
            }
        }), status]
