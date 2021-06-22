import re

SYNONYMS_LOYALTY = ['лояльность', 'верность', 'лоялка', 'лоялочка', 'лояльности', 'лоялки']
SYNONYMS_QUALITY = ['уж', 'у', 'уровень', 'уровень жизни', 'уровень жызни', 'уровеньжизни']
SYNONYMS_CULTURE = ['ок', 'очки культуры', 'очков культуры', 'культуры', 'культура', 'очков']
SYNONYMS_STABILITY = ['стабильность', 'стаба', 'стабильности', 'стабы']
SYNONYMS_GROWTH = ['прирост', 'прирост населения', 'прироста', 'прироста населения']
SYNONYMS_PEOPLE = ['население', 'населения']
INDUSTRIES = ['сельское хозяйство', 'лесозаготовка', 'горное дело', 'военное дело', 'ремесло', 'логистика',
              'строительство', 'география', 'медицина', 'кузнечное дело', 'лесной промысел', 'морской промысел',
              'металлообработка', 'кораблестроение']


def delete_extra_spaces(string):
    if not string or string == " ":
        return string
    string = re.sub(' +', ' ', string)
    while string[0] == " ":
        string = string[1:]
    while string[-1] == " ":
        string = string[:-1:]
    return string


class Verdict:
    def __init__(self, qol=0, loyalty=0, stability=0, growth=0, culture=0, people=0):
        self.loyalty = loyalty
        self.qol = qol
        self.culture = culture
        self.stability = stability
        self.growth = growth
        self.people = people

    def parse_line(self, line):
        line = delete_extra_spaces(line)
        if ':' in line:
            name, effect = line.split(':')
        else:
            res = re.findall(r'\d{1,5}', line)
            if res:
                return "001"  # В строке есть числа, но не введён сепаратор
            else:
                return "005"  # В строке нет чисел и сепаратора, работать не с чем
        sign = 1
        if '+' in effect:
            effect = effect.replace('+', '')
        elif '-' in effect:
            effect = effect.replace('-', '')
            sign = -1
        res = re.findall(r'\d{1,5}', effect)
        if len(res) > 1:
            return "002"  # В строке больше одного числа
        elif res:
            num = res[0]
            if name.lower() in SYNONYMS_LOYALTY:
                self.loyalty += sign*float(num)
            elif name.lower() in SYNONYMS_QUALITY:
                self.qol += sign*float(num)
            elif name.lower() in SYNONYMS_CULTURE:
                self.culture += sign*float(num)
            elif name.lower() in SYNONYMS_STABILITY:
                self.stability += sign*float(num)
            elif name.lower() in SYNONYMS_GROWTH:
                self.growth += sign*float(num)
            elif name.lower() in SYNONYMS_PEOPLE:
                self.people += sign*float(num)
            elif name.lower() in INDUSTRIES:
                setattr(self, name, sign*float(num))
            elif '?' in name:
                setattr(self, name.replace("?", ""), sign*float(num))
            elif '(' in name or ')' in name:
                return "006"
            else:
                return "003"  # Введена подотрасль или ошибка в написании
        else:
            return "004"  # В строке есть сепаратор, но нет чисел, работать не с чем
        return "000"


def parse(lines):
    verd = Verdict()
    for line in lines:
        res = verd.parse_line(line=line)
        if res == "000":
            pass
        elif res == "001":
            return "Ошибка 001. Отсутствует сепаратор ':' в строке '" + line + "'"
        elif res == "002":
            return "Ошибка 002. Введено несколько чисел после сепаратора в строке '" + line + "'"
        elif res == "003":
            return "Ошибка 003. Введена подотрасль в строке '" + line + \
                   "' вместо отрасли, или отрасль написана с ошибкой.\n" + \
                   "Ознакомьтесь со списком доступных отраслей: " + ', '.join(INDUSTRIES)
        elif res == "006":
            return "Ошибка 006. Введён уровень отрасли в строке '" + line + "'. Напишите эту отрасль без уровня."
    return verd
