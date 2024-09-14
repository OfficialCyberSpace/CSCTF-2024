package service

import (
	"app/handlers/db"
	"fmt"
	"os"
	"regexp"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/microcosm-cc/bluemonday"
)

type Post struct {
	PostID string
	Title  string
	Data   string
	User   string
}

func InsertPost(username string, title string, data string) string {
	DB := db.GetDBconn()
	postID := uuid.New().String()
	_, err := DB.Exec("INSERT INTO posts (postid, username, title, data) VALUES ($1, $2, $3, $4)", postID, username, title, data)
	if err != nil {
		fmt.Println(err)
	}
	return postID
}

func GetAllPosts() []Post {
	DB := db.GetDBconn()
	rows, err := DB.Query("SELECT postid, title, username FROM posts")
	if err != nil {
		fmt.Println(err)
	}
	var posts []Post
	for rows.Next() {
		var post Post
		post.Data = ""
		err := rows.Scan(&post.PostID, &post.Title, &post.User)
		if strings.Contains(post.Title, "Welcome") {
			post.User = "NA :)"
		}
		if err != nil {
			fmt.Println(err)
		}
		posts = append(posts, post)
	}
	return posts
}

func GetPostsByUsername(username string) []Post {
	DB := db.GetDBconn()
	rows, err := DB.Query("SELECT postid, title FROM posts WHERE username = $1", username)
	if err != nil {
		fmt.Println(err)
	}
	var posts []Post
	for rows.Next() {
		var post Post
		post.Data = ""
		post.User = username
		err := rows.Scan(&post.PostID, &post.Title)
		if err != nil {
			fmt.Println(err)
		}
		posts = append(posts, post)
	}
	return posts
}

func CheckNoOfPosts(username string) int {
	DB := db.GetDBconn()
	var count int
	err := DB.QueryRow("SELECT COUNT(*) FROM posts WHERE username = $1", username).Scan(&count)
	if err != nil {
		fmt.Println(err)
	}
	return count
}

func SanitizeData(data string) string {
	p := bluemonday.NewPolicy()
	p.AllowURLSchemesMatching(regexp.MustCompile("^https?"))
	p.AllowAttrs("alt", "cite", "datetime", "dir", "high", "hx-delete", "hx-get", "hx-patch", "hx-post", "hx-put", "hx-swap", "hx-target", "hx-trigger", "hx-vals", "id", "low", "map", "max", "min", "name", "optimum", "value").OnElements("a", "abbr", "acronym", "b", "br", "cite", "code", "dfn", "div", "em", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "hr", "i", "mark", "p", "pre", "s", "samp", "small", "span", "strike", "strong", "sub", "sup", "tt", "var", "wbr")
	html := p.Sanitize(data)
	return html
}

func ShowPost(ctx *gin.Context) {
	postID := ctx.Param("postid")
	DB := db.GetDBconn()
	var title string
	var data string
	err := DB.QueryRow("SELECT title, data FROM posts WHERE postid = $1", postID).Scan(&title, &data)
	if err != nil {
		fmt.Println(err)
	}
	html := SanitizeData(data)
	ctx.PureJSON(200, gin.H{
		"title": title, "data": html})
}

func CreatePost(ctx *gin.Context) {
	username := ctx.MustGet("username").(string)
	noOfPosts := CheckNoOfPosts(username)
	var req struct {
		Title string `json:"title"`
		Data  string `json:"data"`
	}
	if err := ctx.BindJSON(&req); err != nil {
		ctx.JSON(400, gin.H{"error": "Invalid request"})
		fmt.Println(err)
		return
	}
	if noOfPosts >= 10 {
		ctx.JSON(200, gin.H{"error": "You have reached the maximum number of posts"})
		return
	}
	if len(req.Data) > 210 {
		ctx.JSON(200, gin.H{"error": "Data length should be less than 210 characters"})
		return
	}
	postID := InsertPost(username, req.Title, req.Data)
	ctx.JSON(200, gin.H{"postid": postID})
}

func DisplayFlag(ctx *gin.Context) {
	username := ctx.MustGet("username").(string)
	noOfPosts := CheckNoOfPosts(username)
	if noOfPosts <= 12 {

		ctx.JSON(200, gin.H{"error": fmt.Sprintf("You need %d more posts to view the flag", 12-noOfPosts)})
		return
	}
	ctx.JSON(200, gin.H{"flag": os.Getenv("POST_FLAG")})
}
