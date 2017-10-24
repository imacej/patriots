package controllers

import (
	"errors"
	"patriots/utils"
	"strings"

	"github.com/astaxie/beego"
)

// 用户登录进系统之后，会返回一个 token，这个 token 对应的就是这个用户的权限（包含图书馆组、图书馆之类的信息）
// 设置不同 status code 的方法 https://github.com/astaxie/beego/issues/1208

// BaseController 所有 Controller 的基类，用于定义公有方法
type BaseController struct {
	beego.Controller
}

// AllowCross 用于解决跨域问题
// 详情 http://www.cnblogs.com/lrj567/p/6141209.html
func (c *BaseController) AllowCross() {
	c.Ctx.Output.Header("Access-Control-Max-Age", "1728000")
	c.Ctx.Output.Header("content-type", "application/json")
	c.Ctx.Output.Header("Access-Control-Allow-Credentials", "true")
	c.Ctx.Output.Header("Access-Control-Allow-Origin", "*")
	c.Ctx.Output.Header("Access-Control-Allow-Headers", "Content-Type, Content-Length, Authorization, Accept, X-Requested-With, X-CSRF-Token")
	c.Ctx.Output.Header("Access-Control-Allow-Methods", "PUT, POST, GET, DELETE, OPTIONS")
}

// Return500 返回 500 错误
func (c *BaseController) Return500(err error) {
	c.Ctx.Output.SetStatus(500)
	c.Data["json"] = utils.Result{Code: 500, Message: utils.Error500(), Data: err.Error()}
	c.returnJSONData()
}

// Return400 返回 400 错误
func (c *BaseController) Return400(err error) {
	c.Ctx.Output.SetStatus(400)
	c.Data["json"] = utils.Result{Code: 400, Message: utils.Error400(), Data: err.Error()}
	c.returnJSONData()
}

// Return401 返回 401 错误
func (c *BaseController) Return401(err error) {
	c.Ctx.Output.SetStatus(401)
	c.Data["json"] = utils.Result{Code: 401, Message: utils.Error401(), Data: err.Error()}
	c.returnJSONData()
}

// Return404 返回 404 错误
func (c *BaseController) Return404(err error) {
	c.Ctx.Output.SetStatus(404)
	c.Data["json"] = utils.Result{Code: 404, Message: utils.Error404(), Data: err.Error()}
	c.returnJSONData()
}

// Return200 简单封装
func (c *BaseController) Return200() {
	c.Ctx.Output.SetStatus(200)
	c.returnJSONData()
}

// ReturnJSONData 解决跨域问题并返回 JSON
func (c *BaseController) returnJSONData() {
	c.AllowCross()
	c.ServeJSON()
}

// Options 允许跨域
func (c *BaseController) Options() {
	c.AllowCross() //允许跨域
	c.Data["json"] = map[string]interface{}{"code": 200, "message": "ok", "data": ""}
	c.ServeJSON()
}

// ParseToken 解析 Token
func (c *BaseController) ParseToken() (*utils.IdentityClaims, error) {
	authString := c.Ctx.Input.Header("Authorization")
	beego.Debug("AuthString", authString)

	kv := strings.Split(authString, " ")
	if len(kv) != 2 || kv[0] != "Bearer" {
		beego.Error("AuthString invalid:", authString)
		return nil, errors.New("AuthString invalid")
	}
	tokenString := kv[1]

	claims, err := utils.ParseToken(tokenString)
	if err != nil {
		return nil, err
	}

	beego.Trace(claims.UserID, claims.Type)
	return claims, err

}
