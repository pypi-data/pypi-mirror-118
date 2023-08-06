#hooker

##Line
### webhook
```python
from Hoooker.line import LineBITF
access_token = ""
channel_secret = ""
line_bot_api = LineBITF(access_token, channel_secret)
```

```python
content = line_bot_api.get_content(request)
```
```python
line_bot_api.reply([re_text], reply_token)
```
```python
res = line_bot_api.push(userId, "hi")
```
```python
res = line_bot_api.get_user_info(userId)
```

