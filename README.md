# flask-controller

![PyPI](https://img.shields.io/pypi/v/flask-controller.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/flask-controller)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-controller)
![PyPI - License](https://img.shields.io/pypi/l/flask-controller)

- Github: [https://github.com/mouday/cator](https://github.com/mouday/flask-controller)
- Pypi: [https://pypi.org/project/cator](https://pypi.org/project/flask-controller)

## 简介

flask-controller 简化Flask开发，自动路由注册，以类的形式管理控制器

支持多层扫描

## 安装

```bash
pip install flask-controller
```

## 使用示例

项目结构
```
.
└── flask_app
    ├── controllers
    │   ├── __init__.py
    │   ├── admin
    │   │   ├── __init__.py
    │   │   └── login_controller.py
    │   ├── index_controller.py
    │   └── user_controller.py
    └── main.py

```

文件内容


flask_app/controllers/index_controller.py
```python
# -*- coding: utf-8 -*-
from flask_controller import FlaskController


class IndexController(FlaskController):

    def index(self):
        return 'index'

```
flask_app/controllers/user_controller.py
```python
# -*- coding: utf-8 -*-
from flask_controller import FlaskController


class UserController(FlaskController):

    def user_name(self, name, age: int = 23):
        return 'username'

```

flask_app/controllers/admin/login_controller.py
```python
# -*- coding: utf-8 -*-
from flask_controller import FlaskController


class LoginController(FlaskController):
    def index(self):
        return 'Login index'

```

flask_app/main.py
```python
# -*- coding: utf-8 -*-


from flask import Flask

from flask_controller import FlaskControllerRegister

app = Flask(__name__, static_folder=None)


# 自动注册路由
register = FlaskControllerRegister(app)

register.register_package('flask_app.controllers')

```


注册结果
``
Map([
 <Rule '/admin/login/index' (OPTIONS, GET, HEAD, POST) -> admin.login.index>,
 <Rule '/index/index' (OPTIONS, GET, HEAD, POST) -> index.index>,
 <Rule '/user/user_name/<name>/<age>' (OPTIONS, GET, HEAD, POST) -> user.user_name>
])
``