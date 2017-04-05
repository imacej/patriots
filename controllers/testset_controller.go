package controllers

import "github.com/astaxie/beego"

// testset.go
// 该文件包含测试集相关 API
// 所有的注释符合 beego 的自动生成文档的规范
// 如果使用 bee run -gendoc=true -downdoc=true 运行的话
// 可以直接在 http://localhost:12333/swagger/# 中查看文档
// da.wang 17.03.31

type TestsetController struct {
	beego.Controller
}

// NewTestset method description
// @Title Create a new test set
// @Description 创建一个测试集
// @Param name formData string true "test set name"
// @Success 200 创建新测试集成功
// @Failure 500 服务器错误
// @router / [post]
func (c *TestsetController) NewTestset() {

}
