package service

import (
	"app/handlers/db"
	"app/handlers/jwt"
	"fmt"

	"github.com/gin-gonic/gin"
)

func ValidateAdmin() gin.HandlerFunc {
	return func(c *gin.Context) {
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
		claims := jwt.ExtractClaims(tokenString)
		if claims["role"] == "admin" || claims["role"] == "superadmin" {
			fmt.Println(claims)
		} else {
			fmt.Println("Token is not valid")
			c.AbortWithStatusJSON(403, gin.H{"error": "User Unauthorized"})
			return
		}
	}
}

func ValidateSuperAdmin() gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Cookie("refreshtoken")
		if err != nil {
			c.JSON(401, gin.H{"error": "Unauthorized"})
			return
		}
		claims := jwt.ExtractClaims(token)
		username := claims["username"]
		DB := db.GetDBconn()
		var role string
		err = DB.QueryRow("SELECT role FROM users WHERE username = $1", username).Scan(&role)
		if err != nil {
			c.JSON(500, gin.H{"error": "Internal server error"})
			fmt.Println(err)
			return
		}
		if role == "superadmin" {
			fmt.Println(claims)
		} else {
			fmt.Println("Token is not valid")
			c.AbortWithStatus(403)
		}
	}
}
