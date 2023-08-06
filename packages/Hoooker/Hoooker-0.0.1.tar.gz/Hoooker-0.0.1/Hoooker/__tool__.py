import json
from typing import Union
from .message import TextMessage


def format_to_message(source: Union[str, dict, list, tuple]) -> [dict]:
    messages = ""
    if isinstance(source, str):
        messages = __smart_json_load__(source)
    elif isinstance(source, dict):
        source = json.dumps(source, ensure_ascii=False)
        messages = __smart_json_load__(source)
    elif isinstance(source, (list, tuple)):
        messages = []
        for s in source:
            messages += __smart_json_load__(str(s))

    return messages


def __smart_json_load__(obj_str: str) -> [dict]:
    if obj_str.startswith("{"):
        try:
            if "\"" not in obj_str:
                obj = json.loads(obj_str.replace("\'", "\""))
            else:
                obj = json.loads(obj_str)
            ms = obj
        except json.decoder.JSONDecodeError as e:
            ms = TextMessage(message_content=obj_str).to_line_format()
    else:
        ms = TextMessage(message_content=obj_str).to_line_format()

    return [ms]
