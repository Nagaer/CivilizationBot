import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "dbe14b98801eb3e9a3430f8f70a113ded1e1fd4370b9177445e9bc5c1b50d3af67d703a018378c9191934"


def blasthack(id, text):
    bh.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


bh = vk_api.VkApi(token=TOKEN)
vk = bh.get_api()
longpoll = VkLongPoll(bh)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            blasthack(id, msg)
