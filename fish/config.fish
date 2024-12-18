
# Set prompt (optional; Fish has a nice default prompt)
function fish_prompt
    echo -n (whoami)"@"(hostname)" " (basename (pwd)) "> "
end

# Add fzf to PATH (if installed)
set -U fish_user_paths /usr/bin/fzf $fish_user_paths

# Alias examples
alias ll="ls -lh"
alias update="sudo pacman -Syu"

set -g fish_greeting
neofetch
atuin init fish | source

# List Directory
alias l='eza -lh  --icons=auto' # long list
alias ls='eza -1   --icons=auto' # short list
alias ll='eza -lha --icons=auto --sort=name --group-directories-first' # long list all
alias ld='eza -lhD --icons=auto' # long list dirs
alias lt='eza --icons=auto --tree' # list folder as tree

# Sets starship as the promt
eval (starship init fish)
set -Ux GTK_CURSOR_THEME Bibata-Modern-Classic
set -Ux XCURSOR_THEME Bibata-Modern-Classic
set -Ux XCURSOR_SIZE 20
set -x QT_QPA_PLATFORMTHEME qt5ct
set -x QT_STYLE_OVERRIDE kvantum
set -x QT_QPA_PLATFORM wayland
