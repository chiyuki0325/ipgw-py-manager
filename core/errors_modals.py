from enum import Enum
from typing import TypedDict

ua = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'''
target = '''https://pass.neu.edu.cn/tpass/login?service=https%3A%2F%2Fipgw.neu.edu.cn%2Fsrun_cas.php%3Fac_id%3D1'''


class UnionAuthError(Exception):
    def __init__(self, last_trial_times):
        self.last_trial_times = last_trial_times


class UnknownPageError(Exception):
    def __init__(self, page):
        self.page = page


# 出现“系统提示”，说明尝试次数已经上限
class AttemptReachLimitError(UnionAuthError):
    pass


# 在尝试登录之后，页面返回智慧东大，但是并没有提示密码错误次数的信息，这种奇怪的错误在这里报告。
class IntimateUnionAuthPageError(UnknownPageError):
    def __init__(self, page):
        self.page = page


# 登出指定设备需要CAS验证。
class RequestNeedCASAuthenticError(Exception):
    pass


# 在查询用户已经消费的流量或在线时长的时候，服务器返回not online错误。
class UserNotOnlineError(Exception):
    pass


class NoDefaultUserError(Exception):  # 没有找到默认用户的错误
    pass


class UsernameOrPasswordEmptyError(Exception):  # 用户名或者密码为空错误。
    pass


class UsernameNotInConfigFileError(Exception):  # 配置文件中查询不到提供的用户名，命令行中也没有提供密码，因此无法登录。
    pass


class EmptyLastLoginInfoError(Exception):  # 有关上次登录的信息为空，而用户却又请求使用上次登录的结果。
    pass


class NoCurrentDeviceError(Exception):  # 没有当前刚刚登录的设备信息。
    pass


class LoginResult(Enum):
    LoginSuccessful = 0
    UsernameOrPasswordError = 1
    AttemptReachLimit = 2


# SuccessPage的两个依赖
class PageStatus(Enum):
    Normal = 0
    ServiceDisabled = 1
    InsufficientFee = 2
    OtherDeviceOnline = 3
    Unknown = -1


class BaseInfo(TypedDict):
    student_number: str
    ip: str
    consume_bytes: int  # 已用流量
    online_time_sec: int  # 总在线时长
