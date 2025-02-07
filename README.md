# Hyprland Configuration

This repository contains my personal Hyprland window manager configuration files, including themes and complementary tools settings.

## 📸 Screenshots

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)
![Screenshot 3](screenshots/screenshot3.png)

## 🛠️ Installation

1. Clone this repository:

- `git clone https://github.com/Saifullah-Balghari/Hyprland-Dotfiles.git`

2. Copy the config files to your config directory:

- `cp -r Hyprland-Dotfiles/ ~/.config/`

3. Start hyprland(if on tty) or Restart Hyprland:

- `hyprland`

4. Enjoy!

## 📦 Dependencies

Required packages:

- Hyprland (window manager)
- Waybar (status bar)
- SwayNC (notification daemon)
- JetBrainsMono Nerd Font (or your preferred font)
- playerctl (media controls)
- brightnessctl (brightness control)
- NetworkManager
- pamixer (volume control)

## 🐛 Troubleshooting

Common issues and solutions:

1. Waybar not appearing:

   - Check if Waybar is running
   - Verify config syntax
   - Check system logs

2. Notifications not showing:
   - Ensure SwayNC service is running
   - Check notification permissions
   - Verify D-Bus configuration

## 📝 License

This configuration is released under the MIT License. See `LICENSE` for more details.

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Share improvements

---
