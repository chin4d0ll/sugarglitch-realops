#!/bin/bash
# SugarGlitch RealOps - Dotfiles Installation Script
# This script installs and configures dotfiles for the development environment

set -e

DOTFILES_DIR="/workspaces/sugarglitch-realops/.devcontainer/dotfiles"
HOME_DIR="$HOME"

echo "🔧 Installing SugarGlitch RealOps dotfiles..."

# Function to backup existing files with timestamp
backup_file() {
    if [ -f "$1" ]; then
        local timestamp=$(date +%s)
        local backup_name="$1.backup.$timestamp"
        echo "  📋 Backing up existing $1 to $backup_name"
        cp "$1" "$backup_name"
        echo "  💾 Backup saved: $backup_name"
    fi
}

# Function to create symlink
create_symlink() {
    local source="$1"
    local target="$2"
    
    if [ -f "$source" ]; then
        backup_file "$target"
        echo "  🔗 Linking $source -> $target"
        ln -sf "$source" "$target"
    else
        echo "  ⚠️ Source file $source not found"
    fi
}

# Install dotfiles
echo "📁 Installing dotfiles..."

# Bash configuration
create_symlink "$DOTFILES_DIR/.bashrc" "$HOME_DIR/.bashrc"

# Zsh configuration  
create_symlink "$DOTFILES_DIR/.zshrc" "$HOME_DIR/.zshrc"

# Git configuration
create_symlink "$DOTFILES_DIR/.gitconfig" "$HOME_DIR/.gitconfig"

# Reload shell configuration
echo "🔄 Reloading shell configuration..."
if [ -n "$BASH_VERSION" ]; then
    source "$HOME_DIR/.bashrc" 2>/dev/null || true
elif [ -n "$ZSH_VERSION" ]; then
    source "$HOME_DIR/.zshrc" 2>/dev/null || true
fi

echo "✅ Dotfiles installation complete!"
echo ""
echo "🎉 Your development environment is now configured with:"
echo "  • Enhanced bash/zsh with useful aliases"
echo "  • Git configuration optimized for development"
echo "  • Security tool shortcuts and functions"
echo "  • Project-specific environment variables"
echo ""
echo "🔄 Please restart your terminal or run 'source ~/.bashrc' to apply changes"
