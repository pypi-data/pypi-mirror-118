# AuthCore

The simple membership system for cross-platform application.

# Member System
#### SERVER: setup a member system
```
# 啟動系統(則一使用)

import AuthCore as ac

## Using Json File
itf = ac.SimpleMemberSystem(db_file_path="./")

## Using MongoDB Cloud
itf = ac.MongoDBMemberSystem(account_label="<account_label>", user="<user>", pws="<pws>", collection="<collection>")

```

#### APP: sign up for third-part application
```
# 註冊平台
decode_key, label = itf.signup_platform()

```


#### SERVER: signup a user
```
# 註冊會員
account = "root"
pws = "root"
itf.signup_user(account, pws)

## Raise RuntimeError if user exist
```

#### SERVER: update info of the user
```
# update or increase info of user
data = {
            "var1": idx,
            "var2": idx,
            "var3": idx,
        }
itf.update_user(account, pws, **data)
```

#### APP: login as user
```
from AuthCore import DecryptITF

# the label from the step 1 (setup a member system)
# decode_key from the step 1 (setup a member system)

# user login
### Raise RuntimeError if user is did NOT exist
encode_text = itf.login_user(label, "root", "root")  

# decode the secret user info
decode_text = DecryptITF.decrypt(decode_key, encode_text) 
print(f"解析會員資料： decode_text:{decode_text}")
```

#### SERVER: Delete a user
```
# Delete a user
itf.delete_user(account, pws)
```

# Other:

#### 連接至DB
```
from AuthCore.sdb import mongo
db = mongo.MongoDBInterface("ooglx")
db.select_table("unittest", "user")
```
#### 新增資料
```
db.__insert__("user1", {"a": 1, "b": 2})
result = db.__select__("user1")
```
#### 搜索資料
```
result = db.__select__("user1")
```
#### 更新資料
```
db.__update__("user1", {"var1": 1, "var2": 2})
result = db.__select__("user1")
```

#### 刪除資料
```
db.__remove__("user1")
result = db.__select__("user1")
```