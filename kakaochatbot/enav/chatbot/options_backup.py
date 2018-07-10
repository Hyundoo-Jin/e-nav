from django.http import JsonResponse

def parse_ship_info(string) :
    txt = string.strip()
    txt = txt.replace(',', ' ')
    infomations = txt.split()
    return infomations

def anchor(content, nowtime, status) :
    if content == '기타' :
        status.step = 'end'
        if status.mode == '센터' :
            return [JsonResponse({
                'message' : {
                    'text' : '상대 선박에 전달할 메세지를 입력하세요.'
                },
                'keyboard' : {
                    'type' : 'text'}
            }), status]
        if status.mode == '선박' :
            return [JsonResponse({
                'message' : {
                    'text' : '상대 센터에 전달할 메세지를 입력하세요.'
                },
                'keyboard' : {
                    'type' : 'text'
                }
            }), status]

    # ship_info
    if status.step == 'init' :
        status.mode = content
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
        if status.mode == '센터' :
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
        if status.mode == '센터' :
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
                        'buttons' : ['센터', '선박']
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
                'buttons' : ['센터', '선박']
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
                'buttons' : ['센터', '선박']
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
                'buttons' : ['센터', '선박']
            }
        }), status]
