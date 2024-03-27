package models

import (
	"encoding/base64"
	"fmt"
	"image"
	"image/color"
	"image/png"
	"io/ioutil"
	"net/http"
	"os"
	"strings"

	openai "github.com/sashabaranov/go-openai"
)

func convertRGBToRGBA(inputPath, outputPath string, mask bool) error {
	// 打开PNG文件
	inputFile, err := os.Open(inputPath)
	if err != nil {
		return fmt.Errorf("无法打开文件: %v", err)
	}
	defer inputFile.Close()

	// 解码PNG文件
	img, _, err := image.Decode(inputFile)
	if err != nil {
		return fmt.Errorf("无法解码图像: %v", err)
	}

	// 创建一个新的RGBA图像
	bounds := img.Bounds()
	rgbaImg := image.NewRGBA(bounds)

	// 将RGB图像的像素复制到新的RGBA图像中
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			r, g, b, _ := img.At(x, y).RGBA()
			if mask && uint8(r) == 0 && uint8(g) == 0 && uint8(b) == 0 {
				rgbaImg.Set(x, y, color.RGBA{0, 0, 0, 0})
			} else {
				rgbaImg.Set(x, y, color.RGBA{uint8(r), uint8(g), uint8(b), 254})
			}
		}
	}

	// 保存新的RGBA图像到文件
	outputFile, err := os.Create(outputPath)
	if err != nil {
		return fmt.Errorf("无法创建输出文件: %v", err)
	}
	defer outputFile.Close()

	// 编码为PNG格式
	err = png.Encode(outputFile, rgbaImg)
	if err != nil {
		return fmt.Errorf("无法编码图像: %v", err)
	}

	fmt.Println("转换成功，输出文件为", outputPath)
	return nil
}

func base64ToPNGFile(base64String, outputFileName string) (*os.File, error) {
	// 解码Base64字符串为字节数组
	decoded, err := base64.StdEncoding.DecodeString(base64String)
	if err != nil {
		return nil, err
	}

	// 创建图片对象
	img, _, err := image.Decode(strings.NewReader(string(decoded)))
	if err != nil {
		return nil, err
	}

	// 创建输出文件
	file, err := os.Create(outputFileName)
	if err != nil {
		return nil, err
	}

	// 将图片对象写入文件
	err = png.Encode(file, img)
	if err != nil {
		return nil, err
	}

	return file, nil
}

func base64ToStr(base64String string) (string, error) {
	// 将Base64字符串解码为字节数组
	decoded, err := base64.StdEncoding.DecodeString(base64String)
	if err != nil {
		return "", err
	}

	// 将字节数组转换为字符串
	result := string(decoded)
	return result, nil
}

func imagUrlToBase64(url string) (string, error) {
	// 发送HTTP GET请求
	response, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer response.Body.Close()

	// 读取图片内容
	imageData, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return "", err
	}

	// 将图片内容转换为Base64字符串
	base64String := base64.StdEncoding.EncodeToString(imageData)

	return base64String, nil
}

func UpdateChatGPTUserChatMessages(newMessage string) {
	// 将新消息添加到全局变量中
	ChatGPTMessages = append(ChatGPTMessages, openai.ChatCompletionMessage{
		Role:    openai.ChatMessageRoleUser,
		Content: newMessage,
	})

	// 限制消息数量为最近的20条
	if len(ChatGPTMessages) > 20 {
		ChatGPTMessages = ChatGPTMessages[len(ChatGPTMessages)-20:]
	}
}

func UpdateChatbotChatGPTChatMessages(newMessage string) {
	// 将新消息添加到全局变量中
	ChatGPTMessages = append(ChatGPTMessages, openai.ChatCompletionMessage{
		Role:    openai.ChatMessageRoleAssistant,
		Content: newMessage,
	})

	// 限制消息数量为最近的20条
	if len(ChatGPTMessages) > 20 {
		ChatGPTMessages = ChatGPTMessages[len(ChatGPTMessages)-20:]
	}
}

func FormChatGPTMessages(head string, history jarray) {
	ChatGPTMessages = []openai.ChatCompletionMessage{}
	UpdateChatbotChatGPTChatMessages(head)
	for _, round := range history {
		UpdateChatGPTUserChatMessages(round.(jarray)[0].(string))
		UpdateChatbotChatGPTChatMessages(round.(jarray)[1].(string))
	}
}

func FormGPT4VMessages(head, query, init_image string, history jarray) jarray {
	var (
		messgaes jarray
	)
	messgaes = append(messgaes, jmap{"role": "assistant", "content": []jmap{{"type": "text", "text": head}}})
	for _, round := range history {
		messgaes = append(messgaes, jmap{"role": "user", "content": []jmap{{"type": "text", "text": round.(jarray)[0].(string)}}})
		messgaes = append(messgaes, jmap{"role": "assistant", "content": []jmap{{"type": "text", "text": round.(jarray)[1].(string)}}})
	}
	messgaes = append(messgaes, jmap{"role": "user", "content": []jmap{{"type": "text", "text": query}, {"type": "image_url", "image_url": jmap{"url": fmt.Sprintf("data:image/jpeg;base64,%s", init_image)}}}})
	return messgaes
}

func FormChatGLM2Messages(head, query string, history jarray) jarray {
	var (
		messgaes jarray
	)
	// messgaes = append(messgaes, jmap{"role": "user", "content": head})
	// messgaes = append(messgaes, jmap{"role": "assistant", "content": "好的。"})
	for _, round := range history {
		messgaes = append(messgaes, jmap{"role": "user", "content": round.(jarray)[0].(string)})
		messgaes = append(messgaes, jmap{"role": "assistant", "content": round.(jarray)[1].(string)})
	}
	messgaes = append(messgaes, jmap{"role": "user", "content": query})
	return messgaes
}

func getLastNChatGPTMessages(n int) []openai.ChatCompletionMessage {
	// 如果消息数量小于N，返回所有消息
	if len(ChatGPTMessages) <= n {
		return ChatGPTMessages
	}
	// 否则返回最近的N条消息
	return ChatGPTMessages[len(ChatGPTMessages)-n:]
}

func ReadTextFile(filePath string) (string, error) {
	// 读取文件内容
	content, err := ioutil.ReadFile(filePath)
	if err != nil {
		return "", err
	}
	// 将文件内容转换为字符串
	fileContent := string(content)
	return fileContent, nil
}
