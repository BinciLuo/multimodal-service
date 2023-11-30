package main

import (
	"middleware/models"
	_ "middleware/routers"
	"os"

	"github.com/beego/beego/v2/core/config"
	beego "github.com/beego/beego/v2/server/web"
	openai "github.com/sashabaranov/go-openai"
)

func main() {
	SDURL, _ := config.String("SDURL")
	models.Text2ImgURL = SDURL + "/sdapi/v1/txt2img"
	models.Img2ImgURL = SDURL + "/sdapi/v1/img2img"
	models.LoraURL = SDURL + "/sdapi/v1/loras"

	OpenAIToken1, _ := config.String("OpenAIToken1")
	OpenAIToken2, _ := config.String("OpenAIToken2")
	OpenAIToken3, _ := config.String("OpenAIToken3")
	OpenAITokenOne := OpenAIToken1 + OpenAIToken2 + OpenAIToken3

	OpenAIToken4, _ := config.String("OpenAIToken4")
	OpenAIToken5, _ := config.String("OpenAIToken5")
	OpenAIToken6, _ := config.String("OpenAIToken6")
	OpenAITokenTwo := OpenAIToken4 + OpenAIToken5 + OpenAIToken6

	TencentAK1, _ := config.String("TencentAK1")
	TencentAK2, _ := config.String("TencentAK2")
	TencentSK1, _ := config.String("TencentSK1")
	TencentSK2, _ := config.String("TencentSK2")
	models.TencentAK = TencentAK1 + TencentAK2
	models.TencentSK = TencentSK1 + TencentSK2

	models.OpenAIClient1 = openai.NewClient(OpenAITokenOne)
	models.OpenAIClient2 = openai.NewClient(OpenAITokenTwo)
	models.OpenAIKey = OpenAITokenTwo
	GlmServer, _ := config.String("GLMSERVER")
	models.GlmChatURL = GlmServer + "/chat/chatglm2-6b"
	Port := os.Getenv("BEE_PORT")
	if Port == "" {
		Port = "8080"
	}
	RunningAddr := "0.0.0.0:" + Port
	beego.Run(RunningAddr)
}
