#!/bin/bash


create_symlinks() {
    # Get the directory in which this script lives.
    script_dir=$(dirname "$(readlink -f "$0")")

    # Get a list of all files in this directory that start with a dot.
    files=$(find -maxdepth 1 -type f -name ".*")

    # Create a symbolic link to each file in the home directory.
    for file in $files; do
        name=$(basename $file)
        echo "Creating symlink to $name in home directory."
        rm -rf ~/$name
        ln -s $script_dir/$name ~/$name
    done
}

create_symlinks

install_copilot_skills() {
    script_dir=$(dirname "$(readlink -f "$0")")
    skills_src="$script_dir/.copilot-skills"

    if [ -d "$skills_src" ]; then
        mkdir -p "$HOME/.copilot/skills"
        for skill in "$skills_src"/*/; do
            skill_name=$(basename "$skill")
            echo "Installing Copilot skill: $skill_name"
            rm -rf "$HOME/.copilot/skills/$skill_name"
            cp -r "$skill" "$HOME/.copilot/skills/$skill_name"
        done
        echo "✅ Copilot skills installed to ~/.copilot/skills/"
    fi
}

install_copilot_skills

echo "Setting up the Spaceship theme."

echo "Installing Powerline"
sudo apt-get install powerline fonts-powerline -y
echo "Installing Powerline"
ZSH_CUSTOM="$HOME/.oh-my-zsh/custom"
echo "Cloning"
git clone https://github.com/spaceship-prompt/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1
echo "Symlink spaceship.zsh-theme"
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"
ln -sf "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"
