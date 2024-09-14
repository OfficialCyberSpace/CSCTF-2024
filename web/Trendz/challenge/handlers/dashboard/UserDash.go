package dashboard

import (
	"app/handlers/service"
	"fmt"

	"github.com/gin-gonic/gin"
)

func UserDashboard(ctx *gin.Context) {
	username := ctx.MustGet("username").(string)
	role := ctx.MustGet("role").(string)
	fmt.Println("User dashboard accessed")
	posts := service.GetPostsByUsername(username)
	ctx.HTML(200, "userDash.tmpl", gin.H{
		"username": username,
		"role":     role,
		"posts":    posts,
		"title":    "{{title}}",
		"data":     "{{data|safe}}",
	})
}
