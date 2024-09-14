package service

import (
	"app/handlers/db"
	"app/handlers/jwt"
	"fmt"

	"github.com/gin-gonic/gin"
)

func AuthorizeRefreshToken() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		refreshToken, err := ctx.Cookie("refreshtoken")
		if refreshToken == "" || err != nil {
			ctx.JSON(401, gin.H{"error": "Unauthorized"})
			return
		}
		token, err := jwt.ValidateRefreshToken(refreshToken)
		if err != nil {
			ctx.JSON(401, gin.H{"error": "Unauthorized"})
			return
		}
		fmt.Println(token)
		if token.Valid {
			claims := jwt.GetClaims(token)
			ctx.Set("username", claims["username"])
		} else {
			ctx.JSON(401, gin.H{"error": "Unauthorized"})
		}

	}

}

func AuthorizeAccessToken() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("X-Frame-Options", "DENY")
		c.Header("X-XSS-Protection", "1; mode=block")
		const bearerSchema = "Bearer "
		var tokenDetected bool = false
		var tokenString string
		authHeader := c.GetHeader("Authorization")
		if len(authHeader) != 0 {
			tokenDetected = true
			tokenString = authHeader[len(bearerSchema):]
		}
		if !tokenDetected {
			var err error
			tokenString, err = c.Cookie("accesstoken")
			if tokenString == "" || err != nil {
				c.Redirect(302, "/getAccessToken?redirect="+c.Request.URL.Path)
			}
		}
		fmt.Println(tokenString)
		token, err := jwt.ValidateAccessToken(tokenString)
		if err != nil {
			fmt.Println(err)
			c.AbortWithStatus(403)
		}
		if token.Valid {
			claims := jwt.GetClaims(token)
			fmt.Println(claims)
			c.Set("username", claims["username"])
			c.Set("role", claims["role"])
		} else {
			fmt.Println("Token is not valid")
			c.Header("HX-Redirect", "/getAccessToken")
			c.AbortWithStatus(403)
		}

	}
}

func GenerateAccessToken(ctx *gin.Context) {
	//run authorize refresh token middleware
	AuthorizeRefreshToken()(ctx)
	username := ctx.MustGet("username").(string)
	db := db.GetDBconn()
	var role string
	err := db.QueryRow("SELECT role FROM users WHERE username = $1", username).Scan(&role)
	if err != nil {
		fmt.Println(err)
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		return
	}
	accessToken, err := jwt.GenerateAccessToken(username, role)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	ctx.SetCookie("accesstoken", accessToken, 600, "/", "", false, true)
	redirect := ctx.Query("redirect")
	if redirect != "" {
		ctx.Redirect(302, redirect)
		return
	}
	ctx.JSON(200, gin.H{"accesstoken": accessToken})
}
