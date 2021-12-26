help:
	@echo "install - Install frontend dependencies"
	@echo "frontend - Build frontend"
	@echo "dev_server - Start dev server for frontend development"

install:
	# Install npm for theme
	cd omap/theme/static_src && npm install

frontend:
	cd omap/theme/static_src && npm run build

dev_server:
	cd omap/theme/static_src && npm run start
