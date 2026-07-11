#!/usr/bin/env bash
# Exit on error
set -o errexit

# Force Playwright to install in a folder that Render preserves
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/playwright

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install chromium
