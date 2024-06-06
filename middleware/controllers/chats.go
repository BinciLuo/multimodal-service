package controllers

import (
	"encoding/json"
	"log"
	"middleware/models"
	"net/http"

	beego "github.com/beego/beego/v2/server/web"
)

type ChatController struct {
	beego.Controller
}

func (c *ChatController) PostGPT3Dot5Turbo() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}
	if _, ok := body["history"].(jarray); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostGPT3Dot5Turbo(body["query"].(string), body["history"].(jarray))
	if err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("ChatControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}

func (c *ChatController) PostGPT4() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}
	if _, ok := body["history"].(jarray); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostGPT4(body["query"].(string), body["history"].(jarray))
	if err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("ChatControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}

func (c *ChatController) PostChatGLM2_6B() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	if _, ok := body["history"].(jarray); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostChatGLM2_6B(body["query"].(string), body["history"].(jarray))
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("ControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}

func (c *ChatController) PostGPT4V() {
	body := make(jmap)
	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	if _, ok := body["query"].(string); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}
	if _, ok := body["history"].(jarray); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}
	if _, ok := body["init_image"].(string); !ok {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostGPT4V(body["query"].(string), body["history"].(jarray), body["init_image"].(string))
	if err != nil {
		log.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("ChatControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}
