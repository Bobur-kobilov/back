from django.conf import settings

ADDRESS_TYPE_INSIDE = 'INSIDE'
ADDRESS_TYPE_OUTSIDE = 'OUTSIDE'

WALLET_TYPE_HOT = 'HOT'
WALLET_TYPE_COLD = 'COLD'

def get_map_item(map = None, code = None):
    result = None
    for item in map:
        if map[item]['code'] == code:
            result = {}
            result[item] = map[item]
            break

    return result

def get_map_item_object(map = None, code = None):
    result = None
    for item in map:
        if map[item]['code'] == code:
            result = map[item]
            break

    return result

def get_map_item_field(map = None, code = None, field = 'txt'):
    result = None
    for item in map:
        if map[item]['code'] == code:
            result = map[item][field]
            break

    return result


currencyDic = {}
for object in settings.CURRENCY_LIST:
    currencyDic[object['id']] = {"code": object["code"].upper()}

marketDic = {}
for object in settings.MARKET_LIST:
    marketDic[object['market_id']] = {"code": object["name"]}

selectMarketDic = {}
for object in settings.MARKET_LIST:
    selectMarketDic[object['name']] = {"code": object["market_id"]}

class StateMap :
    data_map = {
        'CANCEL'              : {"code": 0,   "txt": "취소"},
        'NOT_CONCLUDE'        : {"code": 100, "txt": "미체결"},
        'CONCLUDE'            : {"code": 200, "txt": "체결"},
        'CORRECTION'          : {"code": 300, "txt": "정정"},
        'PARTIAL_CONCLUDE'    : {"code": 'partial_conclude', "txt": "부분체결"},
        'REMAIN_CANCEL'       : {"code": 'remain_cancel', "txt": "잔량취소"}
    }

    def get_item(code = None):
        return get_map_item(map = StateMap.data_map, code = code)

    def get_item_object(code = None):
        return get_map_item_object(map = StateMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = StateMap.data_map, code = code, field = field)


class TypeMap :
    data_map = {
        "BID"   : {"code": 'Bid', "txt": "매수"},
        "ASK"   : {"code": 'Ask', "txt": "매도"}
    }

    def get_item(code = None):
        return get_map_item(map = TypeMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = TypeMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = TypeMap.data_map, code = code, field= field)


class OrderMap :
    data_map = {
        "ORD"   : {"code": 'Ord', "txt": "주문"},
        "MOD"   : {"code": 'Mod', "txt": "정정"},
        "CAC"   : {"code": 'Cac', "txt": "취소"}
    }

    def get_item(code = None):
        return get_map_item(map = OrderMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = OrderMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = OrderMap.data_map, code = code, field = field)


class OrdTypeMap :
    data_map = {
        "LIMIT"    : {"code": 'limit'   , "txt": "지정가"},
        "MARKET"   : {"code": 'market'  , "txt": "시장가"}
    }
    
    def get_item(code = None):
        return get_map_item(map = OrdTypeMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = OrdTypeMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = OrdTypeMap.data_map, code = code, field= field)


class StopStateMap : 
    data_map = {
        "CANCEL"     : {"code": 0   , "txt": "취소"},
        "WATCHING"   : {"code": 100 , "txt": "감시중"},
        "EXCUTE"     : {"code": 200 , "txt": "주문실행"},
        "HIDE"       : {"code": 300 , "txt": "Hide"}
    }
        
    def get_item(code = None):
        return get_map_item(map = StopStateMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = StopStateMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = StopStateMap.data_map, code = code, field= field)


class DepositsAasmStateMap :
    data_map = {
        "ACCEPTED"      : {'code' : 'accepted'  , "txt": '입금완료'},
        "SUBMITTING"    : {'code' : 'submitting', "txt": '제출완료'},
        "SUBMITTED"     : {'code' : 'submitted' , "txt": '처리중'},
        "REJECTED"      : {'code' : 'rejected'  , "txt": '거부'},
        "CANCELLED"     : {'code' : 'cancelled' , "txt": '취소'}
    }

    def get_item(code = None):
        return get_map_item(map = DepositsAasmStateMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = DepositsAasmStateMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = DepositsAasmStateMap.data_map, code = code, field = field)


