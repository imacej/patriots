package controllers

import (
	"fmt"
	"patriots/models"

	"github.com/astaxie/beego"
	"github.com/astaxie/beego/orm"

	"github.com/astaxie/beego/logs"
	_ "github.com/go-sql-driver/mysql"
)

type MainController struct {
	beego.Controller
}

func init() {
	// 只需要在这里初始化一次
	orm.RegisterDriver("mysql", orm.DRMySQL)
	orm.RegisterDataBase("default", "mysql", "root:@/patriots?charset=utf8")
	orm.RunSyncdb("default", false, true)

	// 日志设置
	logs.SetLogger("console")
	logs.SetLogger(logs.AdapterFile, `{"filename":"patriots.log","level":7,"maxlines":0,"maxsize":0,"daily":true, "maxdays":10}`)
}

func (c *MainController) Get() {
	c.Ctx.WriteString("Hello World")
}

func (c *MainController) Post() {
	test := models.Algorithm{}

	fmt.Println(test)
}
