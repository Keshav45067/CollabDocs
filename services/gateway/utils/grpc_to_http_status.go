package utils

import (
	"net/http"

	"google.golang.org/grpc/codes"
)

func HttpStatusFromGRPCCode(code codes.Code) int {
	switch code {
	case codes.OK:
		return http.StatusOK

	case codes.InvalidArgument,
		codes.FailedPrecondition,
		codes.OutOfRange:
		return http.StatusBadRequest

	case codes.Unauthenticated:
		return http.StatusUnauthorized

	case codes.PermissionDenied:
		return http.StatusForbidden

	case codes.NotFound:
		return http.StatusNotFound

	case codes.AlreadyExists,
		codes.Aborted:
		return http.StatusConflict

	case codes.ResourceExhausted:
		return http.StatusTooManyRequests

	case codes.Canceled:
		return http.StatusRequestTimeout

	case codes.DeadlineExceeded:
		return http.StatusGatewayTimeout

	case codes.Unimplemented:
		return http.StatusNotImplemented

	case codes.Unavailable:
		return http.StatusServiceUnavailable

	case codes.DataLoss,
		codes.Unknown,
		codes.Internal:
		fallthrough
	default:
		return http.StatusInternalServerError
	}
}
