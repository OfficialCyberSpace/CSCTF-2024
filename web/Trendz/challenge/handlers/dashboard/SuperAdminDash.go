package dashboard

import (
	"fmt"
	"os"

	"github.com/gin-gonic/gin"
)

func SuperAdminDashboard(ctx *gin.Context) {
	fmt.Println("SuperAdmin dashboard accessed")
	ctx.HTML(200, "superAdminDash.tmpl", gin.H{
		"flag": os.Getenv("SUPERADMIN_FLAG"),
	})
}

func ViewPosts(ctx *gin.Context) {
	ctx.HTML(200, "viewPost.tmpl", gin.H{
		"PostID": ctx.Param("postid"),
		"title":  "Click",
		"data":   "{{data|safe}}",
	})
}
