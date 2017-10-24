# Ubuntu Java 安装配置

# --------------------------
echo "[INFO] Start installing Java 8"
sudo add-apt-repository -y ppa:webupd8team/java
sudo apt-get update
sudo apt-get -y install oracle-java8-installer
echo "[INFO] Done"
echo "All Done. You can now continue your work."