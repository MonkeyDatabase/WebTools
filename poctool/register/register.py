import re

POC_NAME_REGEX = r'''(?sm)POCBase\):.*?name\s*=\s*['"](?P<result>.*?)['"]'''


def get_poc_name(code):
    return extract_regex_result(POC_NAME_REGEX, code)


def extract_regex_result(regex, content, flags=0):
    ret = None

    if regex and content and '?P<result>' in regex:
        match = re.search(regex, content, flags)
        if match:
            ret = match.group('result')
        return ret
