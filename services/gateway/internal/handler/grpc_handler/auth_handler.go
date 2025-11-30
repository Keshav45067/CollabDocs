package grpchandler

import (
	authv1 "gateway/proto/auth/v1"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Login(data *authv1.LoginRequest, authClient authv1.AuthServiceClient, ctx *gin.Context) *authv1.LoginResponse {
	out, err := authClient.Login(ctx, data)
	if err != nil {
		ctx.AbortWithStatus(http.StatusUnauthorized)
	}
	return out
}
