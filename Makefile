git:
	git submodule update --init --recursive

setup: git package.json
	npm install

PROD_OPTIONS=-e production --config config.toml,config_prod.toml --minify
DEV_OPTIONS=-e development --config config.toml,config_dev.toml
LOCAL_OPTIONS=-e development --config config.toml,config_local.toml
PR_OPTIONS=-D $(PROD_OPTIONS) --config config.toml,config_pr.toml
SERVE_OPTIONS=--baseURL http://localhost

clean:
	rm -rf public resources dist

build-prod: clean setup
	hugo $(PROD_OPTIONS)

build-dist: clean setup
	hugo $(LOCAL_OPTIONS) -d dist

htmltest: clean setup
	hugo $(LOCAL_OPTIONS) -d dist
	htmltest

markdowntest:
	markdownlint --config .markdownlint.yaml

build-pr: clean setup
	hugo $(PR_OPTIONS)

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
