# Dockerfile for beads (bd) tool
FROM golang:1.23-alpine AS builder

# Install git and build dependencies (needed for go modules and CGO)
RUN apk add --no-cache git gcc musl-dev

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build the binary (CGO enabled for SQLite)
RUN CGO_ENABLED=1 go build -o bd ./cmd/bd

# Final stage
FROM alpine:latest

# Install ca-certificates and libc for CGO binaries
RUN apk --no-cache add ca-certificates libc6-compat

# Create a non-root user
RUN adduser -D -s /bin/sh beads

# Copy the binary
COPY --from=builder /app/bd /usr/local/bin/bd

# Switch to non-root user
USER beads

# Set the entrypoint
ENTRYPOINT ["bd"]
