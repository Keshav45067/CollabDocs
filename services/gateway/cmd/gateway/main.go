package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"gateway/internal/client"
	"gateway/internal/config"
	httpHandler "gateway/internal/handler/http_handler"
	"gateway/internal/server"
)

func main() {
	cfg := config.Load()
	clients := client.ClientInitialise(cfg)

	router := httpHandler.NewRouter(cfg, clients)
	httpServer := server.NewHTTPServer(cfg, router)

	go func() {
		log.Printf("Gateway listening on %s\n", cfg.Addr)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("server error: %v", err)
		}
	}()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop

	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), cfg.GracefulShutdownTimeout)
	defer cancel()

	if err := httpServer.Shutdown(ctx); err != nil {
		log.Fatalf("forced shutdown: %v", err)
	}

	log.Println("Server exited cleanly")
}