class WithdrawAasmStateMap :
    data_map = {
        'DONE'          : {'code' : 'done',         'txt': '출금완료'},
        'ACCEPTED'      : {'code' : 'accepted',     'txt': '신청완료'},
        'SUBMITTING'    : {'code' : 'submitting',   'txt': '확인대기'},
        'SUBMITTED'     : {'code' : 'submitted',    'txt': '심사대기'},
        'PROCESSING'    : {'code' : 'processing',   'txt': '처리중'},
        'ALMOST_DONE'   : {'code' : 'almost_done',  'txt': '전송중'},
        'REJECTED'      : {'code' : 'rejected',     'txt': '신청거부'},
        'SUSPECT'       : {'code' : 'suspect',      'txt': '상태이상'},
        'FAILED'        : {'code' : 'failed',       'txt': '출금오류'},
        'CANCELED'      : {'code' : 'canceled',     'txt': '취소'},
        'WAIT_CONFIRM'  : {'code' : 'wait_admin_confirm', 'txt': '수동출금대기'},
    }
    
    def get_item(code = None):
        return get_map_item(map = WithdrawAasmStateMap.data_map, code = code)

    def get_item_object(code = None):
        return get_map_item_object(map = WithdrawAasmStateMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = WithdrawAasmStateMap.data_map, code = code, field = field)


class DepositWithdrawTypeMap :
    data_map = {
        'DEPOSITS'  : {'code' : 'Deposits', 'txt': '입금'},
        'WITHDRAWS' : {'code' : 'Withdraws', 'txt': '출금'},
    }
    
    def get_item(code = None):
        return get_map_item(map = DepositWithdrawTypeMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = DepositWithdrawTypeMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = DepositWithdrawTypeMap.data_map, code = code, field = field)


class AccountVersionReasonMap :
    data_map = {
        'UNKNOWN'                       : {'code' : 0, 'txt': ''},
        'PURCHASED_COMPLETE'            : {'code' : 110, 'txt': '매수완료'},
        'SALE_COMPLETE'                 : {'code' : 120, 'txt': '매도완료'},
        'ORDER_COMPLETE'                : {'code' : 600, 'txt': '주문완료'},
        'ORDER_CANCELED'                : {'code' : 610, 'txt': '주문취소'},
        'BELOW_MINIMUM_TRADING_VOLUME'  : {'code' : 620, 'txt': '최소매매수량 이하'},
        'WITHDRAW_VOLUME_LOCKED'        : {'code' : 800, 'txt': '출금신청'},
        'WITHDRAW_CANCELED'             : {'code' : 810, 'txt': '출금신청 취소'},
        'INCOME'                        : {'code' : 1000, 'txt': '입금'},
        'WITHDRAW'                      : {'code' : 2000, 'txt': '출금'},
        'FEE'                           : {'code' : 3000, 'txt': '추천인 수수료 지급'}
    }

    def get_item(code = None):
        return get_map_item(map = AccountVersionReasonMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = AccountVersionReasonMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = AccountVersionReasonMap.data_map, code = code, field = field)


class TrendMap :
    data_map = {
        'SALE_CONCLUDE'     : {'code' : 0, 'txt': '매도체결'},
        'BUYING_CONCLUDE'   : {'code' : 1, 'txt': '매수체결'}
    }
    
    def get_item(code = None):
        return get_map_item(map = TrendMap.data_map, code = code)
    
    def get_item_object(code = None):
        return get_map_item_object(map = TrendMap.data_map, code = code)

    def get_item_field(code = None, field = 'txt'):
        return get_map_item_field(map = TrendMap.data_map, code = code, field = field)
