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
	OpenAIToken := OpenAIToken1 + OpenAIToken2 + OpenAIToken3

	models.OpenAIClient = openai.NewClient(OpenAIToken)
	GlmServer, _ := config.String("GLMSERVER")
	models.GlmChatURL = GlmServer + "/chat/chatglm2-6b"
	Port := os.Getenv("BEE_PORT")
	if Port == "" {
		Port = "8080"
	}
	RunningAddr := "0.0.0.0:" + Port
	beego.Run(RunningAddr)
}
