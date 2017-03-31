# Ubuntu Redis 安装配置
# 最好以 root 运行

# --------------------------
# Home 文件夹位置，需要自定义配置
serviceDir=/path/to/home/folder

# 下载文件
# 需要根据下载路径进行配置
filename=redis-3.2.3.tar.gz
foldername=redis-3.2.3

# 下载 Redis
# http://redis.io/download
cd $serviceDir
echo "[INFO] Download Logstash binaries"
wget http://download.redis.io/releases/$filename
tar -xvzf $filename
mv $foldername redis
cd redis
echo "[INFO] Done (1/3)"

echo "[INFO] Start building redis"
make 
echo "[INFO] Done (2/3)"

# 清理工作，把所有的安装包保存到 software 文件夹中
echo "[INFO] Clean up all the mess" 
cd $serviceDir
mkdir $serviceDir/software
mv *.gz $serviceDir/software
echo "[INFO] Done (3/3)"
echo "All Done. You can now continue your work."
echo "You can run redis with 'redis/src/redis-server''"
echo "And interact with redis using 'redis/src/redis-cli'"