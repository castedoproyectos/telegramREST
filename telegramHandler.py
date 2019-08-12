from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import GetHistoryRequest

import json

from mensaje import Mensaje
import time


class TelegramHandler(object):

    def __init__(self):
        self._list_msn = list()

        self.config_file = "config.json"
        self._read_config()


        self._sesion_name = "test"
        self._hash_id = "526632"
        self._hash_num = "eeb7b94dc683848287857f8bfa03aa58"

        self._client = TelegramClient(self._sesion_name, self._hash_id, self._hash_num)
        self._client.start()
        self._channel_entity = self._client.get_entity('https://t.me/joinchat/AAAAAEovusdyxSfqrfCy2A')

    def _read_config(self):
        with open(self.config_file) as json_file:
            data = json.load(json_file)

            self._sesion_name = data['sesion_name']
            self._hash_id = data['hash_id']
            self._hash_num = data['hash_num']
            self._channel_entity = data['channel_entity']

            json_file.close()

    def _get_messages_telegram(self, num_msn):
        posts = self._client(GetHistoryRequest(
            peer=self._channel_entity,
            limit=100,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0))

        return posts.messages[:]


    def _parse_messages_telegram(self, messages):
        parse_messages = list()
        for i in range(len(messages)):
            id = messages[i].id
            datetime = messages[i].date
            text = messages[i].message
            id_parent = messages[i].reply_to_msg_id
            if text is not None:
                parse_messages.append(Mensaje(id=id, datetime=datetime, text=text, id_parent=id_parent))

        return parse_messages


    def _filter_new_msn(self, list_msn):
        list_new_msn = list()
        if len(self._list_msn) > 0:
            list_date_time = list()
            for item in self._list_msn:
                list_date_time.append(item.datetime)

            for msn in list_msn:
                if msn.datetime not in list_date_time:
                    list_new_msn.append(msn)

        return list_new_msn


    def get_msn(self, num_msn):
        msn_rcv = self._get_messages_telegram(num_msn=num_msn)
        msn_parse = self._parse_messages_telegram(messages=msn_rcv)
        msn_new = self._filter_new_msn(list_msn=msn_parse)

        self._list_msn.extend(msn_new)



if __name__ == '__main__':
    th = TelegramHandler()

    while True:
        print("Buscando nuevos mensajes...")
        msn = th.get_msn(10)
        time.sleep(5)
