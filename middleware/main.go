package main

import (
	_ "middleware/routers"

	beego "github.com/beego/beego/v2/server/web"
)

func main() {
	beego.Run()
}
