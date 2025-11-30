package httpHandler

import (
	"gateway/internal/client"
	"gateway/internal/controller"

	"github.com/gin-gonic/gin"
)

func AuthHTTPRouter(auth *gin.RouterGroup, clients *client.Clients) *gin.RouterGroup {
	authController := controller.AuthController{
		AuthClient: clients.AuthClient,
	}
	auth.POST("/login", authController.Login())

	return auth
}
