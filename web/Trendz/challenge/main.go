package main

import (
	"app/handlers/custom"
	"app/handlers/dashboard"
	"app/handlers/db"
	"app/handlers/jwt"
	"app/handlers/service"

	"github.com/gin-gonic/gin"
)

func main() {
	s := gin.Default()
	s.LoadHTMLGlob("templates/*")
	db.InitDBconn()
	jwt.InitJWT()

	s.GET("/", func(c *gin.Context) {
		c.Redirect(302, "/login")
	})
	s.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})
	r := s.Group("/")
	r.POST("/register", service.CreateUser)
	r.GET("/register", func(c *gin.Context) {
		c.HTML(200, "register.tmpl", gin.H{})
	})
	r.POST("/login", service.LoginUser)
	r.GET("/login", func(c *gin.Context) {
		c.HTML(200, "login.tmpl", gin.H{})
	})

	r.GET("/getAccessToken", service.GenerateAccessToken)

	authorizedEndpoints := r.Group("/user")
	authorizedEndpoints.Use(service.AuthorizeAccessToken())
	authorizedEndpoints.GET("/dashboard", dashboard.UserDashboard)
	authorizedEndpoints.POST("/posts/create", service.CreatePost)
	authorizedEndpoints.GET("/posts/:postid", service.ShowPost)
	authorizedEndpoints.GET("/flag", service.DisplayFlag)

	adminEndpoints := r.Group("/admin")
	adminEndpoints.Use(service.AuthorizeAccessToken())
	adminEndpoints.Use(service.ValidateAdmin())
	adminEndpoints.GET("/dashboard", dashboard.AdminDashboard)

	SAEndpoints := r.Group("/superadmin")
	SAEndpoints.Use(service.AuthorizeAccessToken())
	SAEndpoints.Use(service.ValidateAdmin())
	SAEndpoints.Use(service.AuthorizeRefreshToken())
	SAEndpoints.Use(service.ValidateSuperAdmin())
	SAEndpoints.GET("/viewpost/:postid", dashboard.ViewPosts)
	SAEndpoints.GET("/dashboard", dashboard.SuperAdminDashboard)
	s.NoRoute(custom.Custom404Handler)
	s.Run(":8000")
}
