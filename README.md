### [人人网小黄鸡](http://www.renren.com/601621937)

* 可以通过在状态里@它或者回复它来交流
* 依赖的Python库见`requirements.txt`，可通过 `[sudo] pip install -r requirements.txt`自动安装
* 确保本机有redis server且已启动
* 执行 `python rqworker.py` 启动rqworker（或者使用 `./workers.sh worker个数 日志目录`  来开启）, 然后执行 `python main.py` 启动程序

### TODO:

* 教学模式
* 自有回复

### 提交pull request

* 由于fqj有pep8强迫症，所以在提交之前请先用`pep8` (`pip install pep8`)检查一下代码风格
* 由于fqj有开源协议强迫症，所以在提交之前'请在文件顶部写上你的copyright信息，并且用中文或英文描述你的变动，同时请注意，你的代码将被以MIT许可证发布，如果你不同意MIT许可证的内容，请再changes中自行加上一个与MIT兼容的其他许可证'。

### 插件编写

为了方便大家给小黄鸡加入更多有趣的功能，我们引入了插件的方式。

插件放在plugins目录下，每个插件是一个python文件，提供两个接口，`test`和`handle`，格式如下：

    def test(data, bot):
        // your code

`test`方法返回`True`或`False`，说明是否要用该插件处理这一条请求。

    def handle(data, bot):
        // your code

`handle`方法则实际处理请求，它需要返回一个utf-8编码的字符串，用来作为小黄鸡对这条请求的答复。

`data`是一个字典，内容如下:

    {
        'owner_id'   : 状态主人的id,
        'doing_id'   : 状态的id,
        'message'    : 状态或回复的内容,
        'author_id'  : 回复者的id，   (回复评论的情况)
        'author_name': 回复者的名字,  (回复评论的情况)
        'reply_id'   : 回复的评论的id (回复评论的情况)
    }

`bot`则是一个`RenRen`的实例

插件编写好之后，请在`plugins/__init__.py`文件中注册你的插件，具体为在`__all__`列表里加入一项到你认为合适的位置(插件的匹配是从前往后)，但请保证`simsimi`插件处在列表最后一项。

插件具体例子见`plugins`目录

插件编写好之后，请在tests目录添加对应的单元测试，具体可参考已有的测试代码，在主目录执行`nosetests -v`开始测试。(啊。。我发现我也懒得写单元测试了。。)
