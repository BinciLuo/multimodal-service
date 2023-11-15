package models

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"

	openai "github.com/sashabaranov/go-openai"
)

func PostGPT3Dot5Turbo(query string) (jmap, error) {
	r := make(jmap)

	resp, err := OpenAIClient1.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model: openai.GPT3Dot5Turbo,
			Messages: []openai.ChatCompletionMessage{
				{
					Role:    openai.ChatMessageRoleUser,
					Content: query,
				},
			},
		},
	)

	if err != nil {
		log.Printf("ChatCompletion fallback to client2. error: %v\n, ", err)
		resp, err = OpenAIClient2.CreateChatCompletion(
			context.Background(),
			openai.ChatCompletionRequest{
				Model: openai.GPT3Dot5Turbo,
				Messages: []openai.ChatCompletionMessage{
					{
						Role:    openai.ChatMessageRoleUser,
						Content: query,
					},
				},
			},
		)

		if err != nil {
			log.Printf("ChatCompletion client2 error: %v\n, ", err)
			return nil, err
		}
	}

	r["chat"] = resp.Choices[0].Message.Content
	return r, nil
}

func PostChatGLM2_6B(params jmap) (jmap, error) {
	r := make(jmap)

	requestBody, err := json.Marshal(params)
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
		return nil, err
	}
	err = json.NewDecoder(response.Body).Decode(&r)
	if err != nil {
		log.Println("[models/PostChatGLM2_6] Error decoding JSON response:", err)
		return nil, err
	}

	return r, nil

}
