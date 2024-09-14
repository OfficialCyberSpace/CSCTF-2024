package dashboard

import (
	"app/handlers/service"
	"os"

	"github.com/gin-gonic/gin"
)

func AdminDashboard(ctx *gin.Context) {
	posts := service.GetAllPosts()
	ctx.HTML(200, "adminDash.tmpl", gin.H{
		"flag":  os.Getenv("ADMIN_FLAG"),
		"posts": posts,
	})
}
