from dataclasses import dataclass

def is_all_chinese(string):
    for char in string:
        if not ('\u4e00' <= char <= '\u9fff'):
            return False
    return True

def is_float(s):
    try:
        float(s)
        return '.' in s or 'e' in s.lower()  # 确保是浮点数
    except ValueError:
        return False

def is_integer(s):
    return s.isdigit() or (s[0] == '-' and s[1:].isdigit())

row = "1816670	Beijing	Beijing	BJS,Bac Kinh,Baek-ging,Baekging,Behehzhin,Beijing,Beijing City,Beijing Shi,Beising,Beixin,Beixín,Bejdzing,Bejdżing,Bejing,Beyjing,Beȝcinȝ,Báe̤k-gĭng,Béising,Bắc Kinh,Pechin,Pechino,Pechinu,Pechinum,Pecinum,Pei-ching,Pei-ching-shih,Pei-p'ing,Pei-p'ing-shih,Peken,Pekin,Pekin',Pekina,Pekinas,Peking,Pekini,Pekino,Pekín,Pekîn,Peping,Pequim,Pequin,Pequín,Pet-kin,Pet-kîn,Peycing,Pikkin,Pèquin,Pékin,Péqùin,Péycing,be'ijim,be'ijina,be'ijinga,bei jing,bei jing shi,beidjin,beijing,bijiga,bijing,bijinga,bkyn,buggyeong,byjng,bykyn,byyg'yng,byyzsyng,pakking,peyjin,pkn,Πεκίνο,Бейжің,Бээжин,Бәәҗң балһсн,Пекин,Пекинг,Пекін,Пекінґ,Պեկին,בייג'ינג,בייזשינג,بكين,بيكين,بیجنگ,بېجینګ,بېيجىڭ,بېيجىڭ شەھىرى,پکن,پێکەن,ބީޖިންގ,बीजिंग,बेइजिङ,বেইজিং,ਬੀਜਿੰਗ,બેઇજિંગ,பெய்ஜிங்,బీజింగ్,ಬೀಜಿಂಗ್,ബെയ്‌ജിങ്ങ്‌,බෙයිජිං,ปักกิ่ง,པེ་ཅིང་གྲོང་ཁྱེར།,ပေကျင်းမြို့,პეკინი,ቤዪጂንግ,ប៉េកាំង,北京,北京市,베이징,북경	39.9075	116.39723	P	PPLC	CN		22	11876380			18960744		49	Asia/Shanghai	2024-12-12"
row = "1786657	Yinchuan	Yinchuan	Gin-chhoan-chhi,Gîn-chhoan-chhī,Ho-lan,INC,In'chuan',Inchuan,Incuanas,Inčuanas,Jin-cchuan,Jin-čchuan,Jinchuan,Ngan Xuyen,Ngung-chiong,Ngân Xuyên,Ngṳ̀ng-chiŏng,Ning-hsia,Ningsia,Ningsia-hsien,Ningsiafu,Thanh pho Ngan Xuyen,Thành phố Ngân Xuyên,Yin-ch'uan-shih,Yin-ch’uan-shih,Yinchuan,Yinchuan Shi,Yinzconh,inchwan si,mdynt ynshwan,yin chuan,yin chuan shi,ynchwan,yynchwan,Їньчуань,Јинчуан,Инчуан,Иньчуань,مدينة ينشوان,يىنچۈئەن شەھىرى,ینچوآن,ینچوان,یینچوان,യിഞ്ചുവാൻ,ཡིན་ཁྲོའོན་གྲོང་ཁྱེར།,銀川,銀川市,银川,银川市,인촨 시	38.46806	106.27306	P	PPLA	CN		21	6401			1487579		1117	Asia/Shanghai	2023-12-29"
splits = row.replace('	'," ").replace(","," ").split(" ")
# ss = splits.copy()
# for s in splits:
#     sss = s.split(",")
#     ss.extend(sss)
print(splits)

@dataclass
class Data:
    id:int = None
    name:str = None
    longitude:float = None
    latitude:float = None

datalist = []

def parse_row(splits:list):
    data = Data()
    for s in splits:
        if data.id is None and is_integer(s):
            data.id = int(s)
            continue
        if data.name is None and is_all_chinese(s):
            data.name = s
            continue
        if data.longitude is None and is_float(s):
            data.longitude = float(s)
            continue
        if data.latitude is None and is_float(s):
            data.latitude = float(s)
            continue
    datalist.append(data)

print("done")
print("done")
print("done")
print("done")