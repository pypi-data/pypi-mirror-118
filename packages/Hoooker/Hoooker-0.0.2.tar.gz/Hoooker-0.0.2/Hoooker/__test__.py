from .line import LineBITF
access_token = "o2pl0G+tEnXvNGzwClmznpGKW4KCZzl+2NfdtId0tDckPQ3S4zF/DV4tJ+wqp0swUx/a+KRMDyhVLvzW+jtMLs2YU4AdFMvgOOcc0TaEK+4CmhHVzGLAz23Ehpf+wnE9uFXwdaf96XYFVT7tp8w5awdB04t89/1O/w1cDnyilFU="
channel_secret = "94122457a33431246cadb4d563aae80f"
cil = LineBITF(access_token, channel_secret)
res = cil.push("U3d11778af2bfc34907f58719ed30d076", "hi")
print(res.text)


res = cil.get_user_info("U3d11778af2bfc34907f58719ed30d076")
print(res)