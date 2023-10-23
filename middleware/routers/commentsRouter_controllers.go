package routers

import (
	"log"
	"os"

	beego "github.com/beego/beego/v2/server/web"
	"github.com/beego/beego/v2/server/web/context/param"
)

func init() {

	log.Println("---- LSPOPRUNENV: ", os.Getenv("LSPOPRUNENV"))
	/*
		/pics/txt2img
	*/

	beego.GlobalControllerRouter["middleware/controllers:PicturesController"] = append(beego.GlobalControllerRouter["middleware/controllers:PicturesController"],
		beego.ControllerComments{
			Method:           "PostSDTxt2Img",
			Router:           "/txt2img",
			AllowHTTPMethods: []string{"post"},
			MethodParams:     param.Make(),
			Filters:          nil,
			Params:           nil})

	beego.GlobalControllerRouter["middleware/controllers:PicturesController"] = append(beego.GlobalControllerRouter["middleware/controllers:PicturesController"],
		beego.ControllerComments{
			Method:           "GetLoras",
			Router:           "/loras",
			AllowHTTPMethods: []string{"get"},
			MethodParams:     param.Make(),
			Filters:          nil,
			Params:           nil})

}
