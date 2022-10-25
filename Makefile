git:
	git submodule update --init --recursive

setup: git package.json
	npm install --save-dev autoprefixer
	npm install --save-dev postcss-cli

PROD_OPTIONS=-e production --minify
DEV_OPTIONS=-e development --config config.toml,config_dev.toml
SERVE_OPTIONS=--baseURL http://localhost

clean:
	rm -rf public resources

build-prod: clean setup
	hugo $(PROD_OPTIONS)

build-pr: clean setup
	hugo $(PROD_OPTIONS) --config config.toml,config_pr.toml

serve-prod: setup
	hugo server $(PROD_OPTIONS) $(SERVE_OPTIONS)

serve-prod-draft: setup
	hugo server -D $(PROD_OPTIONS) $(SERVE_OPTIONS)

serve-prod-future: setup
	hugo server -F $(PROD_OPTIONS) $(SERVE_OPTIONS)

serve-dev: setup
	hugo server $(DEV_OPTIONS) $(SERVE_OPTIONS)

serve-dev-draft: setup
	hugo server -D $(DEV_OPTIONS) $(SERVE_OPTIONS)

serve-dev-future: setup
	hugo server -F $(DEV_OPTIONS) $(SERVE_OPTIONS)
