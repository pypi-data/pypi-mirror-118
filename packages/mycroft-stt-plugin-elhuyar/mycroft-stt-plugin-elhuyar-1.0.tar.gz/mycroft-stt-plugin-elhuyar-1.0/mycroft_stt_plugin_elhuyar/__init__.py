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

import http
import json

from mycroft.stt import STT
from mycroft.util.log import LOG


supported_langs = ['eu-eu']


class ElhuyarSTTPlugin(STT):
    """Interface to Elhuyar STT"""

    def __init__(self):
        super(ElhuyarSTTPlugin, self).__init__()
        self.api_key = self.config.get("api_key")
        self.api_id = self.config.get("api_id")

    def execute(self, audio, language=None):
        language = language or self.lang
        if language.lower() not in supported_langs:
            raise ValueError(
                "Unsupported language '{}' for Elhuyar STT".format(language))
        if language.find('-') != -1:
            language = language[:language.find('-')]
        if len(language)>2:
            language = language[:2]
        uri = "live.aditu.eus"
        conn = http.client.HTTPSConnection(uri)
        conn.connect()
        url = "/"+language+"/client/http/recognize"
        conn.putrequest('POST', url)
        conn.putheader('Transfer-Encoding', 'chunked')
        conn.putheader('Content-Type', "audio/x-raw-int; rate=16000")
        conn.putheader('save', 'true')
        conn.endheaders()
        auth_message = "api_id=%s api_key=%s" % (self.api_id, self.api_key)
        conn.send(("%s" % (hex(len(auth_message))[2:])).encode() + b"\r\n")
        conn.send(auth_message.encode()+b"\r\n")
        chunk_size = int(1e10)
        audioData = audio.get_raw_data(convert_rate=16000, convert_width=2)
        if len(audioData) % chunk_size != 0:
            conn.send(
                ("%s" % (hex(len(audioData) % chunk_size)[2:])).encode()
                + b"\r\n"
            )
            conn.send(audioData[-(len(audioData) % chunk_size):] + b"\r\n")
        conn.send(b"0\r\n\r\n")
        resp = conn.getresponse()
        response_text = resp.read()
        conn.close()
        response_json = json.loads(response_text)
        transcript = response_json['hypotheses'][0]['transcript'].lower().rstrip('.')
        LOG.info(transcript)
        return transcript
