SOURCES := $(shell find src static *.cjs *.js *.json)

.PHONY: build
deploy: build/index.html
	rsync -azvh --delete --progress build/ root@assets.molyneaux.ca:/var/www/html

build/index.html: $(SOURCES)
	npx svelte-kit build
