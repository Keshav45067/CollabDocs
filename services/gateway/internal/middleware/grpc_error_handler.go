package middleware

import (
	"gateway/utils"

	"github.com/gin-gonic/gin"
)

func GrpcErrorRecovery() gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {

			if r := recover(); r != nil {
				if ge, ok := r.(*utils.GrpcHTTPError); ok {
					c.JSON(ge.HTTPStatus, gin.H{
						"success": false,
						"message": ge.Message,
						"code":    ge.GRPCCode.String(),
					})
					c.Abort()
					return
				}
				panic(r)
			}
		}()

		c.Next()
	}
}
