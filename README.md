### [人人网小黄鸡](http://www.renren.com/601621937)

* 可以通过在状态里@它或者回复它来交流
* 依赖 requests, pyquery, rq, redis
* 执行 `python rqworker.py` 启动rqworker（或者使用 `./workers.sh worker个数 日志目录`  来开启）, 然后执行 `python main.py` 启动程序

### TODO:

* 教学模式
* 自有回复

### 提交pull request

* 由于fqj有pep8强迫症，所以在提交之前请先用`pep8` (`pip install pep8`)检查一下代码风格
* 由于fqj有开源协议强迫症，所以在提交之前'请在文件顶部写上你的copyright信息，并且用中文或英文描述你的变动，同时请注意，你的代码将被以MIT许可证发布，如果你不同意MIT许可证的内容，请再changes中自行加上一个与MIT兼容的其他许可证'。
