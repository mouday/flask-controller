# -*- coding: utf-8 -*-


from typing import Optional, Type

from .controller import FlaskController
from .utils import case_util, inspect_util


class FlaskControllerRegister:
    def __init__(self, app):
        self._app = app

    def register_package(self, package_name, url_prefix='/', **kwargs):
        """注册一个包"""
        for module_name in inspect_util.iter_module_name(package_name):
            package_prefix = self.get_package_prefix(package_name, module_name)
            # print(package_prefix)

            self.register_module(module_name, url_prefix=url_prefix + '/' + package_prefix, **kwargs)

    def register_module(self, module_name, **kwargs):
        """注册一个模块"""
        # print(module_name)

        for _, clazz in inspect_util.iter_subclass(module_name, super_class=FlaskController):
            # print(clazz)
            self.register_controller(controller=clazz, **kwargs)

    def register_controller(self, controller: FlaskController, url_prefix='/',
                            controller_suffix="Controller",
                            url_style: Optional[str] = 'snake',
                            methods=('GET', 'POST'),
                            **kwargs
                            ):
        """
        注册一个类到路由

        注册rule:      /类名/方法名
        注册endpoint:  类名.方法名


        :param controller:        controller子类
        :param url_prefix:        url前缀  ->  /url前缀/类名/方法名
        :param controller_suffix: controller子类的后缀，会被移除
        :param url_style:         url风格

            class UserController:
                def post_user_name(self):
                    pass

            转换规则：
                camel:   /user/postUserName
                kebab:   /user/post-user-name
                snake:   /user/post_user_name   [default默认]
                pascal:  /User/PostUserName
                upper:   /USER/POST_USER_NAME

        :param methods: 请求方法

        :return: None:
        """
        if not issubclass(controller, FlaskController):
            raise Exception('controller not FlaskController subclass')

        controller_name = self.get_controller_name(controller, controller_suffix)

        # 前缀
        prefixes = [pre for pre in url_prefix.split('/') if pre]
        # print(prefixes)

        # 实例化
        instance = controller()

        for method_name, method in inspect_util.iter_method(instance):
            names = self.get_url_names([*prefixes, controller_name, method_name], url_style=url_style)

            # 端点
            endpoint = '.'.join(names)

            # 后缀
            url_signature = inspect_util.get_signature_url(method)
            if url_signature:
                names.append(url_signature)

            rule = '/' + '/'.join(names)
            # print(endpoint, rule)

            self._app.add_url_rule(rule, endpoint=endpoint, view_func=method,
                                   methods=methods, **kwargs)

    def get_controller_name(self, controller: Type, controller_suffix: str = None):
        """切除后缀"""
        controller_name = controller.__name__
        if controller_suffix:
            controller_name = controller_name[0:-len(controller_suffix)]

        return controller_name

    def get_url_names(self, names, url_style: Optional[str] = None):
        """url"""
        return [case_util.case_to_case(name, url_style) for name in names]

    def get_package_prefix(self, package_name, module_name):
        """前缀"""
        return module_name[len(package_name) + 1: module_name.rindex('.')]
