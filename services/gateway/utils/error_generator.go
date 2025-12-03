package utils

import (
	"net/http"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type GrpcHTTPError struct {
	HTTPStatus int
	GRPCCode   codes.Code
	Message    string
}

func ErrorGenerator(err error) {
	st, ok := status.FromError(err)
	if !ok {
		panic(&GrpcHTTPError{
			HTTPStatus: http.StatusInternalServerError,
			GRPCCode:   codes.Unknown,
			Message:    "Failed to reach auth service",
		})
	}

	panic(&GrpcHTTPError{
		HTTPStatus: HttpStatusFromGRPCCode(st.Code()),
		GRPCCode:   st.Code(),
		Message:    st.Message(),
	})
}
