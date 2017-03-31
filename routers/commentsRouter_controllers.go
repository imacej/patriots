package routers

import (
	"github.com/astaxie/beego"
)

func init() {

	beego.GlobalControllerRouter["patriots/controllers:TestsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TestsetController"],
		beego.ControllerComments{
			Method: "NewTestset",
			Router: `/`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TrainsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TrainsetController"],
		beego.ControllerComments{
			Method: "NewTrainset",
			Router: `/`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

}
