package models

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

// post_data={'prompt': prompt_str,
//
//	'negative_prompt': data['negative_prompt'],
//	'sampler_index': data['sampler_index'],
//	#'seed': data['seed'],
//	'seed':random.randint(0,4029094098),
//	'steps': data['steps'],
//	'width': data['width'],
//	'height': data['height'],
//	'cfg_scale': data['cfg_scale']}

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

func PostSDTxt2Img(paras SDTxt2ImgArgs) (jmap, error) {
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
