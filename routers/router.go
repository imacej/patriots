// @APIVersion 1.0.0
// @Title Patriots 数据挖掘平台 API
// @Description 这是自动生成的 Patriots 数据挖掘平台 API 文档
// @Contact wdxtub@qq.com
// @TermsOfServiceUrl http://wdxtub.com
// @License GPL-3.0
// @LicenseUrl https://github.com/wdxtub/Patriots/blob/master/LICENSE
package routers

import (
	"patriots/controllers"

	"github.com/astaxie/beego"
)

func init() {
	beego.Router("/", &controllers.MainController{})

	beego.Router("/*", &controllers.BaseController{}, "options:Options")

	ns := beego.NewNamespace("/v1",
		beego.NSNamespace("/status",
			beego.NSInclude(
				&controllers.StatusController{},
			),
		),
		beego.NSNamespace("/trainsets",
			beego.NSInclude(
				&controllers.TrainsetController{},
			),
		),
		beego.NSNamespace("/testsets",
			beego.NSInclude(
				&controllers.TestsetController{},
			),
		),
	)
	beego.AddNamespace(ns)
}
