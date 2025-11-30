package client

import (
	"gateway/internal/config"
	authv1 "gateway/proto/auth/v1"
)

type Clients struct {
	AuthClient authv1.AuthServiceClient
}

func ClientInitialise(cnfg *config.Config) *Clients {
	return &Clients{
		AuthClient: AuthConnection("[::]:50051", cnfg, nil),
	}
}
