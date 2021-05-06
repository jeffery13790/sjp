1，所有命名全部为英文, 文件名全部小写单词之间使用“_”分隔开，所有命名以见名识意为目标。
	文件夹命名：模块_test	：search_to_cart_buy_good_test
	文件命名：  流程/动作_test.py  ：search_to_cart_buy_good_test.py
	类名称使用 TestCase动作/流程  类的名称使用驼峰模式：TestCaseSearchToCartBuyGood
	配置文件：
	公共配置文件使用：
	common.csv
	针对某一个文件以及某一个函数的配置文件
	文件_函数.csv

2，在每个类的Config("备注")的备注替换成该类的说明，让后续的人员可以通过这个备注就知道你这个用例干了什么事情。

3，debugtalk.py中只写公用的函数，不写私有的函数，私有的参数放在 'temp_name':["springfall", "springfall1"]  
	或者 "phoneNumber-verifyCode": "${parameterize(**.csv)}",这两种形式，第二种形式的**.csv文件和脚本文件放在
	同一个文件家下面，和py文件取相同的文件名
4. 代码精简，代码中的头文件部分尽量减少，可以只填写swagger中要求的必要的字段，方便后续代码查看。
5，在代码顶端可以写上自己的名字（此条为建议项）
	
注意：如果文件名过长的话，后面的几个单词使用简写（取单词的首字母放在一起），类似类的名称过长的时候也是这样。
每个项目只能有一个debugtalk.py 放在项目的最外层文件夹中，脚本在运行的时候默认吧debugtalk.py所在的目录作为根目录。
