package models

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net/http"
	"os"
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

func PostDALLE2Edit(paras jmap) (jmap, error) {
	r := make(jmap)
	var (
		err error
	)

	if _, ok := paras["init_images"].(jarray)[0].(string); !ok {
		err = fmt.Errorf("err: No init_image")
		log.Println(err)
		return nil, err
	}

	if _, ok := paras["mask_image"].(string); !ok {
		err = fmt.Errorf("err: No mask image")
		log.Println(err)
		return nil, err
	}

	if _, ok := paras["prompt"].(string); !ok {
		err = fmt.Errorf("err: No prompt")
		log.Println(err)
		return nil, err
	}

	// width := int64(paras["width"].(float64))
	// height := int64(paras["height"].(float64))
	// sizeStr := strconv.Itoa(int(width)) + "x" + strconv.Itoa(int(height))
	sizeStr := "512x512"
	log.Println(sizeStr)

	//initImageFile, err := base64ToPNGFile(paras["init_images"].(jarray)[0].(string), "tempt.PNG")
	_, err = base64ToPNGFile(paras["init_images"].(jarray)[0].(string), "tempt.PNG")
	if err != nil {
		log.Println(err)
		return nil, err
	}

	_, err = base64ToPNGFile(paras["mask_image"].(string), "transparent.PNG")
	if err != nil {
		log.Println(err)
		return nil, err
	}

	err = convertRGBToRGBA("tempt.PNG", "tempt_rgba.PNG", false)
	if err != nil {
		log.Println(err)
		return nil, err
	}

	// 设置API密钥
	apiKey := OpenAIKey

	// 设置API端点和请求URL
	apiEndpoint := "https://api.openai.com/v1/images/edits"
	url := apiEndpoint

	// 创建multipart/form-data请求体
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// 添加图像文件字段
	imageFile, err := os.Open("tempt_rgba.PNG")
	if err != nil {
		fmt.Println("Error opening image file:", err)
		return nil, err
	}
	imagePart, err := writer.CreateFormFile("image", "tempt_rgba.PNG")
	if err != nil {
		fmt.Println("Error creating image form file:", err)
		return nil, err
	}
	_, err = io.Copy(imagePart, imageFile)
	if err != nil {
		fmt.Println("Error copy image form file:", err)
		return nil, err
	}

	// 添加透明图片

	transparentFile, err := os.Open("transparent.PNG")
	if err != nil {
		fmt.Println("Error opening image file:", err)
		return nil, err
	}
	transparentPart, err := writer.CreateFormFile("mask", "transparent.PNG")
	if err != nil {
		fmt.Println("Error creating image form file:", err)
		return nil, err
	}
	_, err = io.Copy(transparentPart, transparentFile)
	if err != nil {
		fmt.Println("Error copy image form file:", err)
		return nil, err
	}

	// 添加其他字段
	writer.WriteField("prompt", paras["prompt"].(string))
	writer.WriteField("n", "1")
	writer.WriteField("size", sizeStr)
	writer.WriteField("response_format", "b64_json")

	// 关闭multipart写入器
	writer.Close()

	// 创建HTTP请求
	request, err := http.NewRequest("POST", url, body)
	if err != nil {
		fmt.Println("Error creating HTTP request:", err)
		return nil, err
	}

	// 设置请求头
	request.Header.Set("Content-Type", writer.FormDataContentType())
	request.Header.Set("Authorization", "Bearer "+apiKey)

	// a, _ := io.ReadAll(request.Body)
	// fmt.Println(string(a))

	// 发送请求并获取响应
	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		fmt.Println("Error sending HTTP request:", err)
		return nil, err
	}
	defer response.Body.Close()

	// 读取并打印响应内容
	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		fmt.Println("Error reading response body:", err)
		return nil, err
	}

	if err != nil {
		fmt.Printf("Image creation error: %v\n", err)
		return nil, err
	}

	var responseJson jmap
	err = json.Unmarshal(responseBody, &responseJson)
	if err != nil {
		fmt.Println("解析JSON时发生错误:", err)
		return nil, err
	}

	if _, ok := responseJson["data"].(jarray); !ok {
		log.Println(responseJson)
		err = fmt.Errorf("err: DALLE Get image error")
		log.Println(err)
		return nil, err
	}

	if _, ok := responseJson["data"].(jarray)[0].(jmap)["b64_json"].(string); !ok {
		err = fmt.Errorf("err: DALLE Get image error")

		log.Println(err)
		return nil, err
	}

	imgStr := responseJson["data"].(jarray)[0].(jmap)["b64_json"].(string)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	var images jarray
	images = append(images, imgStr)
	r["images"] = images
	return r, nil
}

func PostHuggingFaceImgSegment(image string) (jarray, error) {
	requestBody, err := json.Marshal(map[string]string{"image": image})
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", SegformerB5URL, bytes.NewBuffer(requestBody))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", "Bearer "+HuggingFaceToken)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	responseBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var result interface{}
	if err := json.Unmarshal(responseBody, &result); err != nil {
		return nil, err
	}

	switch result.(type) {
	case jmap:
		err = fmt.Errorf(result.(jmap)["error"].(string))
		log.Println(err)
		return nil, err
	case jarray:
		return result.(jarray), nil
	default:
		return nil, fmt.Errorf("err: unknown err")
	}
}
