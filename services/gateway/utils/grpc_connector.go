package utils

import (
	"crypto/tls"
	"gateway/internal/config"
	"log"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/credentials/insecure"
)

func GRPCConnector(serviceAddr string, config *config.Config, tls *tls.Config) *grpc.ClientConn {
	var creds credentials.TransportCredentials

	if config.IsProduction {
		if tls == nil {
			panic("TLS config is required for Production")
		}
		creds = credentials.NewTLS(tls)
	} else {
		creds = insecure.NewCredentials()
	}

	var opt []grpc.DialOption = []grpc.DialOption{
		grpc.WithTransportCredentials(creds),
		// grpc.WithKeepaliveParams(keepalive.ClientParameters{
		// 	Time:                30 * time.Second,
		// 	Timeout:             10 * time.Second,
		// 	PermitWithoutStream: true,
		// }),
	}

	conn, err := grpc.NewClient(serviceAddr, opt...)
	if err != nil {
		log.Panicf("Failed to establish gRPC client for service with address %v", serviceAddr)
	}
	return conn
}
