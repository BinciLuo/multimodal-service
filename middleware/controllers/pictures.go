package controllers

import (
	"encoding/json"
	"fmt"
	"log"
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

func (c *PicturesController) PostTencentCloudImg2Img() {
	var (
		body jmap
	)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		fmt.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostTencentCloudImg2Img(body)
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("PicturesControllerError")
	}

	c.Data["json"] = r
	c.ServeJSON()

}

func (c *PicturesController) PostDALLE2Edit() {
	var (
		body jmap
	)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		fmt.Println(err)
		c.Ctx.ResponseWriter.WriteHeader(http.StatusBadRequest)
		c.Abort("RequestParams")
	}

	r, err := models.PostDALLE2Edit(body)
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(http.StatusInternalServerError)
		c.Abort("PicturesControllerError")
	}

	c.Data["json"] = r
	c.ServeJSON()

}

func (c *PicturesController) PostHuggingFaceImgSegment() {
	var (
		body jmap
	)

	if err := json.Unmarshal(c.Ctx.Input.RequestBody, &body); err != nil {
		r := make(jmap)
		r["error"] = err.Error()
		log.Println(err)
		c.Data["json"] = r
		c.ServeJSON()
	}

	if _, ok := body["image"].(string); !ok {
		err := fmt.Errorf("err: No Image Provided")
		r := make(jmap)
		r["error"] = err.Error()
		log.Println(err)
		c.Data["json"] = r
		c.ServeJSON()
	}

	imagePackages, err := models.PostHuggingFaceImgSegment(body["image"].(string))
	if err != nil {
		r := make(jmap)
		r["error"] = err.Error()
		log.Println(err)
		c.Data["json"] = r
		c.ServeJSON()
	}

	r := make(jmap)
	r["error"] = nil
	r["image_packages"] = imagePackages
	c.Data["json"] = r
	c.ServeJSON()
}
