package controllers

import (
	"encoding/json"
	"fmt"
	"middleware/models"
	"net/http"

	beego "github.com/beego/beego/v2/server/web"
)

type PicturesController struct {
	beego.Controller
}

func (c *PicturesController) PostSDTxt2Img() {
	var (
		body jmap
	)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		fmt.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("RequestParams")
	}

	r, err := models.PostSDTxt2Img(body)
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("PicturesControllerError")
	}

	c.Data["json"] = r
	c.ServeJSON()

}

func (c *PicturesController) PostSDImg2Img() {
	var (
		body jmap
	)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		fmt.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostSDImg2Img(body)
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("PicturesControllerError")
	}

	c.Data["json"] = r
	c.ServeJSON()

}

func (c *PicturesController) GetLoras() {
	r, err := models.GetLoras()
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("PicturesControllerError")
	}
	c.Data["json"] = r
	c.ServeJSON()
}
