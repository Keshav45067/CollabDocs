PROTO_DIR := ../../proto

# Output folder inside this service
PY_OUT := proto

# Proto dependencies for this service
PROTO_FILES := \
	$(PROTO_DIR)/common/v1/common.proto \
	$(PROTO_DIR)/auth/v1/auth.proto

PYTHON := python3

.PHONY: protos clean init-packages

protos: init-packages
	$(PYTHON) -m grpc_tools.protoc \
		-I $(PROTO_DIR) \
		--python_out=$(PY_OUT) \
		--grpc_python_out=$(PY_OUT) \
		--pyi_out=$(PY_OUT) \
		$(PROTO_FILES)

# Ensure proper Python import structure
init-packages:
	@mkdir -p $(PY_OUT)/auth/v1
	@mkdir -p $(PY_OUT)/common/v1
	@touch $(PY_OUT)/__init__.py
	@touch $(PY_OUT)/auth/__init__.py
	@touch $(PY_OUT)/auth/v1/__init__.py
	@touch $(PY_OUT)/common/__init__.py
	@touch $(PY_OUT)/common/v1/__init__.py

clean:
	@rm -rf $(PY_OUT)