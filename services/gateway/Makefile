PROTO_DIR := ../../proto

# Where generated Go code will be written
GO_OUT := proto

# Which proto files this service depends on
PROTO_FILES := \
	$(PROTO_DIR)/common/v1/common.proto \
	$(PROTO_DIR)/auth/v1/auth.proto

.PHONY: protos clean

protos:
	@mkdir -p $(GO_OUT)
	protoc \
		-I $(PROTO_DIR) \
		--go_out=$(GO_OUT) \
		--go_opt=paths=source_relative \
		--go-grpc_out=$(GO_OUT) \
		--go-grpc_opt=paths=source_relative \
		$(PROTO_FILES)

clean:
	rm -rf $(GO_OUT)