# 문자열의 '%'를 '%%'로 치환하는 메서드
def replace_percent_mark(text):
    # for key in re.findall('\'%(.*?)%\'', query, re.I|re.S):
    #     print(key)
    #     query = re.sub('\'%' + key + '%\'', 'CONCAT(TRIM(\' % \' ), \'' + key + '\', TRIM( \' % \' ))', query, 0, re.I|re.S)

    return text.replace('\'%\'', '\'%%\'')

# 소수 자릿수 표현
def float_under(number):
    if number is not None:
        return format(float(number), ".10f")
    else:
        return format(float(0), ".10f")

def float_under_account(number):
    if number is not None:
        return format(float(number), ".8f")
    else:
        return format(float(0), ".8f")
