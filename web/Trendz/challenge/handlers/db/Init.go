package db

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/lib/pq"
)

var (
	DB *sql.DB
)

func InitDBconn() {

	var host string = "localhost" //os.Getenv("DB_HOST" )
	var db_user string = os.Getenv("POSTGRES_USER")
	var db_password string = os.Getenv("POSTGRES_PASSWORD")
	var db_name string = os.Getenv("POSTGRES_DB")
	sqlconn := fmt.Sprintf("host=%v user=%v password=%v dbname=%v sslmode=disable", host, db_user, db_password, db_name)
	fmt.Println(sqlconn)
	d, err := sql.Open("postgres", sqlconn)
	if err != nil {
		panic(err)
	}
	DB = d
}

func GetDBconn() *sql.DB {
	return DB
}
