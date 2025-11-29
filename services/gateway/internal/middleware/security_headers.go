package middleware

import "github.com/gin-gonic/gin"

func SecurityHeaders() gin.HandlerFunc {
	return func(c *gin.Context) {
		h := c.Writer.Header()

		h.Set("X-Frame-Options", "DENY")
		h.Set("X-Content-Type-Options", "nosniff")
		h.Set("X-XSS-Protection", "1; mode=block")
		h.Set("Referrer-Policy", "strict-origin-when-cross-origin")
		h.Set("X-Download-Options", "noopen")
		h.Set("X-Permitted-Cross-Domain-Policies", "none")

		// h.Set("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")

		// h.Set("Content-Security-Policy",
		// 	"default-src 'self'; "+
		// 		"script-src 'self' 'unsafe-inline' 'unsafe-eval'; "+
		// 		"style-src 'self' 'unsafe-inline'; "+
		// 		"img-src 'self' data:; "+
		// 		"font-src 'self' data:; "+
		// 		"connect-src 'self'; "+
		// 		"frame-ancestors 'none'; "+
		// 		"base-uri 'self'; "+
		// 		"form-action 'self';",
		// )

		c.Next()
	}
}
