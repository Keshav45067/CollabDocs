package middleware

import (
	"context"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func Timeout(timeout time.Duration) gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(c.Request.Context(), timeout)
		defer cancel()

		c.Request = c.Request.WithContext(ctx)

		done := make(chan struct{})
		panicChan := make(chan any)

		go func() {
			defer func() {
				if p := recover(); p != nil {
					panicChan <- p
				}
				close(done)
			}()
			c.Next()
		}()

		select {
		case <-ctx.Done():
			c.AbortWithStatus(http.StatusGatewayTimeout)
		case p := <-panicChan:
			panic(p)
		case <-done:
			return
		}
	}
}
