mycroft-stt-plugin-elhuyar
==========================

This STT service for Mycroft requires credentials for accessing Elhuyar STT API. The access to the API is free for developers.

Configuration parameters (only the credentials are mandatory, others are defaulted as in the following) ::

    "stt": {
        "module": "elhuyar_stt",
        "elhuyar_stt": {
            "api_id": "insert_your_api_id_here",
            "api_key": "insert_your_api_key_here"
        }
    }

Installation
------------

::

    mycroft-pip install mycroft-stt-plugin-elhuyar

License
-------

Apache-2.0
