# PyUniversalKit工具包

#### Hello,PyUniversalKit!

## 下载方式
> `pip install PyUniversalKit` 

## 支持
<a href="https://pypi.org/project/PyUniversalKit/"><img src="https://warehouse-camo.ingress.cmh1.psfhosted.org/047074c34350165c9a6a57b844a2390d638c173d/68747470733a2f2f6769746875622e636f6d2f6a696e612d61692f6a696e612f626c6f622f6d61737465722f2e6769746875622f6261646765732f707974686f6e2d62616467652e7376673f7261773d74727565"></a>

## 工具包内容

* ### AnswerSearchkit
  #### AnswerSearchkit工具包是为了满足网页快速搜题需求。输入匹配规则以及url，将会自动获取该页面全部题目并提供搜索，目前提供search()一个方法
  示例
  > * `from PyUniversalKit import Netkit,AnswerSearchkit`
  > * `result = AnswerSearchkit.search(url="XXX",**kwargs)`
  > * `print(result.preview)`
  * #### 可选参数：API:str,cookie:str,*（默认cookie在models.py内更改）*
  `AnswerSearchkit.search`函数返回一个AnswerObject类型的类，其包含两个属性：
  * `.preview`: 返回一个*PrettyTable*格式的表
  * `.original_data`: 返回一个答案列表（二元嵌套数组）
  #### AnswerSearchkit工具包使用流程如下
  * 判断是否能使用AnswerSearchkit
    * 查看将要搜题的网页的HTML代码，若题目显示在HTML元素里，便可使用
  * 添加题目匹配规则
    * 可以选择Xpath或者正则表达式来添加规则。
    * 位置：`models.Match()`
  * 查看待搜索页面是否需要cookie，如果需要，前往`models.DefaultSetting`添加默认cookie
  * 如果需要预览搜题结果，请前往`admin.py`添加API映射Table。每一个API对应一个唯一的Table，在调用属性`.preview`时，数据将会根据你定义的格式显示，具体用法前往`admin.py`查看
  * 如果想使用其他API接口，请前往`interface.py`添加想要的函数，之后前往`models.DefaultSetting `，在`self.setting`的`API_Support`字段下添加新的API接口名称,并添加相应函数。


* ### CSVkit
  #### CSVkit工具包提供了多种便携的方法来操作CSV文件
  #### 提供方法：`read`，`write`,调用这两个方法会返回`CSVobjects`类型；
  #### 该类型主要属性有：
  * `.preview`: 返回一个*PrettyTable*格式的表，显示传入文件前1000行内容（不够1000行全部显示）
  * `.size`: 返回该文件的大小
  * `.modify_time`: 返回该文件的上次修改时间
  *  `.create_time`: 返回该文件的创建时间
  *  `.rows`: 返回文件的总行数
  *  `.columns`: 返回文件的总列数
  #### 主要方法有：
  * `specifyROW()`： 方法接受三个可选变量:start_num,end_num,equal，将会返回第start_num行与end_num行（不包括end_num）之间的CSV数据，若equal为True，end_num行的数据也会被返回
  #### 更多方法和属性的详细用法请阅读对应的*api.py*文件
  #### 示例
  >* `from PyUniversalKit import CSVkit`
  >* `csv_obj = CSVkit.read("/Users/macos/Downloads/2021zzuli模拟赛/C_hour.csv")`
  >* `print(csv_obj.specifyROW(start_num=3,end_num=4,equal=False))`
  >* `print(csv_obj.preview)`
  * 参数均为空的时候默认为0,all,True.
* ### Netkit
  #### 与requests库用法一致，自己去看源代码。
  
  
  ## 注意：本项目内置的API接口为<a href="https://github.com/CodFrm/cxmooc-tools">*超星慕课小工具*</a>,感谢这位创作者提供的接口
