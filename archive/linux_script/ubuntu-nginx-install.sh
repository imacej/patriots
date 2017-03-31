# Ubuntu Nginx 环境配置脚本
# 需要以 root 权限执行

# -------------------------
# Home 文件夹位置，需要自定义配置
serviceDir=/path/to/home/folder

# 安装配置依赖，这里直接用 apt-get
echo "[INFO] Installing make g++"
cd $serviceDir
apt-get -y install make
apt-get -y install g++
echo "[INFO] Done(1/7)"

# 安装 openssl，其中 openssl-1.0.2 是长期支持版本，所以我采用这个版本
# 更多信息请访问 https://www.openssl.org/source/
echo "[INFO] Installing openssl" 
cd $serviceDir
wget https://www.openssl.org/source/openssl-1.0.2h.tar.gz
tar -xzvf openssl-1.0.2h.tar.gz
cd $serviceDir/openssl-1.0.2h
./config
make
make install
ldconfig
echo "[INFO] Done(2/7)"

# 安装 Pcre，为了保证兼容我们这里使用较老的版本
# 源用的是 stanford 的（因为 pcre.org 我这里打不开）
# 源：http://ftp.cs.stanford.edu/pub/exim/pcre/
echo "[INFO] Installing pcre"
cd $serviceDir
wget http://ftp.cs.stanford.edu/pub/exim/pcre/pcre-8.37.tar.gz
tar -xzvf pcre-8.37.tar.gz
cd $serviceDir/pcre-8.37
./configure
make
make install
ldconfig
echo "[INFO] Done(3/7)"

# 安装 zlib，用的就是最新的 1.2.8
# 源 http://zlib.net/zlib-1.2.8.tar.gz
echo "[INFO] Installing zlib"
cd $serviceDir
wget http://zlib.net/zlib-1.2.8.tar.gz
tar -xzvf zlib-1.2.8.tar.gz
cd $serviceDir/zlib-1.2.8
./configure
make
make install
ldconfig
echo "[INFO] Done(4/7)"

# 安装 Nginx
echo "[INFO] Installing Nginx"
cd $serviceDir
wget https://nginx.org/download/nginx-1.10.1.tar.gz
tar -xzvf nginx-1.10.1.tar.gz
cd $serviceDir/nginx-1.10.1
./configure --prefix=$serviceDir/nginx-server --with-openssl=$serviceDir/openssl-1.0.2h --with-http_ssl_module --with-http_stub_status_module --with-stream
make
make install
cd $serviceDir/nginx-server/conf
rm -rf nginx.conf
# 这里用的是已经配置好的配置文件
wget http://xssz.oss-cn-shenzhen.aliyuncs.com/server_software/nginx.conf
ln -s $serviceDir/nginx-server/sbin/nginx /usr/local/bin/nginx
mkdir $serviceDir/nginx-server/run
mkdir $serviceDir/nginx-config
ln -s $serviceDir/nginx-server/sbin/nginx /usr/local/bin/nginx
nginx -c $serviceDir/nginx-server/conf/nginx.conf
echo "[INFO] Done(5/7)"

# 安装守护
echo "[INFO] Config daemon"
echo $serviceDir'/nginx-server/sbin/nginx -c '$serviceDir'/nginx-server/conf/nginx.conf' > /etc/rc.local
echo 'exit 0' >> /etc/rc.local
echo "[INFO] Done(6/7)"

# 清理工作，把所有的安装包保存到 software 文件夹中
echo "[INFO] Clean up all the mess"
cd $serviceDir
mkdir $serviceDir/software
mv *.gz $serviceDir/software
echo "[INFO] Done(7/7)"

echo "All Done. You can now continue your work."