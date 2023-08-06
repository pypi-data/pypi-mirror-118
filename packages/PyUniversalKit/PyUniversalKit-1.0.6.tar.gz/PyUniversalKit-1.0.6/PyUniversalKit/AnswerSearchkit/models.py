from typing import Dict
from PyUniversalKit import CSVkit
from .error import AdminRunError
"""
---------------------------------------------------------------------------------------------
The models.py file holds the project matching rules and the default settings
In the match rules class you can add new regular expressions and decide whether they need to be returned or not.
In the default settings class you can customize methods or properties to access the privacy settings data, plus you can set and add.

* First data screening rules

* Default interface

* List of supported interfaces

* Default Cookie
---------------------------------------------------------------------------------------------

"""

class Match(object):
    def __init__(self):
        # Custom rules need to be added to this again
        self.all_return = [self.__general(),self.__discussion_1(),self.__discussion_2()]

    @staticmethod
    def __general() -> Dict:
        kind = "RE"
        reg = r'<h3 class="mark_name colorDeep">([\S\s]*?)</h3>'
        reg_dict = {
            "kind":kind,
            "reg":reg
        }
        return reg_dict


    @staticmethod
    def __discussion_1() -> Dict:
        kind = "RE"
        reg = r'"content":"(.*?)"'
        reg_dict = {
            "kind": kind,
            "reg": reg
        }
        return reg_dict

    @staticmethod
    def __discussion_2() -> Dict:
        kind = "RE"
        reg = r'"title":"(.*?)"'
        reg_dict = {
            "kind": kind,
            "reg": reg
        }
        return reg_dict

    # Add new matching rules here (via decorators)


    @property
    def return_all_match(self) -> list:
        return self.all_return


class DefaultSetting(object):
    def __init__(self):
        self.setting = {
            "default_API": "icodef",
            "API_Support": ["icodef"],
            "default_cookie_Chaoxing": "Add your own cookie",
            # Add more setting here
        }

        # First data filtering rules -- RE
        """
        self.re_replace_rules = [
            # Matching (1) class
            r'[(（\[]/d+[)）\]]'
        ]
        """

        # First data filtering rules
        self.replace_rules = {
            "\n": "",
            "&nbsp;": "",
            " ": "",
            "(单选题)": "",
            "(多选题)": "",
            "(填空题)": "",
            "(判断题)": "",
            "[判断题]": "",
            "(简答题)": "",
            "(计算题)": "",
            "(单选题,": "",
            "(单选题": "",
            "(其它)": "",
            "(10分)": "",
            "10分)": "",
            "10分": "",
            "简答题":"",
            "(简答题":"",
            "*":"",
            "&": "",
            "@": "",
            "(":"",
            ")": "",
            # Add more rules here to

        }

    @property
    def default_api(self) -> str:
        return self.setting["default_API"]

    @property
    def default_cookie_Chaoxing(self) -> str:
        return self.setting["default_cookie_Chaoxing"]

    @property
    def api_support(self) -> list:
        return self.setting["API_Support"]

    @property
    def api_icodef(self) -> list:
        # API address and rules
        # [API address , [params of post...]]
        return ["https://cx.icodef.com/v2/answer",["topic[0]"]]

    # Add more API interface here




class Mapping():

    # This method will be loaded every time it is run
    def setting_mapping(self,api_type,header:list) -> bool:
        try:
            CSVkit.write(PATH="%s.csv" % api_type, header=header, rows=[[]])
            return True
        except:
            raise AdminRunError(api_type)





