package service

import (
	"app/handlers/db"
	"app/handlers/jwt"
	"fmt"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type LoginUserRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type LoginUserResponse struct {
	Message string `json:"message"`
	Succes  bool   `json:"success"`
}

func LoginUser(ctx *gin.Context) {
	var req LoginUserRequest
	if err := ctx.BindJSON(&req); err != nil {
		ctx.JSON(400, gin.H{"error": "Invalid request"})
		fmt.Println(err)
		return
	}
	DB := db.GetDBconn()

	var count int
	var hash string
	var userRole string
	err := DB.QueryRow("SELECT COUNT(*) FROM users WHERE username = $1", req.Username).Scan(&count)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	if count == 0 {
		ctx.JSON(400, LoginUserResponse{Message: "Invalid credentials"})
		return
	}
	err = DB.QueryRow("SELECT password,role FROM users WHERE username = $1", req.Username).Scan(&hash, &userRole)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	if !CheckPasswordHash(req.Password, hash) {
		ctx.JSON(400, LoginUserResponse{Message: "Invalid credentials"})
		return
	}
	uid := uuid.New().String()
	token, err := jwt.GenerateRefreshToken(req.Username, uid)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	accessToken, err := jwt.GenerateAccessToken(req.Username, userRole)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	_, err = DB.Exec("INSERT INTO session (username, uuid, expiry) VALUES ($1, $2, $3)", req.Username, uid, time.Now().Add(time.Hour*24))
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Internal server error"})
		fmt.Println(err)
		return
	}
	ctx.SetCookie("refreshtoken", token, 86400, "/", "", false, true)
	ctx.SetCookie("accesstoken", accessToken, 600, "/", "", false, false)
	ctx.Header("HX-Redirect", "/user/dashboard")
	ctx.JSON(200, LoginUserResponse{Message: "Login successful", Succes: true})
}
func CheckPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}
