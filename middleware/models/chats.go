package models

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

func postChatGPT(query string) (error, jmap) {
	r := make(jmap)
	// 创建一个 JSON 数据作为请求体
	requestBody := []byte(`{"key1": "value1", "key2": "value2"}`)

	// 发送 POST 请求
	response, err := http.Post("https://example.com/api/endpoint", "application/json", bytes.NewBuffer(requestBody))
	if err != nil {
		fmt.Println("HTTP POST request failed:", err)
		return err, nil
	}
	defer response.Body.Close()

	// 读取响应
	responseData := make([]byte, 4096)
	_, err = response.Body.Read(responseData)
	if err != nil {
		fmt.Println("Error reading response:", err)
		return err, nil
	}
	err = json.Unmarshal(responseData, &r)
	if err != nil {
		fmt.Println("Error Unmarshal response:", err)
		return err, nil
	}

	return nil, r
}
