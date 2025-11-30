package controller

import (
	authv1 "gateway/proto/auth/v1"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

type AuthController struct {
	AuthClient authv1.AuthServiceClient
}

// func NewAuthController(authClient authv1.AuthServiceClient) *AuthController {
// 	return &AuthController{
// 		authClient: authClient,
// 	}
// }

func (ctr *AuthController) Login() gin.HandlerFunc {
	return func(c *gin.Context) {
		var parsedData authv1.LoginRequest
		if err := c.ShouldBindJSON(&parsedData); err != nil {
			c.AbortWithStatus(http.StatusUnprocessableEntity)
		}
		log.Print("Login working")
		_, err := ctr.AuthClient.Login(c, &parsedData)
		if err != nil {
			c.AbortWithStatus(http.StatusBadRequest)
		}

		c.JSON(http.StatusOK, gin.H{
			"message": "Hello",
		})
	}
}
