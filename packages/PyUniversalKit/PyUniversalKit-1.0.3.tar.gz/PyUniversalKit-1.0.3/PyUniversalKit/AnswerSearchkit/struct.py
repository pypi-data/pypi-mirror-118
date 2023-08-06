from .error import ThirdPackageImportError,AdminStyleError,AdminRunError
from .admin import mapping
from PyUniversalKit import CSVkit
import sys

try:
    from prettytable import PrettyTable
except:
    raise ThirdPackageImportError("prettytable")

class AnswerObject():
    def __init__(self,_content,_kind):
        self._content = _content
        self._kind = _kind
    @staticmethod
    def __iterator(start_num, end_num):
        while start_num < end_num:
            yield start_num
            start_num += 1

    def __return_table(self) -> PrettyTable:
        try:
            mapping_reload_flag = mapping[self._kind]
        except:
            raise AdminRunError(self._kind)

        print("\nAPI %s mapping reload complete.\n" % self._kind)

        if mapping_reload_flag == True:
            try:
                PATH = "%s.csv" % self._kind
                header = CSVkit.read(PATH).specifyROW()
                table = PrettyTable(header[0], encoding=sys.stdout.encoding)
                num = 1
                for i in self._content:
                    table.add_row(["%s." % num, i[0], i[1], i[2],self._kind])
                    num += 1

                return table
            except:
                raise AdminStyleError(self._kind)



    @property
    def preview(self) -> PrettyTable:
        return self.__return_table()

    @property
    def original_data(self) -> list:
        return self._content

