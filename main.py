import vk_api, re
from vk_api.longpoll import VkLongPoll, VkEventType
from verdict_parser import parse, delete_extra_spaces, Verdict

TOKEN = "dbe14b98801eb3e9a3430f8f70a113ded1e1fd4370b9177445e9bc5c1b50d3af67d703a018378c9191934"
TOKEN_2 = "3a27673d3a27673d3a27673d353a5f5a1e33a273a27673d5ae0e8da8ccf8e4114bb5414"
EM_DASH = chr(8212)
NON_BREAKING_SPACE = chr(160)
GROUP_ID = 144590331
RESOURCES_INDUSTRIES = ["сельское хозяйство", "лесозаготовка", "горное дело", "металлургия"]


def blasthack(id, text):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


bh = vk_api.VkApi(token=TOKEN)
bh_2 = vk_api.VkApi(token=TOKEN_2)
vk = bh.get_api()
vk_2 = bh_2.get_api()
longpoll = VkLongPoll(bh)


def process_request(text):
    name_country = delete_extra_spaces(text.split('\n')[0])
    pars = parse(text.split('\n')[1:])
    if type(pars) == str:
        return pars
    elif type(pars) == Verdict:
        topics = vk_2.board.getTopics(group_id=GROUP_ID, count=100)['items']
        topic_id = ""
        for topic in topics:
            title = topic['title']
            if EM_DASH in title:
                name = delete_extra_spaces(title.split(EM_DASH)[1])
                if name_country.lower() == name.lower():
                    topic_id = topic['id']
        if topic_id:
            topic_header = vk_2.board.getComments(group_id=GROUP_ID, topic_id=topic_id)['items'][0]['text'].split('\n')
            start_index = 0
            end_index = 0
            qol_index = 0
            loy_index = 0
            stab_index = 0
            cul_index = 0
            industries_index = 0
            growth_index = 0
            for index, line in enumerate(topic_header):
                if 'Население' in line:
                    start_index = index
                elif 'Достижения' in line:
                    end_index = index - 1
                elif 'Уровень жизни' in line:
                    qol_index = index
                elif 'Лояльность' in line:
                    loy_index = index
                elif 'Стабильность' in line:
                    stab_index = index
                elif 'Культура' in line:
                    cul_index = index
                elif 'Развитие отраслей' in line:
                    industries_index = index
                elif 'Прирост населения' in line:
                    growth_index = index
            msg_topic_error = ""
            if start_index == 0:
                msg_topic_error += "Не найдена строка 'Население'\n"
            if end_index == 0:
                msg_topic_error += "Не найдена строка 'Достижения'\n"
            if qol_index == 0:
                msg_topic_error += "Не найдена строка 'Уровень жизни'\n"
            if loy_index == 0:
                msg_topic_error += "Не найдена строка 'Лояльность'\n"
            if stab_index == 0:
                msg_topic_error += "Не найдена строка 'Стабильность'\n"
            if cul_index == 0:
                msg_topic_error += "Не найдена строка 'Культура'\n"
            if industries_index == 0:
                msg_topic_error += "Не найдена строка 'Развитие отраслей'\n"
            if growth_index == 0:
                msg_topic_error += "Не найдена строка 'Прирост населения'\n"
            if msg_topic_error:
                return msg_topic_error + "Обратитесь к администратору."

            if pars.qol != 0:
                qol = re.findall(r'\d{1,3}%', topic_header[qol_index])[0][:-1]
                new_qol = int(qol) + int(pars.qol)
                if new_qol > 100:
                    new_qol = 100
                topic_header[qol_index] = re.sub(r'\d{1,3}%', str(new_qol) + '%', topic_header[qol_index])

            if pars.loyalty != 0:
                loyalty = re.findall(r'\d{1,3}%', topic_header[loy_index])[0][:-1]
                new_loyalty = int(loyalty) + int(pars.loyalty)
                if new_loyalty > 100:
                    new_loyalty = 100
                topic_header[loy_index] = re.sub(r'\d{1,3}%', str(new_loyalty) + '%', topic_header[loy_index])

            if pars.stability != 0:
                stability = re.findall(r'\d{1,3}%', topic_header[stab_index])[0][:-1]
                new_stability = int(stability) + int(pars.stability)
                if new_stability > 100:
                    new_stability = 100
                topic_header[stab_index] = re.sub(r'\d{1,3}%', str(new_stability) + '%', topic_header[stab_index])

            if pars.growth != 0:
                growth = re.findall(r'\(\d{1,6}\)', topic_header[growth_index].replace(" ", "").replace(NON_BREAKING_SPACE, ""))[0][:-1][1:]
                new_growth = int(growth) + int(pars.growth)
                topic_header[growth_index] = re.sub(r'\(\d{1,6}\)', str(new_growth), topic_header[growth_index].replace(NON_BREAKING_SPACE, ""))

            if pars.culture != 0:
                cul = re.findall(r'\(\d{1,4}\)', topic_header[cul_index])[0][:-1][1:]
                new_cult = int(cul) + int(pars.culture)
                topic_header[cul_index] = re.sub(r'\(\d{1,4}\)', '(' + str(new_cult) + ')', topic_header[cul_index])

            if pars.people != 0:
                people = re.findall(r'\d{1,6}', topic_header[start_index])[0]
                new_people = int(people) + int(pars.people)
                topic_header[start_index] = re.sub(r'\d{1,6}', str(new_people), topic_header[start_index].replace(NON_BREAKING_SPACE, ""))

            for industry in dir(pars):
                if not (industry.startswith('__')) and not (industry in ('qol', 'name', 'loyalty', 'culture',
                                                                         'stability', 'growth', 'parse_line', 'people')):
                    is_update = False
                    for index, ind in enumerate(topic_header[industries_index:end_index]):
                        if industry.lower() in ind.lower():
                            x = re.findall(r'\d{1,3}.\d{1,2}%', ind)
                            if not x:
                                x = re.findall(r'\d{1,3}%', ind)
                                if not x:
                                    return "Вы ввели подотрасль '" + ind + "'. Введите её основную отрасль"
                                new_x = int(x[0][:-1]) + int(getattr(pars, industry))
                                if new_x > 100:
                                    if industry in RESOURCES_INDUSTRIES:
                                        new_x -= 100
                                        level = int(re.findall(r'\(\d{1,2}\)%', ind)[0])
                                        topic_header[industries_index + index] = re.sub(r'\(\d{1,2}\)%', str(level + 1)
                                                                                        + '%', ind)
                                    else:
                                        new_x = 100
                                topic_header[industries_index + index] = re.sub(r'\d{1,3}%', str(new_x) + '%', ind)
                            else:
                                new_x = float(x[0][:-1]) + float(getattr(pars, industry))
                                if new_x > 100:
                                    if industry in RESOURCES_INDUSTRIES:
                                        new_x -= 100
                                        level = int(re.findall(r'\(\d{1,2}\)%', ind)[0])
                                        topic_header[industries_index + index] = re.sub(r'\(\d{1,2}\)%', str(level + 1)
                                                                                        + '%', ind)
                                    else:
                                        new_x = 100
                                topic_header[industries_index + index] = re.sub(r'\d{1,3}.\d{0,2}%', str(new_x) + '%', ind)
                            is_update = True
                    if not is_update:
                        topic_header.insert(end_index,
                                            '- ' + str(industry) + ': ' + str(int(getattr(pars, industry))) + '%')
                        end_index += 1

            return '\n'.join(topic_header[start_index:end_index])
        else:
            return "Страна " + name_country + " не найдена"
    else:
        return "Произошла непредвиденная ошибка обработки. Обратитесь к администратору"


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            text = event.text
            msg = process_request(text)
            id = event.user_id
            blasthack(id, msg)
