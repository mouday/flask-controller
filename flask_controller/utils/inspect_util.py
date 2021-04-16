# -*- coding: utf-8 -*-
import importlib
import inspect
import pkgutil


def iter_module_name(package_name: str):
    """
    :param package_name:
    :return: module_name
    """
    package = importlib.import_module(package_name)

    for _, module_name, is_pkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + "."):

        if not is_pkg:
            yield module_name


def iter_subclass(module_name, super_class):
    """
    :param module_name:
    :param super_class:
    :return: class_name, clazz
    """
    module = importlib.import_module(module_name)

    def is_subclass(obj):
        return inspect.isclass(obj) and issubclass(obj, super_class)

    yield from inspect.getmembers(module, is_subclass)


def iter_method(obj):
    """
    :param obj:
    :return: method_name, method
    """
    yield from inspect.getmembers(obj, inspect.ismethod)


# flask 支持的类型装换器(已知)
converter_mapping = {
    'str': 'string',  # （缺省值） 接受任何不包含斜杠的文本
    'int': 'int',  # 接受正整数
    'float': 'float',  # 接受正浮点数
    'path': 'path',  # 类似 string ，但可以包含斜杠
    'uuid': 'uuid',  # 接受 UUID 字符串
}


def get_signature_url(method):
    """获取方法签名参数"""

    global converter_mapping

    signature = inspect.getfullargspec(method)
    # print(signature)

    lst = []
    for param in signature.args:
        if param == 'self':
            continue

        param_type = signature.annotations.get(param)

        if param_type:
            param_type_name = converter_mapping.get(param_type.__name__, param_type.__name__)
            lst.append(f'<{param_type_name}:{param}>')
        else:
            lst.append(f'<{param}>')

    return '/'.join(lst)
