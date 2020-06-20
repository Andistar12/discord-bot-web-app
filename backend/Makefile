# This Makefile is meant only for dev on the gateway

#-------------------------------------------------

# The container name that docker will use when running
CONTAINER_NAME=backend

# The image name that docker will use to build
IMAGE_NAME=backend

# The relative, in-container location of the config
CONFIG_LOC=/app/config.json

# The relative, host location of the config to copy into the container
CONFIG_LOC_EXT=../config.json

# The port on the host that should map to the container
# This is only useful if you are debugging from the host
EXPOSED_PORT=8080

# The internal port that the backend will use. Should match the config's
# This is only useful if you are debugging from the host
INTERNAL_PORT=2468

#-------------------------------------------------

.PHONY: clean build run all

# Note that this is the first target
all: clean build run

build: # Builds the docker image
	docker build -t $(IMAGE_NAME) --target dev .
	
run: # Spins up a container 
	# Supress error if not preexisting
	docker rm $(CONTAINER_NAME) || true
	docker run -it --name $(CONTAINER_NAME) --log-driver local \
		-e CONFIG_LOC=$(CONFIG_LOC) \
	    -p $(EXPOSED_PORT):$(INTERNAL_PORT) \
		-v $(realpath $(CONFIG_LOC_EXT)):$(CONFIG_LOC) \
		$(IMAGE_NAME) || true

test: clean build # Runs go tests
	# Supress error if not preexisting
	docker rm $(CONTAINER_NAME) || true
	docker run -it --name $(CONTAINER_NAME) --log-driver local \
		-e CONFIG_LOC=$(CONFIG_LOC) \
	    -p $(EXPOSED_PORT):$(INTERNAL_PORT) \
		-v $(realpath $(CONFIG_LOC_EXT)):$(CONFIG_LOC) \
		$(IMAGE_NAME) go test || true

clean: # Stops the container
	# Surpress error if not started
	docker stop $(CONTAINER_NAME) || true
