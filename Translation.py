import json
import urllib.error
import urllib.parse
import urllib.request

from translate import Translator


def translate(sentence, src_lan, tgt_lan, apikey):
    url = 'http://api.niutrans.com/NiuTransServer/translation?'
    data = {"from": src_lan, "to": tgt_lan, "apikey": apikey, "src_text": sentence}
    data_en = urllib.parse.urlencode(data)
    req = url + "&" + data_en
    res = urllib.request.urlopen(req)
    res = res.read()
    res_dict = json.loads(res)
    if "tgt_text" in res_dict:
        result = res_dict['tgt_text']
    else:
        result = res
    return result


def translate_zh(text):
    translator = Translator(to_lang="zh")
    return translator.translate(text)


if __name__ == "__main__":
    trans = translate("Hello", 'en', 'zh', 'e85329b06057b0b7349399fe94ed3038')
    print(trans)
