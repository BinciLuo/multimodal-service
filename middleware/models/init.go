package models

type jarray = []interface{}
type jmap = map[string]interface{}

type jset = map[string]bool

var (
	ChatBotURL   string
	ChatBotAK    string
	ChatBotSK    string
	ChatBotPort  int64
	Text2ImgURL  string
	Text2ImgAK   string
	Text2ImgSK   string
	Text2ImgPort int64
)

func init() {

}
