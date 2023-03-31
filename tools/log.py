import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import date, timedelta, datetime

tfm = "%Y-%m-%d %H:%M:%S"
edit_cal = 0
msg_id = None


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='midnight', interval=1, backupCount=0):
        super().__init__(filename=filename, when=when, interval=interval, backupCount=backupCount, encoding="utf-8")
        self.namer = rotator_namer


def rotator_namer(filename):
    yesterday = (date.today() - timedelta(1)).isoformat()
    return filename.split('.log')[0] + '_' + yesterday + '.log'


async def log_message(backend, log_msg, guild=None, channel='Server', command=None):
    logging.getLogger('discord').info(f"【{guild}】{log_msg} ({channel})")
    prefix = f'[{datetime.now().strftime(tfm)}][INFO ][{channel}]'
    if command:
        content = f"+ {prefix} {log_msg}\n"
    elif command == 0:
        content = f"- {prefix} {log_msg}\n"
    else:
        content = f"{prefix} {log_msg}\n"

    global edit_cal, msg_id
    if edit_cal % 10 == 0:
        edit_cal = 0
        msg = await backend.send(f"```diff\n{content}```")
        msg_id = msg.id
    else:
        msg = await backend.fetch_message(msg_id)
        original_content = msg.content
        updated_content = original_content[:-3] + f"{content}```"
        await msg.edit(content=updated_content)
    edit_cal += 1
