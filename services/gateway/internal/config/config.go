package config

import (
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/joho/godotenv"
)

type Config struct {
	Addr                    string
	AllowedOrigins          []string
	MaxBodyBytes            int64
	RequestTimeout          time.Duration
	GracefulShutdownTimeout time.Duration
	RateLimitRPS            float64
	RateLimitBurst          int
	IsProduction            bool
}

func Load() *Config {
	loadENV()
	return &Config{
		Addr:                    getEnv("ADDR", ":8080"),
		AllowedOrigins:          splitAndTrim(getEnv("ALLOWED_ORIGINS", "http://localhost:3000")),
		MaxBodyBytes:            mustInt64Env("MAX_BODY_BYTES"),               // 1<<20 (1MB)
		GracefulShutdownTimeout: mustDurationEnv("GRACEFUL_SHUTDOWN_TIMEOUT"), // 10*time.Second
		RateLimitRPS:            mustFloatEnv("RATE_LIMIT_RPS"),               //10.0
		RateLimitBurst:          mustIntEnv("RATE_LIMIT_BURST"),               //20
		RequestTimeout:          mustDurationEnv("REQUEST_TIMEOUT"),
		IsProduction:            mustBool("IS_PRODUCTION"),
	}
}

func loadENV() {
	if err := godotenv.Load(); err != nil {
		log.Panicf("Failed to load environmental variables: %v", err)
	}
}

func getEnv(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func splitAndTrim(s string) []string {
	parts := strings.Split(s, ",")
	var out []string
	for _, p := range parts {
		if t := strings.TrimSpace(p); t != "" {
			out = append(out, t)
		}
	}
	return out
}

func mustIntEnv(key string) int {
	v := getEnv(key, "")
	if v == "" {
		log.Panicf("Environment Variable '%v' not provided ", key)
	}
	n, err := strconv.Atoi(v)
	if err != nil {
		log.Fatalf("invalid %s: %v", key, err)
	}
	return n
}

func mustInt64Env(key string) int64 {
	v := getEnv(key, "")
	if v == "" {
		log.Panicf("Environment Variable '%v' not provided ", key)
	}
	n, err := strconv.ParseInt(v, 10, 64)
	if err != nil {
		log.Fatalf("invalid %s: %v", key, err)
	}
	return n
}

func mustFloatEnv(key string) float64 {
	v := getEnv(key, "")
	if v == "" {
		log.Panicf("Environment Variable '%v' not provided ", key)
	}
	n, err := strconv.ParseFloat(v, 64)
	if err != nil {
		log.Fatalf("invalid %s: %v", key, err)
	}
	return n
}

func mustDurationEnv(key string) time.Duration {
	v := getEnv(key, "")
	if v == "" {
		log.Panicf("Environment Variable '%v' not provided ", key)
	}
	d, err := time.ParseDuration(v)
	if err != nil {
		log.Fatalf("invalid %s: %v", key, err)
	}
	return d
}

func mustBool(key string) bool {
	v := getEnv(key, "")
	if v == "" {
		log.Panicf("Environment Variable '%v' not provided ", key)
	}
	if v == "true" {
		return true
	}
	return false
}
