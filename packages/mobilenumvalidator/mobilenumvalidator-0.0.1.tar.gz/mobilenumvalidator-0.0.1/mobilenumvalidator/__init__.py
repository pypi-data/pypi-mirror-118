import re

def clean_no(no):
    no = re.sub(r'[^0-9]', '', no)
    return no

def validate_no(no):
    flag = False
    if len(no) >= 8 and len(no) <= 11:
        pass
    else:
        flag = True
    return flag

def format_no(no):
    local_no = no[-8:] 
    if no.startswith('61') and len(no) == 11:
        area_code = no[2]
        no = '0' + area_code + local_no
        return no
    elif no.startswith('0') and len(no) == 10:
        return no
    elif not(no.startswith('0')) and len(no) == 9:
        no = '0' + no
        return no
    elif no.startswith('13') or no.startswith('18'):
        return no

def validator(no):
    no_cleaned = clean_no(no)
    validator_flag = validate_no(no_cleaned)
    if validator_flag:
        return no_cleaned, validator_flag
    else:
        no_formatted = format_no(no_cleaned)
        return no_formatted, validator_flag