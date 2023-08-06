from PyUniversalKit import Netkit
from .models import DefaultSetting,Match
from PyUniversalKit.Netkit.models import TestResponse
from .struct import AnswerObject
from .error import MatchError,ApiTypeError,MatchTypeError,ThirdPackageImportError
from .interface import Interface
from typing import Dict
import re
try:
    from lxml import etree
except:
    raise ThirdPackageImportError("lxml")




class QSobject():

    def search_question(self,url:str,**kwargs) -> AnswerObject:
        def __get_Q_list(which: Dict, add_list: list,url_response:TestResponse) -> list:
            add_list.clear()
            kind = which["kind"]
            reg = which["reg"]
            if kind == "RE":
                # RE Type Matching Rules
                url_result = re.findall(reg, url_response.text)
                for each_result in url_result:
                    to_string = "".join(each_result[:])
                    drop_html = re.sub('<[^<+]+?>', '', to_string)

                    # First data filtering rules

                    for (key, val) in DefaultSetting().replace_rules.items():
                        drop_html = drop_html.replace(key, val)
                    add_list.append(drop_html)
                return add_list
            elif kind == "XPATH":
                # XPATH Matching Rules
                url_response = Netkit.get(url=url).text
                to_html = etree.HTML(url_response)
                url_result = to_html.xpath(reg)
                for each_result in url_result:
                    to_string = "".join(each_result[:])
                    drop_html = re.sub('<[^<+]+?>', '', to_string)

                    # First data filtering rules

                    for (key, val) in DefaultSetting().replace_rules.items():
                        drop_html = drop_html.replace(key, val)
                    add_list.append(drop_html)
                return add_list

            # Here you can add the corresponding data extraction method for the new match type
            else:

                raise MatchTypeError(kind, reg)




        API_type = kwargs["API"]
        cookie = kwargs["cookie"]

        # Call the properties of the match rule class to get all supported match rules
        Matchs = Match().return_all_match

        # Get HTML resource objects with the Net Toolkit
        url_response = Netkit.get(url=url,cookie=cookie)

        # Iterate through all the rules, break when a rule is feasible, compose
        # a list of filtered data and pass it to the _icodef function, which will
        # iterate through and search that list

        for every_matches in Matchs:
            # Return List
            return_match_list = __get_Q_list(every_matches,[],url_response)
            if len(return_match_list) == 0 or "" in return_match_list:
                pass
            else:

                if API_type == "icodef":
                    Anwser_list = Interface()._icodef(return_match_list, cookie)
                    return AnswerObject(_content=Anwser_list,_kind="icodef")


                # add more api type here
                else:
                    raise ApiTypeError(API_type)
        else:
            raise MatchError(_url=url)











