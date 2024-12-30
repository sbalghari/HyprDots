# Fish Configuration
# by Saifullah Balghari 
# -----------------------------------------------------

# Remove the fish greetings
set -g fish_greeting

# Start neofetch
neofetch

# Start atuin
atuin init fish | source

# List Directory
alias l='eza -lh  --icons=auto' # long list
alias ls='eza -1   --icons=auto' # short list
alias ll='eza -lha --icons=auto --sort=name --group-directories-first' # long list all
alias ld='eza -lhD --icons=auto' # long list dirs
alias lt='eza --icons=auto --tree' # list folder as tree

# Sets starship as the promt
eval (starship init fish)

# Variables
set -Ux GTK_CURSOR_THEME Bibata-Modern-Classic
set -Ux XCURSOR_THEME Bibata-Modern-Classicz
set -Ux XCURSOR_SIZE 20
set -x QT_QPA_PLATFORMTHEME qt5ct
set -x QT_QPA_PLATFORMTHEME qt6ct
set -x QT_QPA_PLATFORM wayland
