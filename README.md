# MOOC_Scrapy

基于Scrapy的小爬虫，主要包括：
* 各个学科频道下的所有科目的基本信息(包括课程二级界面的评分信息)
* 指定关键词的搜索页面课程信息
* 爬取数据的存储和两种可视化库的小试水( **[Dash]** & **[pyecharts]** )

主要目的是写一个走Ajax接口的爬虫练手（和交作业😥，初期的测试都是从零开始查看XHR信息，再fiddler抓包和模拟POST，测试完成再开写。

可视化试了 **[Dash]** 和 **[pyecharts]**，都各有各的优缺点，dash的页面写的真的很戳
（当时还没学完web基础！）数据分析意义其实感觉不是很大，尽量多花了几张图熟悉库操作而已。

**ps** ：cookie文件内容如失效请自行替换

[Dash]: https://dash.plotly.com/
[pyecharts]: https://pyecharts.org/
