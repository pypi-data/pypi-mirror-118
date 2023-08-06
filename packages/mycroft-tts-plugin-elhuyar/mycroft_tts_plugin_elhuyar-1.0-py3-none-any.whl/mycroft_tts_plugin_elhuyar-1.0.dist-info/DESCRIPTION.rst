mycroft-tts-plugin-elhuyar
==========================

This TTS service for Mycroft requires a token for accessing Elhuyar TTS API. The access to the API is free for developers.

Configuration parameters (only the token is mandatory, others are defaulted as in the following) ::

    "tts": {
        "module": "elhuyar_tts",
        "elhuyar_tts": {
            "token": "insert_your_token_here",
            "genre": "M", # optional, F or M, defaults to M
            "speed": 100 # optional, defaults to 100)
        }
    }

Installation
------------

::

    mycroft-pip install mycroft-tts-plugin-elhuyar`

License
-------

Apache-2.0


