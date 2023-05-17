import os

import openai
from utils import File, Log, hashx

COMMAND = '''
You are a text humanizer.
Your job is to rewrite text provided earlier by the user
such that a lay-person can easily understand.
'''

log = Log('Humanizer')


class Humanizer:
    def translate_nocache(content_lines: list[str]) -> str:
        openai.api_key = os.environ["OPENAI_API_KEY"]
        messages = [
            dict(role="user", content=content) for content in content_lines
        ] + [
            dict(
                role="system",
                content=COMMAND,
            ),
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = response['choices'][0]['message']['content']
        m = len(reply)
        log.debug(f'Humanized to {m} chars')
        return reply

    def translate(content_lines: list[str]) -> str:
        content = '\n'.join(content_lines)
        hash = hashx.md5(content)[:6]
        tmp_path = os.path.join('data_tmp', f'{hash}.txt')
        tmp_file = File(tmp_path)
        if os.path.exists(tmp_path):
            reply = tmp_file.read()
        else:
            reply = Humanizer.translate_nocache(content_lines)
            tmp_file.write(reply)
        return reply
