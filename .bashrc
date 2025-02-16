#
# ~/.bashrc
#

[[ $- != *i* ]] && return

# Start fastfetch
fastfetch

# Start Starship prompt
eval "$(starship init bash)"

# Start Atuin
eval "$(atuin init bash)"

# List Directory aliases using eza
alias l='eza -lh  --icons=auto' # long list
alias ls='eza -1   --icons=auto' # short list
alias ll='eza -lha --icons=auto --sort=name --group-directories-first' # long list all
alias ld='eza -lhD --icons=auto' # long list dirs
alias lt='eza --icons=auto --tree' # list folder as tree

# Environment Variables
export GTK_CURSOR_THEME=Bibata-Modern-Classic
export XCURSOR_THEME=Bibata-Modern-Classic
export XCURSOR_SIZE=20
export QT_QPA_PLATFORMTHEME=qt6ct
export QT_QPA_PLATFORM=wayland
export QT_STYLE_OVERRIDE=kvantum
