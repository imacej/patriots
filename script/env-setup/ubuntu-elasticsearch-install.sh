# Ubuntu Elasticsearch 安装配置
# 需要有 Java 环境，可以用另外的脚本安装

# --------------------------
# Home 文件夹位置，需要自定义配置
serviceDir=/path/to/home/folder

# 下载 Elasticsearch
# https://www.elastic.co/downloads/elasticsearch
cd $serviceDir
echo "[INFO] Download Elasticsearch binaries"
wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.0/elasticsearch-2.4.0.tar.gz
tar -xvzf elasticsearch-2.4.0.tar.gz
echo "[INFO] Done (1/2)"

# 清理工作，把所有的安装包保存到 software 文件夹中
echo "[INFO] Clean up all the mess" 
cd $serviceDir
mkdir $serviceDir/software
mv *.gz $serviceDir/software
echo "[INFO] Done (2/2)"
echo "All Done. You can now continue your work."
echo "You can launch Elasticsearch with './bin/elasticsearch'"
echo "Or run it in background 'nohup ./bin/elasticsearch &'"