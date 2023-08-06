"""

This Is For Security Purpose Only
As Many Noobs Using Cheap Tricks To Hack userbot.
We here to save them

~ @TeamUltroid

"""

# Lol You Are So desperate.
# You came all here just to see this
# 😂😂😂😂

import os

wanted = ["SESSION", "REDIS_PASSWORD", "REDISPASSWORD", "HEROKU_API", "BOT_TOKEN"]


def cleanup_cache(var):
    os_stuff()
    for z in wanted:
        if z in list(var.__dict__.keys()):
            setattr(var, z, "")


def os_stuff():
    all = os.environ
    for z in list(all.keys()):
        if z in wanted:
            all.update({z: ""})


DANGER = [
    "SESSION",
    "HEROKU_API",
    "base64",
    "bash",
    "get_me()",
    "exec",
    "phone",
    "REDIS_PASSWORD",
    "load_addons",
    "load_plugins",
    "load_vc",
    "load_manager",
    "load_pmbot",
    "load_assistant",
    "plugin_loader",
    "os.system",
    "subprocess",
    "await locals()",
    "aexec",
    ".session.save()",
    ".auth_key.key",
    "INSTA_USERNAME",
    "INSTA_PASSWORD",
    "INSTA_SET",
]
