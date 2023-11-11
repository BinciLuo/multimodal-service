package models

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"

	aiart "github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/aiart/v20221229"
	"github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common"
	"github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common/errors"
	"github.com/tencentcloud/tencentcloud-sdk-go/tencentcloud/common/profile"
)

type SDTxt2ImgArgs struct {
	Prompt         string `json:"prompt"`
	NegativePrompt string `json:"negative_prompt"`
	SamplerIndex   string `json:"sampler_index"`
	Seed           int64  `json:"seed"`
	Steps          int64  `json:"steps"`
	Width          int64  `json:"width"`
	Height         int64  `json:"height"`
	CFGScale       int64  `json:"cfg_scale"`
}

type SDImg2ImgArgs struct {
	InitImages     []string `json:"init_images"`
	Prompt         string   `json:"prompt"`
	NegativePrompt string   `json:"negative_prompt"`
	SamplerIndex   string   `json:"sampler_index"`
	Seed           int64    `json:"seed"`
	Steps          int64    `json:"steps"`
	Width          int64    `json:"width"`
	Height         int64    `json:"height"`
	CFGScale       int64    `json:"cfg_scale"`
}

func PostSDTxt2Img(paras jmap) (jmap, error) {
	r := make(jmap)

	requestBody, err := json.Marshal(paras)
	if err != nil {
		fmt.Println("Json Marshak err:", err)
		return nil, err
	}

	response, err := http.Post(Text2ImgURL, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Println("HTTP POST request failed:", err)
		return nil, err
	}
	defer response.Body.Close()

	err = json.NewDecoder(response.Body).Decode(&r)
	if err != nil {
		fmt.Println("Error decoding JSON response:", err)
		return nil, err
	}

	return r, nil
}

func PostSDImg2Img(paras jmap) (jmap, error) {
	r := make(jmap)

	requestBody, err := json.Marshal(paras)
	if err != nil {
		fmt.Println("Json Marshak err:", err)
		return nil, err
	}

	response, err := http.Post(Img2ImgURL, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Println("HTTP POST request failed:", err)
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		err = fmt.Errorf("PostSDImg2Img failed, status code : " + strconv.Itoa(response.StatusCode))
		log.Println(err)
		return nil, err
	}

	err = json.NewDecoder(response.Body).Decode(&r)
	if err != nil {
		fmt.Println("Error decoding JSON response:", err)
		return nil, err
	}

	return r, nil
}

func GetLoras() (jmap, error) {
	var (
		loras jarray
	)
	r := make(jmap)
	response, err := http.Get(LoraURL)
	if err != nil {
		fmt.Println("HTTP Get request failed:", err)
		return nil, err
	}
	defer response.Body.Close()

	err = json.NewDecoder(response.Body).Decode(&loras)
	if err != nil {
		fmt.Println("Error decoding JSON response:", err)
		return nil, err
	}
	r["loras"] = loras
	r["count"] = len(loras)

	return r, nil
}

func getResizedTencentCloudImg2ImgResolution(width, height int64) string {
	availableResolution := make(map[float64]string)
	availableResolution[1.] = "768:768"
	availableResolution[.75] = "768:1024"
	availableResolution[4/3] = "1024:768"

	wdh := float64(width) / float64(height)

	var widthHeightStr string
	if wdh > 1.15 {
		widthHeightStr = availableResolution[4/3]
	} else if wdh < 0.86 {
		widthHeightStr = availableResolution[.75]
	} else {
		widthHeightStr = availableResolution[1.]
	}

	return widthHeightStr
}

func PostTencentCloudImg2Img(paras jmap) (jmap, error) {
	// 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
	credential := common.NewCredential(
		TencentAK,
		TencentSK,
	)
	cpf := profile.NewClientProfile()
	cpf.HttpProfile.Endpoint = "aiart.tencentcloudapi.com"
	client, _ := aiart.NewClient(credential, "ap-shanghai", cpf)

	request := aiart.NewImageToImageRequest()

	request.InputImage = common.StringPtr(paras["init_images"].(jarray)[0].(string))
	request.Prompt = common.StringPtr(paras["prompt"].(string))
	request.NegativePrompt = common.StringPtr(paras["negative_prompt"].(string))
	width := int64(paras["width"].(float64))
	height := int64(paras["height"].(float64))
	widthHeightStr := getResizedTencentCloudImg2ImgResolution(width, height)
	fmt.Println(widthHeightStr)
	request.ResultConfig = &aiart.ResultConfig{
		Resolution: common.StringPtr(widthHeightStr),
	}
	request.LogoAdd = common.Int64Ptr(0)
	request.Strength = common.Float64Ptr(paras["denoising_strength"].(float64) / 2)

	response, err := client.ImageToImage(request)
	if _, ok := err.(*errors.TencentCloudSDKError); ok {
		fmt.Printf("An API error has returned: %s", err)
		return nil, err
	}
	if err != nil {
		return nil, err
	}
	r := make((jmap))
	response.ToJsonString()
	err = json.Unmarshal([]byte(response.ToJsonString()), &r)
	if err != nil {
		return nil, err
	}
	return r, nil
}
