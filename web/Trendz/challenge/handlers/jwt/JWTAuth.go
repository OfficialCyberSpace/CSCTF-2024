package jwt

import (
	"fmt"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var superSecretKey = []byte(os.Getenv("JWT_SECRET_KEY"))
var secretKey = []byte{}

func InitJWT() {
	key, err := os.ReadFile("jwt.secret")
	if err != nil {
		panic(err)
	}
	secretKey = key[:]
	//fmt.Printf("JWT initialized %v\n", secretKey)
}

func GenerateRefreshToken(username string, uuid string) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256,
		jwt.MapClaims{
			"username": username,
			"uuid":     uuid,
			"exp":      time.Now().Add(time.Hour * 24).Unix(),
			"iat":      time.Now().Unix(),
		})

	signedToken, err := token.SignedString([]byte(superSecretKey))
	if err != nil {
		signedToken = ""
	}
	return signedToken, err
}

func GenerateAccessToken(username string, role string) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256,
		jwt.MapClaims{
			"username": username,
			"exp":      time.Now().Add(time.Minute * 10).Unix(),
			"role":     role,
			"iat":      time.Now().Unix(),
		})

	signedToken, err := token.SignedString([]byte(secretKey))
	if err != nil {
		signedToken = ""
	}
	return signedToken, err
}

func ValidateRefreshToken(encodedToken string) (*jwt.Token, error) {
	return jwt.Parse(encodedToken, func(token *jwt.Token) (interface{}, error) {
		_, isValid := token.Method.(*jwt.SigningMethodHMAC)
		if !isValid {
			return nil, fmt.Errorf("invalid token with signing method: %v", token.Header["alg"])
		}
		return []byte(superSecretKey), nil
	})
}

func ValidateAccessToken(encodedToken string) (*jwt.Token, error) {
	return jwt.Parse(encodedToken, func(token *jwt.Token) (interface{}, error) {
		_, isValid := token.Method.(*jwt.SigningMethodHMAC)
		if !isValid {
			return nil, fmt.Errorf("invalid token with signing method: %v", token.Header["alg"])
		}
		return []byte(secretKey), nil
	})
}

func ExtractClaims(encodedToken string) jwt.MapClaims {
	token, _ := jwt.Parse(encodedToken, nil)
	return GetClaims(token)
}

func GetClaims(token *jwt.Token) jwt.MapClaims {
	return token.Claims.(jwt.MapClaims)
}
