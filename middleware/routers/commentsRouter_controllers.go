package routers

import (
	beego "github.com/beego/beego/v2/server/web"
	"github.com/beego/beego/v2/server/web/context/param"
)

func init() {
	/*
		/pics
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
			Method:           "PostSDImg2Img",
			Router:           "/img2img",
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
	/*
		/chat
	*/

	beego.GlobalControllerRouter["middleware/controllers:ChatController"] = append(beego.GlobalControllerRouter["middleware/controllers:ChatController"],
		beego.ControllerComments{
			Method:           "PostGPT3Dot5Turbo",
			Router:           "/gpt3dot5turbo",
			AllowHTTPMethods: []string{"post"},
			MethodParams:     param.Make(),
			Filters:          nil,
			Params:           nil})

	beego.GlobalControllerRouter["middleware/controllers:ChatController"] = append(beego.GlobalControllerRouter["middleware/controllers:ChatController"],
		beego.ControllerComments{
			Method:           "PostChatGLM2_6B",
			Router:           "/glm2_6b",
			AllowHTTPMethods: []string{"post"},
			MethodParams:     param.Make(),
			Filters:          nil,
			Params:           nil})

}
