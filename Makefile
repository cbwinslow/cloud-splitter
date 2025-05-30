.PHONY: setup test format build clean

setup:
	./scripts/setup_dev.sh

test:
	./scripts/run_tests.sh

format:
	./scripts/format_code.sh

build:
	./scripts/build_package.sh

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
