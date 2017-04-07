package routers

import (
	"github.com/astaxie/beego"
)

func init() {

	beego.GlobalControllerRouter["patriots/controllers:StatusController"] = append(beego.GlobalControllerRouter["patriots/controllers:StatusController"],
		beego.ControllerComments{
			Method: "Login",
			Router: `/login`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:StatusController"] = append(beego.GlobalControllerRouter["patriots/controllers:StatusController"],
		beego.ControllerComments{
			Method: "Logout",
			Router: `/logout`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:StatusController"] = append(beego.GlobalControllerRouter["patriots/controllers:StatusController"],
		beego.ControllerComments{
			Method: "Status",
			Router: `/`,
			AllowHTTPMethods: []string{"get"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TestsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TestsetController"],
		beego.ControllerComments{
			Method: "CreateTestset",
			Router: `/`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TestsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TestsetController"],
		beego.ControllerComments{
			Method: "GetTestset",
			Router: `/:id`,
			AllowHTTPMethods: []string{"get"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TestsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TestsetController"],
		beego.ControllerComments{
			Method: "GetTestsetList",
			Router: `/`,
			AllowHTTPMethods: []string{"get"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TestsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TestsetController"],
		beego.ControllerComments{
			Method: "DeleteTestset",
			Router: `/:id/delete`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TrainsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TrainsetController"],
		beego.ControllerComments{
			Method: "CreateTrainset",
			Router: `/`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TrainsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TrainsetController"],
		beego.ControllerComments{
			Method: "GetTrainset",
			Router: `/:id`,
			AllowHTTPMethods: []string{"get"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TrainsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TrainsetController"],
		beego.ControllerComments{
			Method: "GetTrainsetList",
			Router: `/`,
			AllowHTTPMethods: []string{"get"},
			Params: nil})

	beego.GlobalControllerRouter["patriots/controllers:TrainsetController"] = append(beego.GlobalControllerRouter["patriots/controllers:TrainsetController"],
		beego.ControllerComments{
			Method: "DeleteTrainset",
			Router: `/:id/delete`,
			AllowHTTPMethods: []string{"post"},
			Params: nil})

}
