package controllers

import (
	"encoding/json"
	"fmt"
	"middleware/models"

	beego "github.com/beego/beego/v2/server/web"
)

type ChatController struct {
	beego.Controller
}

func (c *ChatController) PostGPT3Dot5Turbo() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		fmt.Println(err)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Abort("RequestParams")
	}

	r, err := models.PostGPT3Dot5Turbo(body["query"].(string))
	if err != nil {
		fmt.Println(err)
		c.Abort("ChatControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}
