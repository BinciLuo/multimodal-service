package routers

import (
	"middleware/controllers"

	beego "github.com/beego/beego/v2/server/web"
)

func init() {
	ns := beego.NewNamespace("/v1",

		beego.NSNamespace("/pics",
			beego.NSInclude(
				&controllers.PicturesController{},
			),
		),
	)

	beego.AddNamespace(ns)

}
