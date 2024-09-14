package service

import (
	"app/handlers/db"
	"fmt"

	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

type CreateUserRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type CreateUserResponse struct {
	Message string `json:"message"`
}

func CreateUser(ctx *gin.Context) {
	var req CreateUserRequest
	if err := ctx.BindJSON(&req); err != nil {
		ctx.JSON(400, gin.H{"error": "Invalid request"})
		fmt.Println(err)
		return
	}
	DB := db.GetDBconn()

	var count int
	err := DB.QueryRow("SELECT COUNT(*) FROM users WHERE username = $1", req.Username).Scan(&count)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	if count > 0 {
		ctx.JSON(400, gin.H{"error": "User already exists"})
		return
	}

	userRole := "user"
	_, err = DB.Exec("INSERT INTO users (username, password, role) VALUES ($1, $2, $3)", req.Username, hashPassword(req.Password), userRole)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}

	ctx.Redirect(302, "/login")
}

func hashPassword(password string) string {
	hp, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		panic(err)
	}
	return string(hp)
}
