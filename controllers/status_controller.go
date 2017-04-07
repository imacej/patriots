package controllers

import (
	"encoding/json"
	"patriots/models"
	"patriots/utils"

	"errors"

	"github.com/astaxie/beego"
)

// 登录、登出、验证等

// 状态控制 API
type StatusController struct {
	BaseController
}

// Login method description
// @Description 登陆系统，校验密码，返回 token，注，需要传入一个 json 字符串
// @Success 200 登录成功
// @Failure 400 客户端传入参数错误
// @Failure 500 创建失败
// @router /login [post]
func (c *StatusController) Login() {
	// root 帐号（系统的最初用户）
	// username: root
	// password: root1234

	// 客户端传入参数错误
	user := new(models.User)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &user); err != nil {
		c.Return400(err)
		return
	}
	beego.Trace(user)

	// root 帐号登录，其他的需要去数据库检索
	if user.Username == "root" && user.Password == "root1234" {
		// Token 创建失败
		token, err := utils.GenerateToken(0, "root")
		if err != nil {
			c.Return500(err)
			return
		}

		// Token 创建成功
		beego.Trace("Token 创建成功", token)
		c.Data["json"] = utils.ResultTokenCreated(user.Username, token)
		c.Return200()
		return
	}

	iuser, err := models.GetUserByUsername(user.Username)
	if err != nil {
		beego.Trace(err)
		c.Return500(errors.New("没有该用户"))
		return
	}
	if user.Password != iuser.Password {
		c.Return404(errors.New("密码错误"))
		return
	}

	// 前面校验没错的话就开始创建 Token
	token, err := utils.GenerateToken(iuser.ID, iuser.Username)
	if err != nil {
		c.Return500(err)
		return
	}
	// Token 创建成功
	beego.Trace("Token 创建成功", token)
	c.Data["json"] = utils.ResultTokenCreated(iuser.Username, token)
	c.Return200()
	return
}

// Logout method description
// @Description 登出系统，清除 token 对应的账户信息，注，需要传入一个 json 字符串
// @Success 200 登出成功
// @Failure 400 客户端传入参数错误
// @Failure 500 创建失败
// @router /logout [post]
func (c *StatusController) Logout() {

}

// Status method description
// @Description 获取当前登录状态（即验证 token）
// @Success 200 登录成功
// @Failure 400 客户端传入参数错误
// @Failure 500 创建失败
// @router / [get]
func (c *StatusController) Status() {

}
