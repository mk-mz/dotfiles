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

function npm_test_watch {
    bin/npm run test:watch -w @github-ui/billing-app
}

function test_emu() { TEST_WITH_ALL_EMUS=1 bin/rails test "$1" }
function test_all_features() { TEST_ALL_FEATURES=1 bin/rails test "$1" }
function seed_console() { bin/seed console }

function dc_down {
    script/dc down
}

function sync_github {
    bin/dev-sync-github-inc-billing-platform
}

function gh_ui {
    script/server --ui --debug
}

function open_github_ui {
    script/open-with-github-ui
}

# Wraps a command and auto-opens any Tailscale auth URLs in the browser
function tailscale_auto_open {
    "$@" 2>&1 | while IFS= read -r line; do
        echo "$line"
        url=$(echo "$line" | grep -oE 'https://login\.tailscale\.com/[^ ]+')
        if [[ -n "$url" ]]; then
            echo "Opening auth URL in browser..."
            code --open-url "$url" 2>/dev/null || xdg-open "$url" 2>/dev/null || open "$url" 2>/dev/null
        fi
    done
}

function ts_up {
    tailscale_auto_open sudo tailscale up "$@"
}

function ts_make {
    tailscale_auto_open make tailscale "$@"
}
