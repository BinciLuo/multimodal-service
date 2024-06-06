package models

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strconv"

	openai "github.com/sashabaranov/go-openai"
)

func PostGPT3Dot5Turbo(query string, history jarray) (jmap, error) {
	r := make(jmap)

	FormChatGPTMessages(ChatGPTHead, history)
	UpdateChatGPTUserChatMessages(query)
	resp, err := OpenAIClient2.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model:    openai.GPT3Dot5Turbo,
			Messages: ChatGPTMessages,
		},
	)

	if err != nil {
		log.Printf("ChatCompletion client2 error: %v\n, ", err)
		return nil, err
	}

	r["chat"] = resp.Choices[0].Message.Content
	return r, nil
}

func PostGPT4(query string, history jarray) (jmap, error) {
	r := make(jmap)

	FormChatGPTMessages(ChatGPTHead, history)
	UpdateChatGPTUserChatMessages(query)
	resp, err := OpenAIClient2.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model:    openai.GPT4,
			Messages: ChatGPTMessages,
		},
	)

	if err != nil {
		log.Printf("ChatCompletion client2 error: %v\n, ", err)
		return nil, err
	}

	r["chat"] = resp.Choices[0].Message.Content
	return r, nil
}

func PostChatGLM2_6B(query string, history jarray) (jmap, error) {
	r := make(jmap)
	paras := make(jmap)
	resp := make(jmap)

	paras["model"] = "chatglm2-6b"
	paras["messages"] = FormChatGLM2Messages(ChatGPTHead, query, history)
	paras["temperature"] = 0.7
	paras["top_p"] = 0.5
	paras["n"] = 1
	paras["max_tokens"] = 128
	paras["stream"] = false

	requestBody, err := json.Marshal(paras)
	if err != nil {
		log.Println("Json Marshak err:", err)
		return nil, err
	}

	response, err := http.Post(GlmChatURL, "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		log.Println("HTTP POST request failed:", err)
		return nil, err
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		err = fmt.Errorf(" PostChatGLM2_6B not avliable, status code : " + strconv.Itoa(response.StatusCode))
		// 读取并打印响应结果
		responseBody, _ := ioutil.ReadAll(response.Body)
		fmt.Println("POST请求的响应结果:", string(responseBody))
		return nil, err
	}
	err = json.NewDecoder(response.Body).Decode(&r)
	if err != nil {
		log.Println("[models/PostChatGLM2_6] Error decoding JSON response:", err)
		return nil, err
	}

	resp["chat"] = r["choices"].(jarray)[0].(jmap)["message"].(jmap)["content"]

	return resp, nil

}

func PostGPT4V(query string, history jarray, init_image string) (jmap, error) {
	r := make(jmap)
	apiURL := "https://api.openai.com/v1/chat/completions"
	openaiAPIKey := OpenAIKey

	// 构建请求体数据
	data := jmap{
		"model":      "gpt-4-vision-preview",
		"messages":   FormGPT4VMessages(ChatGPTHead, query, init_image, history),
		"max_tokens": 300,
	}

	// 将请求体数据转换为JSON格式
	payload, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}

	// 发送POST请求到OpenAI API
	req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(payload))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", openaiAPIKey))

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// 读取API响应
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// 解析响应数据为JSON格式
	var result jmap
	err = json.Unmarshal(body, &result)
	if err != nil {
		return nil, err
	}
	r["chat"] = result["choices"].(jarray)[0].(jmap)["message"].(jmap)["content"]
	return r, nil
}
