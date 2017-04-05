package controllers

import "github.com/astaxie/beego"

// trainset.go
// 该文件包含训练集相关 API
// 所有的注释符合 beego 的自动生成文档的规范
// 如果使用 bee run -gendoc=true -downdoc=true 运行的话
// 可以直接在 http://localhost:12333/swagger/# 中查看文档
// da.wang 17.03.31

type TrainsetController struct {
	beego.Controller
}

// NewTrainset method description
// @Title Create a new train set
// @Description 创建一个训练集
// @Param name formData string true "train set name"
// @Success 200 创建新训练集成功
// @Failure 500 服务器错误
// @router / [post]
func (c *TrainsetController) NewTrainset() {

}
