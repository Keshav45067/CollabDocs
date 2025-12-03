package grpchandler

import (
	authv1 "gateway/proto/auth/v1"
	"gateway/utils"
	"net/http"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc/status"
)

func Login(data *authv1.LoginRequest, authClient authv1.AuthServiceClient, ctx *gin.Context) *authv1.LoginResponse {
	grpcCtx := ctx.Request.Context()

	out, err := authClient.Login(grpcCtx, data)
	if err != nil {
		st, ok := status.FromError(err)
		if !ok {
			ctx.JSON(http.StatusInternalServerError, gin.H{
				"success": false,
				"message": "Failed to reach auth service",
			})
			ctx.Abort()
			return nil
		}

		httpStatus := utils.HttpStatusFromGRPCCode(st.Code())

		ctx.JSON(httpStatus, gin.H{
			"success": false,
			"message": st.Message(),
			"code":    st.Code().String(),
		})
		ctx.Abort()
		return nil
	}

	return out

}
