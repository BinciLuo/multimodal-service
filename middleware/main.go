package main

import (
	"middleware/models"
	_ "middleware/routers"

	"github.com/beego/beego/v2/core/config"
	beego "github.com/beego/beego/v2/server/web"
)

func main() {
	SDURL, _ := config.String("SDURL")
	models.Text2ImgURL = SDURL + "/sdapi/v1/txt2img"
	models.LoraURL = SDURL + "/sdapi/v1/loras"

	beego.Run()
}
