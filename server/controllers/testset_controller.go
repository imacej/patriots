package controllers

import (
	"encoding/json"
	"os"
	"patriots/models"
	"patriots/utils"
	"strconv"

	"github.com/astaxie/beego"
)

// testset.go
// 该文件包含测试集相关 API
// 所有的注释符合 beego 的自动生成文档的规范
// 如果使用 bee run -gendoc=true -downdoc=true 运行的话
// 可以直接在 http://localhost:12333/swagger/# 中查看文档
// da.wang 17.03.31

type TestsetController struct {
	BaseController
}

// CreateTestset method description
// @Description 创建一个新的测试集，注，需要传入一个 json 字符串，自带的命令无法实现
// @Success 200 创建测试集成功
// @Failure 400 客户端传入参数错误
// @Failure 500 创建失败
// @router / [post]
func (c *TestsetController) CreateTestset() {
	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	// 客户端传入参数错误
	testset := new(models.Testset)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &testset); err != nil {
		c.Return400(err)
		return
	}

	// 配置对应路径
	dir, _ := os.Getwd()

	testset.Path = "/static/testset/" + testset.Name

	existed, _ := utils.PathExists(dir + testset.Path)
	if !existed { // 不存在则创建
		err := os.Mkdir(dir+testset.Path, os.ModePerm)
		if err != nil {
			c.Return500(err)
			return
		}
	}

	_, err = models.CreateTestset(testset)
	// 创建失败
	if err != nil {
		c.Return500(err)
		return
	}

	// 创建成功
	c.Data["json"] = utils.ResultTestsetCreated()
	c.Return200()
}

// GetTrainset method description
// @Description 根据ID获取训练集
// @Param id path int true "对应 ID"
// @Success 200 获取图书馆组成功
// @Failure 500 服务器错误
// @router /:id [get]
func (c *TestsetController) GetTestset() {

	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	id, _ := strconv.Atoi(c.Ctx.Input.Param(":id"))

	testset, err := models.GetTestsetByID(id)
	if err != nil {
		c.Return500(err)
		return
	}

	c.Data["json"] = testset
	c.Return200()
}

// GetTestsetList method description
// @Description 获取训练集列表
// @Success 200 获取成功
// @Failure 500 服务器错误
// @router / [get]
func (c *TestsetController) GetTestsetList() {

	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	testsetlist := models.GetTestsetList()
	c.Data["json"] = testsetlist
	c.Return200()
}

// DeleteTestset method description
// @Description 删除指定训练集
// @Success 200 删除成功
// @Failure 500 服务器错误
// @router /:id/delete [post]
func (c *TestsetController) DeleteTestset() {

	// 校验 Token
	claims, err := c.ParseToken()
	if err != nil { // Token 校验失败
		c.Return401(err)
		return
	}
	beego.Trace(claims)

	id, _ := strconv.Atoi(c.Ctx.Input.Param(":id"))
	// 获取组失败
	testset, err := models.GetTestsetByID(id)
	if err != nil {
		c.Return500(err)
		return
	}

	// 删除失败
	num, err := models.DeleteTestset(testset)
	if err != nil {
		c.Return500(err)
		return
	}
	beego.Trace("此次删除影响的行数为", num)

	// 需要删除对应文件夹
	dir, _ := os.Getwd()

	testset.Path = "/static/testset/" + testset.Name

	existed, _ := utils.PathExists(dir + testset.Path)
	if existed { // 存在则删除
		err = os.RemoveAll(dir + testset.Path)
		if err != nil {
			c.Return500(err)
			return
		}
	}

	// 删除成功，返回新的列表
	c.Data["json"] = models.GetTrainsetList()
	c.Return200()
}
