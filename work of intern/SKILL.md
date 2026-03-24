如果需要获取新闻，使用如下命令，XXX为用户希望搜索的关键词
curl -L -A "Mozilla/5.0" "https://news.google.com/rss/search?q=XXX&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"

如果需要读取某个特定网页的内容，使用如下命令，XXX为目标网页的完整 URL 链接：
curl -s "https://r.jina.ai/XXX"

如果遇到需要进行数据处理、复杂计算或文本分析的任务，你可以编写一行 Python 代码并使用如下命令执行，XXX 为你的 Python 代码（注意转义双引号）：
python -c "XXX"
例如：python -c "import pandas as pd; print(pd.read_csv('data.csv').head())"

如果需要搜索某个领域的学术论文或文献，使用如下命令，XXX 为英文搜索关键词（多个词用+连接）：
curl -s "http://export.arxiv.org/api/query?search_query=all:XXX&start=0&max_results=3"

如果需要查询天气情况，使用如下命令，XXX 为城市名称的拼音或英文：
curl -s "wttr.in/XXX?format=3"