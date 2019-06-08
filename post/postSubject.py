# 发表主题贴
import sys
sys.path.append("..")
from Model import session, User

a=session.query(User).first()
print(a.uid) #14
