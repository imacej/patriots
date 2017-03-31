# Ubuntu BeeGo 安装脚本
# 需要配置 GOPATH 路径，请先使用 ubuntu-go-install.sh

# --------------------------
# 安装 git
echo "[INFO] Installing git"
sudo apt install git -y

# 安装 BeeGo
echo "[INFO] Installing beego"
go get github.com/astaxie/beego
# 升级 BeeGo
# go get -u github.com/astaxie/beego
echo "[INFO] Done(1/2)"

# 安装 Bee 工具
echo "[INFO] Installing bee tool"
go get github.com/beego/bee
# 更新 PATH 变量，这里支持的是 bash
echo "Updating PATH variable"
echo "export PATH=$PATH:$GOPATH/bin" >> ~/.bashrc
source ~/.bashrc
echo "[INFO] Done(2/2)"
echo "All Done. You can now continue your work."
echo "Remember to go to the project folder and run 'bee fix' for upgrading"
