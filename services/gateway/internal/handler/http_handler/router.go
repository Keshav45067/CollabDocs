package httpHandler

import (
	"net/http"
	"time"

	"gateway/internal/client"
	"gateway/internal/config"
	"gateway/internal/middleware"

	"github.com/gin-gonic/gin"
)

func NewRouter(cnfg *config.Config, clients *client.Clients) *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	r.Use(gin.Recovery())
	r.Use(
		middleware.CORS(cnfg.AllowedOrigins),
		middleware.BodyLimit(cnfg.MaxBodyBytes),
		middleware.SecurityHeaders(),
		middleware.SetRequestId(),
		middleware.Timeout(cnfg.RequestTimeout),
	)

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "Healthy",
			"time":   time.Now().UTC(),
		})
	})
	auth := r.Group("/auth")
	AuthHTTPRouter(auth, clients)

	return r
}
