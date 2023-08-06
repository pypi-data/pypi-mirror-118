# Copyright 2021 Elhuyar
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests

from mycroft.tts import TTS, TTSValidator
from mycroft.util.log import LOG


supported_langs = ['eu-eu']


class ElhuyarTTSPlugin(TTS):
    """Interface to Elhuyar TTS"""

    def __init__(self, lang, config):
        super(ElhuyarTTSPlugin, self).__init__(lang,
                                               config,
                                               ElhuyarTTSValidator(self),
                                               'wav')
        self.token = config.get('token')
        self.gender = config.get('gender', 'M')
        self.speed = config.get('speed', 100)

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio from Elhuyar

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None) # No phonemes
        """

        url_elhuyar = 'http://tts.elhuyar.eus/ahots_sintesia/ahots_sintesia/'
        headers = {
            'User-Agent': 'mycroft'
        }
        request_data = {
            'testua': sentence.encode('utf-8'),
            'kodea': self.token,
            'speed': self.speed,
            'gender': self.gender,
            # Lang for Elhuyar TTS:`eu-eu` -> `eu`
            'hizkuntza': self.lang.split('-')[0],
            'response': 'wav'
        }
        response = requests.post(url_elhuyar, headers=headers, data=request_data)
        if response.status_code == 200:
            with open(wav_file, "wb") as f:
                f.write(response.content)
                return wav_file, None
        else:
            LOG.error("Status code: " + str(response.status_code) +
                      " Error. Reason: " + str(response.reason))


class ElhuyarTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(ElhuyarTTSValidator, self).__init__(tts)

    def validate_lang(self):
        lang = self.tts.lang
        if lang.lower() not in supported_langs:
            raise ValueError("Language not supported by Elhuyar TTS: {}"
                             .format(lang))

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return ElhuyarTTSPlugin
