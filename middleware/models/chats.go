package models

import (
	"context"
	"fmt"

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
