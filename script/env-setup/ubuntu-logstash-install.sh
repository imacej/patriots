# Ubuntu Logstash 安装配置
# 需要有 Java 环境，可以用另外的脚本安装

# --------------------------
# Home 文件夹位置，需要自定义配置
serviceDir=/path/to/home/folder

# 下载文件
# 需要根据下载路径进行配置
filename=logstash-all-plugins-2.3.4.tar.gz
foldername=logstash-all-plugins-2.3.4

# 下载 Logstash，这里直接下载全插件版，就不用配置了
# https://www.elastic.co/downloads/logstash
cd $serviceDir
echo "[INFO] Download Logstash binaries"
wget https://download.elastic.co/logstash/logstash/logstash-all-plugins-2.3.4.tar.gz
tar -xvzf $filename
mv $foldername logstash
cd logstash
# 创建配置文件夹
mkdir confs
echo "[INFO] Done (1/2)"

# 清理工作，把所有的安装包保存到 software 文件夹中
echo "[INFO] Clean up all the mess" 
cd $serviceDir
mkdir $serviceDir/software
mv *.gz $serviceDir/software
echo "[INFO] Done (2/2)"
echo "All Done. You can now continue your work."