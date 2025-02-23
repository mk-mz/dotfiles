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


function setup_billing_platform {
    script/setup-codespaces-billing-platform
    cd ../billing-platform
    code /workspaces/billing-platform/.vscode/github-billing-platform.code-workspace
}


function start_docker {
    sudo pkill dockerd && sudo pkill containerd
    /usr/local/share/docker-init.sh
}

function remove_containers {
    docker rm -f $(docker ps -aq)
}

function cosmos_query {
    script/cli --query
}


function test_emu() { TEST_WITH_ALL_EMUS=1 bin/rails test "$1" }
function test_all_features() { TEST_ALL_FEATURES=1 bin/rails test "$1" }
function seed_console() { bin/seed console }
