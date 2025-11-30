package client

import (
	"crypto/tls"
	authv1 "gateway/proto/auth/v1"

	"gateway/internal/config"
	"gateway/utils"
)

func AuthConnection(authAddr string, config *config.Config, tls *tls.Config) authv1.AuthServiceClient {
	authConn := utils.GRPCConnector(authAddr, config, tls)
	authClient := authv1.NewAuthServiceClient(authConn)
	return authClient
}

// package server

// import (
// 	"time"

// 	authv1 "gateway/proto/auth/v1"
// 	crdtv1 "gateway/proto/crdt/v1"

// 	"google.golang.org/grpc"
// 	"google.golang.org/grpc/credentials/insecure"
// 	"google.golang.org/grpc/keepalive"
// )

// type GRPCClients struct {
// 	Auth authv1.AuthServiceClient
// 	Crdt crdtv1.CrdtServiceClient

// 	authConn *grpc.ClientConn
// 	crdtConn *grpc.ClientConn
// }

// // NewGRPCClients dials both microservices and returns typed gRPC clients.
// func NewGRPCClients(authAddr, crdtAddr string) (*GRPCClients, error) {
// 	authConn, err := grpc.Dial(
// 		authAddr,
// 		grpc.WithTransportCredentials(insecure.NewCredentials()), // dev only
// 		grpc.WithKeepaliveParams(keepalive.ClientParameters{
// 			Time:                30 * time.Second,
// 			Timeout:             10 * time.Second,
// 			PermitWithoutStream: true,
// 		}),
// 	)
// 	if err != nil {
// 		return nil, err
// 	}

// 	crdtConn, err := grpc.Dial(
// 		crdtAddr,
// 		grpc.WithTransportCredentials(insecure.NewCredentials()), // dev only
// 		grpc.WithKeepaliveParams(keepalive.ClientParameters{
// 			Time:                30 * time.Second,
// 			Timeout:             10 * time.Second,
// 			PermitWithoutStream: true,
// 		}),
// 	)
// 	if err != nil {
// 		authConn.Close()
// 		return nil, err
// 	}

// 	return &GRPCClients{
// 		Auth:     authv1.NewAuthServiceClient(authConn),
// 		Crdt:     crdtv1.NewCrdtServiceClient(crdtConn),
// 		authConn: authConn,
// 		crdtConn: crdtConn,
// 	}, nil
// }

// // Close closes all underlying gRPC connections.
// func (c *GRPCClients) Close() error {
// 	var err error
// 	if c.authConn != nil {
// 		if e := c.authConn.Close(); e != nil {
// 			err = e
// 		}
// 	}
// 	if c.crdtConn != nil {
// 		if e := c.crdtConn.Close(); e != nil {
// 			err = e
// 		}
// 	}
// 	return err
// }
