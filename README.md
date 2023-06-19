# Data-Explorer
這是一個python project，可以對database進行全域搜尋關鍵字，目前只提供對於三種database的實作(mySQL, neo4j, mongodb)。

# Getting Started
## Installation
```
git clone https://github.com/container513/data_explorer.git
```
且需要 pip install 所有需要的套件
## Usage
``` python
searchEngine = Neo4jForSearch(
    "bolt://localhost:7687", "user", "password","db_name")
# searchEngine = MongoDBForSearch("mongodb://localhost:27017/", "db_name")
# searchEngine = MysqlForSearch('localhost', 'user', 'password', 'db_name')
data_explorer = DataExplorer(searchEngine)
data_explorer.search_keyword('apple')
data_explorer.visualize('histogram')
data_explorer.visualize('wordcloud')
searchEngine.close()
```
1. 首先，要去創造 SearchEngine，傳入連上 DBMS 所需的資訊。
2. 使用 SearchEngine 創造 DataExplorer
3. 使用 DataExplorer 搜尋想要的關鍵字
4. 使用 DataExplorer 提供的視覺化圖形
5. 關閉與 DBMS 的連接