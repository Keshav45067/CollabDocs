PROTO_DIR := ../../proto

# Output folder inside this service
PY_OUT := proto

# Proto dependencies for this service
PROTO_FILES := \
	$(PROTO_DIR)/common/v1/common.proto \
	$(PROTO_DIR)/auth/v1/auth.proto

PYTHON := python

PROTO_VERSION := 1

.PHONY: protos clean init-packages

create-protos: init-packages
	$(PYTHON) -m grpc_tools.protoc \
		-I $(PROTO_DIR) \
		--python_out=$(PY_OUT) \
		--grpc_python_out=$(PY_OUT) \
		--pyi_out=$(PY_OUT) \
		$(PROTO_FILES)

protos: create-protos
	@echo "Fixing imports in generated files..."
	@find $(PY_OUT) -type f -name "*_pb2*.py" -exec sed -i.bak \
		-E 's/^from ([a-zA-Z_][a-zA-Z0-9_]*)\.v([0-9]+) import/from proto.\1.v\2 import/g' {} \;
	@find $(PY_OUT) -type f -name "*.bak" -delete

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