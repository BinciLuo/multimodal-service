package controllers

import (
	"encoding/json"
	"log"
	"middleware/models"

	beego "github.com/beego/beego/v2/server/web"
)

type ChatController struct {
	beego.Controller
}

func (c *ChatController) PostGPT3Dot5Turbo() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		log.Println(err)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Abort("RequestParams")
	}

	r, err := models.PostGPT3Dot5Turbo(body["query"].(string))
	if err != nil {
		log.Println(err)
		c.Abort("ChatControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}

func (c *ChatController) PostChatGLM2_6B() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		log.Println(err)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Abort("RequestParams")
	}

	r, err := models.PostChatGLM2_6B(body)
	if err != nil {
		c.Abort("ControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}
