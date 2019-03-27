
使用方法：



在spider_thread文件夹下创建Python文件（参考cnpiec_1文件）

    创建两个类分别继承 Standard_spider中的StartSpider与EndSpider，实现get方法

    StartSpider：
        输入：会传入一个数字，代表翻页的页数
        输出：一个list，要求list中包含下载页面的url与日期（推荐使用self.set_list方法对list赋值）

    EndSpider：
        输入：下载页面的url
        输出：无需返回，但必须调用 self.set_title设置标题，调用self.set_text方法设置正文

将创建好的python文件配置到spider_modules文件夹下conf.cfg中，格式要求如下：

    python文件名=startspider子类类名，endspider子类类名

将所有需要运行的爬虫都配置到名叫task的section下







