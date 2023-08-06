__VERSION__ = '20210903.13'

from .Avatar import (
    Avatar,
    dict2avatar,
)

from .get_avatars import (
    get_avatars,
)

from .Talk import (
    Talk,
    TalkEffects,
    TalkEmotions,
    talk2dict,
)

from .talk_on_server import (
    talk_on_server,
    TalkOnServerResponse,
)

from .record_talk import (
    record_talk,
    RecordTalkResponse,
)

from .add_talk_arguments import (
    add_talk_arguments,
    add_talk_arguments_effects,
    add_talk_arguments_emotions,
)
