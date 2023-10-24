package models

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"

	openai "github.com/sashabaranov/go-openai"
)

func PostGPT3Dot5Turbo(query string) (jmap, error) {
	r := make(jmap)

	resp, err := OpenAIClient.CreateChatCompletion(
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
		fmt.Printf("ChatCompletion error: %v\n", err)
		return nil, err
	}

	r["chat"] = resp.Choices[0].Message.Content
	return r, nil
}

func PostChatGLM2_6B(params jmap) (jmap, error) {
	r := make(jmap)

	requestBody, err := json.Marshal(params)
	if err != nil {
		fmt.Println("Json Marshak err:", err)
		return nil, err
	}
	response, err := http.Post(GlmChatURL, "application/json", bytes.NewBuffer(requestBody))
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
