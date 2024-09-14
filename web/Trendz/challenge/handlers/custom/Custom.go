package custom

import (
	"encoding/base64"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func check(customHeader string) bool {
	array := make([]int, len(customHeader))
	for i, c := range customHeader {
		array[i] = int(c)
	}
	if array[0]+array[21] != 114 {
		return false
	}
	if array[1]*array[16] != 11413 {
		return false
	}
	if array[2]+array[11] != 174 {
		return false
	}
	if array[3]+array[9] != 157 {
		return false
	}
	if array[4]^array[2] != 78 {
		return false
	}
	if array[5]+array[19] != 155 {
		return false
	}
	if array[6]+array[24] != 142 {
		return false
	}
	if array[7]*array[21] != 3080 {
		return false
	}
	if array[8]-array[28] != 72 {
		return false
	}
	if array[9]-array[31] != -47 {
		return false
	}
	if array[10]+array[9] != 165 {
		return false
	}
	if array[11]*array[6] != 3920 {
		return false
	}
	if array[12]^array[6] != 15 {
		return false
	}
	if array[13]-array[14] != -48 {
		return false
	}
	if array[14]^array[21] != 26 {
		return false
	}
	if array[15]*array[16] != 12726 {
		return false
	}
	if array[16]*array[13] != 3939 {
		return false
	}
	if array[17]-array[31] != 31 {
		return false
	}
	if array[18]+array[29] != 82 {
		return false
	}
	if array[19]*array[2] != 5928 {
		return false
	}
	if array[20]+array[6] != 109 {
		return false
	}
	if array[21]*array[30] != 3696 {
		return false
	}
	if array[22]-array[24] != -32 {
		return false
	}
	if array[23]+array[27] != 201 {
		return false
	}
	if array[24]-array[4] != 48 {
		return false
	}
	if array[25]-array[6] != 51 {
		return false
	}
	if array[26]-array[10] != -18 {
		return false
	}
	if array[27]+array[12] != 159 {
		return false
	}
	if array[28]^array[3] != 95 {
		return false
	}
	if array[29]-array[9] != 29 {
		return false
	}
	if array[30]^array[26] != 87 {
		return false
	}
	if array[31]+array[4] != 129 {
		return false
	}
	if array[20]+array[10] != 174 {
		return false
	}
	if array[11]^array[16] != 35 {
		return false
	}
	if array[4]*array[23] != 3686 {
		return false
	}
	if array[3]*array[26] != 11639 {
		return false
	}
	if array[31]^array[12] != 108 {
		return false
	}
	if array[12]*array[30] != 2640 {
		return false
	}
	if array[20]*array[14] != 4611 {
		return false
	}
	if array[10]^array[19] != 64 {
		return false
	}
	if array[0]+array[23] != 134 {
		return false
	}
	if array[9]-array[12] != -11 {
		return false
	}
	if array[4]*array[19] != 2166 {
		return false
	}
	if array[15]^array[8] != 8 {
		return false
	}
	if array[15]^array[11] != 56 {
		return false
	}
	if array[22]*array[2] != 5616 {
		return false
	}
	if array[19]^array[24] != 111 {
		return false
	}
	if array[0]+array[16] != 138 {
		return false
	}
	if array[18]*array[16] != 909 {
		return false
	}
	if array[29]*array[15] != 9198 {
		return false
	}
	if array[9]+array[27] != 148 {
		return false
	}
	if array[20]*array[0] != 1961 {
		return false
	}
	if array[8]+array[15] != 244 {
		return false
	}
	if array[23]+array[30] != 145 {
		return false
	}
	if array[19]*array[12] != 3135 {
		return false
	}
	if array[26]*array[8] != 12154 {
		return false
	}
	if array[2]^array[0] != 77 {
		return false
	}
	if array[12]-array[19] != -2 {
		return false
	}
	if array[19]^array[24] != 111 {
		return false
	}
	if array[22]-array[28] != 8 {
		return false
	}

	return true
}

func Custom404Handler(c *gin.Context) {
	if c.Request.Method == http.MethodConnect {
		customHeader := c.GetHeader("X-Super-Secret")
		testVal, _ := base64.StdEncoding.DecodeString(customHeader)
		if check(string(testVal)) {
			c.JSON(404, gin.H{"error": "Here your flag: " + os.Getenv("REV_FLAG")})
			return
		}
		return
	}

	c.JSON(404, gin.H{"error": "Resource not found"})
}
