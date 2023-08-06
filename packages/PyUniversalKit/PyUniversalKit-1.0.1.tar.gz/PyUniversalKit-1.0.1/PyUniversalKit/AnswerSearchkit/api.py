from .operate import QSobject
from .error import ApiTypeError
from .models import DefaultSetting
from .struct import AnswerObject


def search(url:str,**kwargs) -> AnswerObject:
    """

    :param url: Str
    :param kwargs: API:Str cookie:Str
    :return: PrettyTable Object

    * The search() method contains one required parameter url, optional parameters API (the source of the search API), cookie (the main credentials for logging in, default cookie
      in `models.DefaultSetting().setting["default_cookie_Chaoxing"])`


    """
    # Make default settings
    if 'API' not in kwargs:
        kwargs.setdefault("API",DefaultSetting().default_api)
    if 'cookie' not in kwargs:
        kwargs.setdefault("cookie",DefaultSetting().default_cookie_Chaoxing)
    # Verify that the API interface is supported
    if kwargs["API"] not in DefaultSetting().api_support:
        raise ApiTypeError(kwargs["icodef"])
    print("You are using AnswerSearchkit {}, please wait for the program to finish...".format("1.0.0 Beta"))
    return QSobject().search_question(url,**kwargs)