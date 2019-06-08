# 发表主题贴
import sys
sys.path.append("..")
import Model.*

DB = Model.DB()
a=DB.session.query(Model.DB.User).first()
print(a)
