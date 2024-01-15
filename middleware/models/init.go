package models

import (
	openai "github.com/sashabaranov/go-openai"
)

type jarray = []interface{}
type jmap = map[string]interface{}

type jset = map[string]bool

var (
	GlmChatURL       string
	Text2ImgURL      string
	Img2ImgURL       string
	LoraURL          string
	OpenAIClient1    *openai.Client
	OpenAIClient2    *openai.Client
	OpenAIKey        string
	TencentAK        string
	TencentSK        string
	HuggingFaceToken string
	SegformerB5URL   string

	ChatGPTHead     string
	ChatGPTMessages []openai.ChatCompletionMessage
)

func init() {

}
