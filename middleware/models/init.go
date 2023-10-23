package models

import (
	openai "github.com/sashabaranov/go-openai"
)

type jarray = []interface{}
type jmap = map[string]interface{}

type jset = map[string]bool

var (
	ChatBotURL   string
	ChatBotAK    string
	ChatBotSK    string
	Text2ImgURL  string
	LoraURL      string
	OpenAIClient *openai.Client
)

func init() {

}
