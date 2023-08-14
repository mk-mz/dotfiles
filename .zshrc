export ZSH="${HOME}/.oh-my-zsh"

# Theme.
ZSH_THEME="spaceship"
export SPACESHIP_DIR_TRUNC=0

# Plugins.
plugins=(git)

source $ZSH/oh-my-zsh.sh

# Set colors for LS_COLORS.
eval `dircolors ~/.dircolors`
function search_urls() { rails routes -g "$1" }

function setup_bp_dotcom {
    bin/toggle-feature-flag enable billing_vnext_pages
    script/server --debug
}

function setup_billing_platform {
    script/setup-codespaces-billing-platform
    cd ../billing-platform
    az login --use-device-code
}

function bp_run_server {
    script/set-remote
    script/server
}

function full_setup_billing_platform {
    script/setup-codespaces-billing-platform
    cd ../billing-platform
    az login --use-device-code
    script/set-remote
    script/server
}

