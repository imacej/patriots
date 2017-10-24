package controllers

import (
	"encoding/json"
	"errors"
	"os"
	"patriots/models"
	"patriots/utils"
	"strconv"

	"github.com/astaxie/beego"
)

// algorithm.go
// 该文件包含算法相关 API
// 所有的注释符合 beego 的自动生成文档的规范
// 如果使用 bee run -gendoc=true -downdoc=true 运行的话
// 可以直接在 http://localhost:port/swagger/# 中查看文档
// da.wang 17.03.31

type AlgorithmController struct {
	BaseController
}

// CreateAlgorithm method description
// @Description 创建一个新的算法，注，需要传入一个 json 字符串，自带的命令无法实现
// @Success 200 创建成功
// @Failure 400 客户端传入参数错误
// @Failure 500 创建失败
// @router / [post]
func (c *AlgorithmController) CreateAlgorithm() {
	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	// 客户端传入参数错误
	algorithm := new(models.Algorithm)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &algorithm); err != nil {
		c.Return400(err)
		return
	}

	beego.Trace(algorithm)

	// 配置对应路径
	dir, _ := os.Getwd()

	algorithm.Path = "/static/code/" + algorithm.Path

	existed, _ := utils.PathExists(dir + algorithm.Path)
	if !existed { // 不存在则创建
		c.Return500(errors.New("没有对应的算法文件"))
		return
	}

	_, err = models.CreateAlgorithm(algorithm)
	// 创建失败
	if err != nil {
		c.Return500(err)
		return
	}

	// 创建成功
	c.Data["json"] = utils.ResultAlgorithmCreated()
	c.Return200()
}

// GetAlgorithm method description
// @Description 根据ID获取算法
// @Param id path int true "对应 ID"
// @Success 200 获取成功
// @Failure 500 服务器错误
// @router /:id [get]
func (c *AlgorithmController) GetAlgorithm() {

	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	id, _ := strconv.Atoi(c.Ctx.Input.Param(":id"))

	// 获取组失败
	algorithm, err := models.GetAlgorithmByID(id)
	if err != nil {
		c.Return500(err)
		return
	}

	c.Data["json"] = algorithm
	c.Return200()
}

// GetAlgorithmList method description
// @Description 获取算法列表
// @Success 200 获取成功
// @Failure 500 服务器错误
// @router / [get]
func (c *AlgorithmController) GetAlgorithmList() {

	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	algorithmlist := models.GetAlgorithmList()
	c.Data["json"] = algorithmlist
	c.Return200()
}

// DeleteAlgorithm method description
// @Description 删除指定算法
// @Success 200 删除成功
// @Failure 500 服务器错误
// @router /:id/delete [post]
func (c *AlgorithmController) DeleteAlgorithm() {

	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	id, _ := strconv.Atoi(c.Ctx.Input.Param(":id"))
	// 获取组失败
	algorithm, err := models.GetAlgorithmByID(id)
	if err != nil {
		c.Return500(err)
		return
	}

	// 删除失败
	num, err := models.DeleteAlgorithm(algorithm)
	if err != nil {
		c.Return500(err)
		return
	}
	beego.Trace("此次删除影响的行数为", num)

	// 不删除代码，怕弄错

	// 删除成功，返回新的列表
	c.Data["json"] = models.GetAlgorithmList()
	c.Return200()
}
