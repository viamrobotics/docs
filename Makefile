git:
	git submodule update --init --recursive

setup: git package.json
	npm install

setupnpm:
	npm install

PROD_OPTIONS=-e production --config config.toml,config_prod.toml --minify
DEV_OPTIONS=-e development --config config.toml,config_dev.toml
LOCAL_OPTIONS=-e development --config config.toml,config_local.toml
PR_OPTIONS=-D $(PROD_OPTIONS) --config config.toml,config_pr.toml
SERVE_OPTIONS=--baseURL http://localhost

clean:
	rm -rf public resources dist

purge:
	npm cache clean --force && hugo mod clean --all && rm -rf public resources dist node_modules themes/docsy/* themes/docsy/.[a-zA-Z0-9]* .hugo_build.lock

build-prod: clean setup
	hugo $(PROD_OPTIONS)

build-dist: clean setup
	hugo $(LOCAL_OPTIONS) -d dist

build-dist-pr: setupnpm
	hugo $(LOCAL_OPTIONS) -d dist

htmltest: clean setup
	hugo $(LOCAL_OPTIONS) -d dist
	htmltest

htmltest-fast: setup
	hugo $(LOCAL_OPTIONS) -d dist
	htmltest

coveragetest:
	python3 .github/workflows/update_sdk_methods.py --coverage -vv

markdowntest:
	markdownlint --config .markdownlint.yaml

flake8test:
	flake8-markdown docs/**/*.md

build-pr: clean setup
	hugo $(PR_OPTIONS)

build-pr-no-clean: setupnpm
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

prettierfix: setup
	./node_modules/prettier/bin/prettier.cjs --check docs/**/*.md --fix --write

test-code-snippets: test-python-snippets test-go-snippets test-typescript-snippets

test-python-snippets:
	rm -rf static/include/examples/**/.DS_Store
	bluehawk snip -o static/include/examples-generated/ static/include/examples/
	@echo "Starting to test Python code samples..."
	@echo "========================================"
	@total_files=0; \
	passed_files=0; \
	failed_files=0; \
	failed_file_list=""; \
	for file in static/include/examples/**/*.py; do \
		if [ -f "$$file" ]; then \
			echo "Testing: $$file"; \
			total_files=$$((total_files + 1)); \
			if VIAM_API_KEY="$$VIAM_API_KEY" VIAM_API_KEY_ID="$$VIAM_API_KEY_ID" TEST_ORG_ID="$$TEST_ORG_ID" VIAM_API_KEY_DATA_REGIONS="$$VIAM_API_KEY_DATA_REGIONS" VIAM_API_KEY_ID_DATA_REGIONS="$$VIAM_API_KEY_ID_DATA_REGIONS" python "$$file"; then \
				passed_files=$$((passed_files + 1)); \
				echo "✅ PASSED: $$file"; \
			else \
				failed_files=$$((failed_files + 1)); \
				echo "❌ FAILED: $$file"; \
				if [ -z "$$failed_file_list" ]; then \
					failed_file_list="$$file"; \
				else \
					failed_file_list="$$failed_file_list $$file"; \
				fi; \
			fi; \
			echo "----------------------------------------"; \
		fi; \
	done; \
	echo "========================================"; \
	echo "TEST SUMMARY:"; \
	echo "Total files tested: $$total_files"; \
	echo "Passed: $$passed_files"; \
	echo "Failed: $$failed_files"; \
	echo "Skipped: $$((total_files - passed_files - failed_files))"; \
	if [ $$failed_files -gt 0 ]; then \
		echo "Failed files:"; \
		for failed_file in $$failed_file_list; do \
			echo "  - $$failed_file"; \
		done; \
	fi

test-go-snippets:
	rm -rf static/include/examples/**/.DS_Store
	bluehawk snip -o static/include/examples-generated/ static/include/examples/
	@echo "Starting to test Go code samples..."
	@echo "========================================"
	@total_files=0; \
	passed_files=0; \
	failed_files=0; \
	failed_file_list=""; \
	for file in static/include/examples/**/*.go; do \
		if [ -f "$$file" ]; then \
			echo "Testing: $$file"; \
			total_files=$$((total_files + 1)); \
			file_dir=$$(dirname "$$file"); \
			if (cd "$$file_dir" && VIAM_API_KEY="$$VIAM_API_KEY" VIAM_API_KEY_ID="$$VIAM_API_KEY_ID" TEST_ORG_ID="$$TEST_ORG_ID" VIAM_API_KEY_DATA_REGIONS="$$VIAM_API_KEY_DATA_REGIONS" VIAM_API_KEY_ID_DATA_REGIONS="$$VIAM_API_KEY_ID_DATA_REGIONS" go run "$$(basename "$$file")"); then \
				passed_files=$$((passed_files + 1)); \
				echo "✅ PASSED: $$file"; \
			else \
				failed_files=$$((failed_files + 1)); \
				echo "❌ FAILED: $$file"; \
				if [ -z "$$failed_file_list" ]; then \
					failed_file_list="$$file"; \
				else \
					failed_file_list="$$failed_file_list $$file"; \
				fi; \
			fi; \
			echo "----------------------------------------"; \
		fi; \
	done; \
	echo "========================================"; \
	echo "TEST SUMMARY:"; \
	echo "Total files tested: $$total_files"; \
	echo "Passed: $$passed_files"; \
	echo "Failed: $$failed_files"; \
	echo "Skipped: $$((total_files - passed_files - failed_files))"; \
	if [ $$failed_files -gt 0 ]; then \
		echo "Failed files:"; \
		for failed_file in $$failed_file_list; do \
			echo "  - $$failed_file"; \
		done; \
	fi

test-typescript-snippets:
	rm -rf static/include/examples/**/.DS_Store
	bluehawk snip -o static/include/examples-generated/ static/include/examples/
	@echo "Starting to test TypeScript code samples..."
	@echo "========================================"
	@total_files=0; \
	passed_files=0; \
	failed_files=0; \
	failed_file_list=""; \
	for file in static/include/examples/**/*.ts; do \
		if [ -f "$$file" ]; then \
			echo "Testing: $$file"; \
			total_files=$$((total_files + 1)); \
			if VIAM_API_KEY="$$VIAM_API_KEY" VIAM_API_KEY_ID="$$VIAM_API_KEY_ID" TEST_ORG_ID="$$TEST_ORG_ID" VIAM_API_KEY_DATA_REGIONS="$$VIAM_API_KEY_DATA_REGIONS" VIAM_API_KEY_ID_DATA_REGIONS="$$VIAM_API_KEY_ID_DATA_REGIONS" node "$$file"; then \
				passed_files=$$((passed_files + 1)); \
				echo "✅ PASSED: $$file"; \
			else \
				failed_files=$$((failed_files + 1)); \
				echo "❌ FAILED: $$file"; \
				if [ -z "$$failed_file_list" ]; then \
					failed_file_list="$$file"; \
				else \
					failed_file_list="$$failed_file_list $$file"; \
				fi; \
			fi; \
			echo "----------------------------------------"; \
		fi; \
	done; \
	echo "========================================"; \
	echo "TEST SUMMARY:"; \
	echo "Total files tested: $$total_files"; \
	echo "Passed: $$passed_files"; \
	echo "Failed: $$failed_files"; \
	echo "Skipped: $$((total_files - passed_files - failed_files))"; \
	if [ $$failed_files -gt 0 ]; then \
		echo "Failed files:"; \
		for failed_file in $$failed_file_list; do \
			echo "  - $$failed_file"; \
		done; \
	fi