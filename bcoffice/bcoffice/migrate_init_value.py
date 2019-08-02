# 관리자 관련 초기 생성 값
class Account:
    DEFAULT_SUPER_USER = {
        'EMAIL': 'administrator@domain.com'
        , 'PASSWORD': 'superUser!!'
    }

    DEFAULT_DEPT_DUTY = {
        'duty_cd'           : '00'
        , 'duty_name'       : '관리자'
        , 'duty_eng_name'   : 'Administrator'
        , 'status'          : 'ACTV'
    }

    DEFAULT_DEPT_RANK = {
        'rank_cd'           : '00'
        , 'rank_name'       : '관리자'
        , 'rank_eng_name'   : 'Administrator'
        , 'status'          : 'ACTV'
    }

    DEFAULT_DEPT_TYPE = {
        'dept_cd'           : '00'
        , 'team_cd'         : '00'
        , 'dept_name'       : '관리부'
        , 'dept_eng_name'   : 'Management'
        , 'managerial'      : 1
        , 'status'          : 'ACTV'
    }


class Boards:
    DEFAULT_FAQ_CATEGORY = [
        {"category": "전체보기", "category_id": 1, "lang": "ko"}
        , {"category": "개인정보", "category_id": 2, "lang": "ko"}
        , {"category": "기타", "category_id": 3, "lang": "ko"}
        , {"category": "인증", "category_id": 4, "lang": "ko"}
        , {"category": "거래", "category_id": 5, "lang": "ko"}

        , {"category": "View all", "category_id": 1, "lang": "en"}
        , {"category": "Personal Information", "category_id": 2, "lang": "en"}
        , {"category": "etc.", "category_id": 3, "lang": "en"}
        , {"category": "Authentication", "category_id": 4, "lang": "en"}
        , {"category": "Trading", "category_id": 5, "lang": "en"}

        , {"category": "Xem toàn bộ", "category_id": 1, "lang": "vi"}
        , {"category": "Thông tin cá nhân", "category_id": 2, "lang": "vi"}
        , {"category": "Nội dung khác", "category_id": 3, "lang": "vi"}
        , {"category": "Xác nhận", "category_id": 4, "lang": "vi"}
        , {"category": "Giao dịch", "category_id": 5, "lang": "vi"}

        , {"category": "全体を見る", "category_id": 1, "lang": "ja"}
        , {"category": "個人情報", "category_id": 2, "lang": "ja"}
        , {"category": "その他", "category_id": 3, "lang": "ja"}
        , {"category": "認証", "category_id": 4, "lang": "ja"}
        , {"category": "取引", "category_id": 5, "lang": "ja"}

        , {"category": "查看全部", "category_id": 1, "lang": "zh-CN"}
        , {"category": "个人信息", "category_id": 2, "lang": "zh-CN"}
        , {"category": "其他", "category_id": 3, "lang": "zh-CN"}
        , {"category": "验证", "category_id": 4, "lang": "zh-CN"}
        , {"category": "交易", "category_id": 5, "lang": "zh-CN"}
    ]


class CoinAccount:
    DEFAULT_WITHDRAW_REASON = [
        {'code': 100, 'description': 'HOT비중초과', 'reason_type': 'HOT'}
        , {'code': 150, 'description': 'COLD비중초과', 'reason_type': 'COLD'}
        , {'code': 200, 'description': '오입금환불', 'reason_type': 'HOT, COLD'}
        , {'code': 999, 'description': '기타사유', 'reason_type': 'HOT, COLD'}
    ]


class PolicyManage:
    DEFAULT_SYSTEM_ALARM = [
        {'alarm_code': '0000', 'is_sms': 1, 'is_email': 1}
        , {'alarm_code': '0100', 'is_sms': 0, 'is_email': 1}
        , {'alarm_code': '0200', 'is_sms': 0, 'is_email': 1}
        , {'alarm_code': '0201', 'is_sms': 1, 'is_email': 0}
        , {'alarm_code': '0300', 'is_sms': 1, 'is_email': 0}
        , {'alarm_code': '0400', 'is_sms': 0, 'is_email': 1}
        , {'alarm_code': '0401', 'is_sms': 0, 'is_email': 1}
        , {'alarm_code': '0500', 'is_sms': 1, 'is_email': 1}
        , {'alarm_code': '0600', 'is_sms': 0, 'is_email': 0}
    ]


class Supports:
    DEFAULT_QUESTION_TYPE = [
        {"type": "계정", "category_id": 1, "lang": "ko"}
        , {"type": "매매", "category_id": 2, "lang": "ko"}
        , {"type": "오입금", "category_id": 3, "lang": "ko"}
        , {"type": "일반", "category_id": 4, "lang": "ko"}
        , {"type": "제안", "category_id": 5, "lang": "ko"}

        , {"type": "Account", "category_id": 1, "lang": "en"}
        , {"type": "Trading", "category_id": 2, "lang": "en"}
        , {"type": "Deposit Error", "category_id": 3, "lang": "en"}
        , {"type": "General Inquiry", "category_id": 4, "lang": "en"}
        , {"type": "Suggestions", "category_id": 5, "lang": "en"}

        , {"type": "Tài khoản", "category_id": 1, "lang": "vi"}
        , {"type": "Tiếp thị", "category_id": 2, "lang": "vi"}
        , {"type": "Nạp tiền sai", "category_id": 3, "lang": "vi"}
        , {"type": "Yêu cầu chung", "category_id": 4, "lang": "vi"}
        , {"type": "Đề xuất", "category_id": 5, "lang": "vi"}

        , {"type": "アカウント", "category_id": 1, "lang": "ja"}
        , {"type": "マーケティング", "category_id": 2, "lang": "ja"}
        , {"type": "誤入金", "category_id": 3, "lang": "ja"}
        , {"type": "一般", "category_id": 4, "lang": "ja"}
        , {"type": "提案", "category_id": 5, "lang": "ja"}

        , {"type": "帐户", "category_id": 1, "lang": "zh-CN"}
        , {"type": "市场", "category_id": 2, "lang": "zh-CN"}
        , {"type": "存款错误", "category_id": 3, "lang": "zh-CN"}
        , {"type": "一般", "category_id": 4, "lang": "zh-CN"}
        , {"type": "主张", "category_id": 5, "lang": "zh-CN"}
    ]