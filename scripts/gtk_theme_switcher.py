import os
import subprocess
import shutil
import json
from typing import Dict
import logging

import gi
gi.require_version('Adw', '1')
from gi.repository import Adw

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.expanduser("~/.cache/gtk_theme_switcher.log"))
    ]
)

# Paths
DATA_DIR = os.path.expanduser("~/.local/share")
CONFIG_DIR = os.path.expanduser("~/.config")

class GTKThemeManager:
    def __init__(
            self, 
            theme_name: str | None = None,
            icon_theme_name: str | None = None, 
            cursor_theme_name: str | None = None, 
            cursor_size: int | None = None,
            font_name: str | None = None,
            prefer_dark_mode: int | None = None, # 0=default, 1=prefer_dark, -1=prefer_light
        ) -> None:
        
        # Saved settings json path
        self.settings_json_path = os.path.expanduser("~/.user_settings/gtk_settings.json")
        
        # Load previous settings
        self.previous_settings = self._load_settings()
        logging.info(f"Settings loaded: {self.previous_settings}")
        
        # Set the new value if given else set from settings_json
        self.theme_name = theme_name if theme_name is not None else self.previous_settings.get("gtk_theme_name")
        self.icon_theme_name = icon_theme_name if icon_theme_name is not None else self.previous_settings.get("gtk_icon_theme_name")
        self.cursor_theme_name = cursor_theme_name if cursor_theme_name is not None else self.previous_settings.get("gtk_cursor_theme_name")
        self.cursor_size = cursor_size if cursor_size is not None else self.previous_settings.get("gtk_cursor_size")
        self.font_name = font_name if font_name is not None else self.previous_settings.get("gtk_font_name")
        self.prefer_dark_mode = prefer_dark_mode if prefer_dark_mode is not None else self.previous_settings.get("gtk_prefer_dark_mode")

        # Theme dirs
        self.theme_dirs = [
            os.path.expanduser("~/.themes"),
            os.path.expanduser("~/.local/share/themes"),
            "/usr/share/themes"
            ]
        self.icon_dirs = [
            os.path.expanduser("~/.icons"),
            os.path.expanduser("~/.local/share/icons"),
            "/usr/share/icons"
        ]
        self.cursor_dirs = self.icon_dirs

        # Initialize theme lists
        self.themes: list[str] = []
        self.icon_themes: list[str] = []
        self.cursor_themes: list[str] = []
        
        # Populate theme lists
        self._get_themes()
        self._get_icon_themes()
        self._get_cursor_themes()
        
        # GTK-4.0 config dir
        self.gtk_4_dir = os.path.join(CONFIG_DIR, "gtk-4.0")

        # Config files
        self.gtk_3_ini = os.path.join(CONFIG_DIR, "gtk-3.0", "settings.ini")
        self.gtk_4_ini = os.path.join(CONFIG_DIR, "gtk-4.0", "settings.ini")
        self.gtkrc_2_0 = os.path.expanduser("~/.gtkrc-2.0")
        self.xsettingsd_config = os.path.join(CONFIG_DIR, "xsettingsd", "xsettingsd.conf")
        self.index_dot_theme = os.path.join(DATA_DIR, "icons", "default", "index.theme")
        
        # build the contents
        self._build_config_contents()
        
    def _remove_duplicates(self, items: list[str]) -> list[str]:
        """Remove duplicates from a list"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    def _save_settings(self):
        """Create the .user_settings dir if doesn't exists and write the settings to it"""
        settings: dict[str: str] = {
            "gtk_theme_name": self.theme_name,
            "gtk_icon_theme_name": self.icon_theme_name,
            "gtk_cursor_theme_name": self.cursor_theme_name,
            "gtk_cursor_size": self.cursor_size,
            "gtk_font_name": self.font_name,
            "gtk_prefer_dark_mode": self.prefer_dark_mode
        }
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.settings_json_path), exist_ok=True)
        
        # Write the settings to the JSON file
        with open(self.settings_json_path, "w") as f:
            json.dump(settings, f, indent=4)
            
        logging.debug(f"Settings updated: {settings}")
            
    def _load_settings(self) -> Dict[str, str]:
        """Load settings from the JSON file and return them as a dictionary."""
        try:
            with open(self.settings_json_path, "r") as f:
                settings = json.load(f)
            return settings
        except FileNotFoundError:
            logging.error(f"File not found: {self.settings_json_path}")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"JSONDecodeError: {e}")
            return {}
        
    def _get_themes(self) -> None:
        """Get the available themes"""
        for theme_dir in self.theme_dirs:
            if os.path.exists(theme_dir):
                for theme in os.listdir(theme_dir):
                    if self._is_theme_dir(os.path.join(theme_dir, theme)):
                        self.themes.append(theme)
                        
        # Remove duplicates
        self.themes = self._remove_duplicates(self.themes)
        
        logging.debug(f"Found themes = {self.themes}")
        
        # If no themes are found
        if not self.themes:
            logging.error("No themes found")
            
    def _get_icon_themes(self):
        """Get the available icon themes"""
        
        # Themes to exclude
        not_themes = ["default", "hicolor"]
        
        # Scan for themes
        for icon_dir in self.icon_dirs:
            if os.path.exists(icon_dir):
                for theme in os.listdir(icon_dir):
                    theme_path = os.path.join(icon_dir, theme)
                    if os.path.isdir(theme_path) and not os.path.exists(os.path.join(theme_path, "cursors")):
                        if theme not in not_themes:
                            self.icon_themes.append(theme)
                            
        # Remove duplicates
        self.icon_themes = self._remove_duplicates(self.icon_themes)
                    
        logging.debug(f"Found icon themes = {self.icon_themes}")
        
        # If no themes are found
        if not self.icon_themes:
            logging.error("No icon themes found")

    def _get_cursor_themes(self):
        """Get the available cursor themes"""
        
        # Themes to exclude
        not_themes = ["default", "hicolor"]
        
        # Scan for themes
        for cursor_dir in self.cursor_dirs:
            if os.path.exists(cursor_dir):
                for theme in os.listdir(cursor_dir):
                    theme_path = os.path.join(cursor_dir, theme)
                    cursors_dir = os.path.join(theme_path, "cursors")
                    if os.path.isdir(theme_path) and os.path.isdir(cursors_dir):
                        if theme not in not_themes:
                            self.cursor_themes.append(theme)
                            
        # Remove duplicates
        self.cursor_themes = self._remove_duplicates(self.cursor_themes)
                                                
        logging.debug(f"Found cursor themes = {self.cursor_themes}")
                    
        # If no themes are found
        if not self.cursor_themes:
            logging.error("No cursor themes found")

    def _is_theme_dir(self, theme_path):
        """Check if a directory is a valid theme dir"""
        index_theme = os.path.join(theme_path, "index.theme")
        return os.path.isfile(index_theme)
        
    def _build_config_contents(self):
        # GTK-3.0.ini file contents
        self.gtk_3_ini_content = f"""[Settings]
gtk-theme-name={self.theme_name}
gtk-icon-theme-name={self.icon_theme_name}
gtk-font-name={self.font_name}
gtk-cursor-theme-name={self.cursor_theme_name}
gtk-cursor-theme-size={self.cursor_size}
gtk-toolbar-style=GTK_TOOLBAR_ICONS
gtk-toolbar-icon-size=GTK_ICON_SIZE_LARGE_TOOLBAR
gtk-button-images=0
gtk-menu-images=0
gtk-enable-event-sounds=1
gtk-enable-input-feedback-sounds=0
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle=hintmedium
gtk-xft-rgba=rgb
gtk-application-prefer-dark-theme={self.prefer_dark_mode}"""

        # GTK-4.0.ini file contents
        self.gtk_4_ini_content = f"""[Settings]
gtk-application-prefer-dark-theme={self.prefer_dark_mode}"""

        # .gtkrc-2.0 file content
        self.gtkrc_2_0_content = f"""gtk-theme-name={self.theme_name}
gtk-icon-theme-name={self.icon_theme_name}
gtk-font-name={self.font_name}
gtk-cursor-theme-name={self.cursor_theme_name}
gtk-cursor-theme-size={self.cursor_size}
gtk-toolbar-style=GTK_TOOLBAR_ICONS
gtk-toolbar-icon-size=GTK_ICON_SIZE_LARGE_TOOLBAR
gtk-button-images=0
gtk-menu-images=0
gtk-enable-event-sounds=1
gtk-enable-input-feedback-sounds=0
gtk-xft-antialias=1
gtk-xft-hinting=1
gtk-xft-hintstyle=\"hintmedium\"
gtk-xft-rgba=\"rgb\""""

        # xsettingsd.config file content
        self.xsettingsd_config_content = f"""Net/ThemeName \"{self.theme_name}\"
Net/IconThemeName \"{self.icon_theme_name}\"
Gtk/CursorThemeName \"{self.cursor_theme_name}\"
Net/EnableEventSounds 1
EnableInputFeedbackSounds 0
Xft/Antialias 1
Xft/Hinting 1
Xft/HintStyle \"hintmedium\"
Xft/RGBA \"rgb\""""

        # index.theme file content
        self.index_dot_theme_content = f"""[Icon Theme]
Name=Default
Comment=Default Cursor Theme
Inherits={self.cursor_theme_name}"""

    def apply_theme(self) -> None:
        # Check if given theme exists
        if not self.theme_name in self.themes:
            logging.error(f"Theme {self.theme_name} does not exist.")
            return
            
        msg = f"""Applying theme:
    GTK Theme: {self.theme_name}
    GTK Icon: {self.icon_theme_name}
    GTK Cursor: {self.cursor_theme_name}
    GTK Font: {self.font_name}
    GTK Cursor Size: {self.cursor_size}
    GTK Prefer Dark Mode: {self.prefer_dark_mode}"""
        logging.debug(msg)
        
        # Create config files
        self._write(file=self.gtkrc_2_0, content=self.gtkrc_2_0_content)
        self._write(file=self.gtk_3_ini, content=self.gtk_3_ini_content)
        self._write(file=self.gtk_4_ini, content=self.gtk_4_ini_content)
        self._write(file=self.xsettingsd_config, content=self.xsettingsd_config_content) 
        self._write(file=self.index_dot_theme, content=self.index_dot_theme_content)    
        
        # Apply GTK-4.0 theme
        self._apply_theme_gtk_4()   
            
        # Apply theme to flatpak
        self._apply_flatpak_overrides()
        
        # Reload GTK
        self._reload_gtk_settings()
        
        # Save the applied settings as backup
        self._save_settings()
            
        logging.info("Theme applied.")
    
    def _apply_theme_gtk_4(self):
        """Apply the theme to GTK-4.0"""
        
        items = ["assets", "gtk-dark.css", "gtk.css"]
        
        logging.debug("Deleting old GTK-4.0 theme")
        for item in items:
            output = subprocess.run(
                ["rm", "-r", f"{os.path.join(self.gtk_4_dir, item)}"],
                capture_output=True
            )
            logging.debug(f"Deleting {item}: {output.stderr}")
        
        # Copy the assets, gtk.css and gtk-dark.css from themes dir to gtk-4.0 dir
        for theme_dir in self.theme_dirs:
            theme_path = os.path.join(theme_dir, self.theme_name, "gtk-4.0")
            if os.path.exists(theme_path):
                try:
                    shutil.copytree(
                        src=theme_path,
                        dst=self.gtk_4_dir,
                        copy_function=shutil.copy2,
                        dirs_exist_ok=True
                    )
                    logging.info("GTK-4 theme applied.")
                    return  # Exit the loop once the theme is applied
                except Exception as e:
                    logging.error(f"While applying GTK-4.0 theme: {e}")
        
        logging.error(f"GTK-4.0 theme directory for '{self.theme_name}' not found in any of the theme directories.")
            
    def _write(self, file, content) -> None:
        """Write the content(str) to the file"""
        os.makedirs(os.path.dirname(file), exist_ok=True)
        try:
            with open(file, "w") as f:
                f.write(content)
                logging.info(f"Wrote to {file}")
                
        except Exception as e:
            logging.error(f"Error while writing to {file}:{e}")
            return

    def _apply_flatpak_overrides(self) -> None:
        """Apply the theme to flatpak apps"""
        subprocess.run(["flatpak", "override", "--user", "--filesystem=xdg-config/gtk-3.0"])
        subprocess.run(["flatpak", "override", "--user", "--filesystem=xdg-config/gtk-4.0"])
        subprocess.run(["flatpak", "override", "--user", "--filesystem=xdg-data/themes"])
        logging.info("Flatpak overrides applied")

    def _reload_gtk_settings(self) -> None:
        # Reload gsettings for GTK themes, icons, and cursors
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", f"{self.theme_name}"])
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "icon-theme", f"{self.icon_theme_name}"])
        subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", f"{self.cursor_theme_name}"])

        # Set color scheme for vanilla GTK apps using gsettings
        if self.prefer_dark_mode == 1:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", "'prefer-dark'"])
        elif self.prefer_dark_mode == 0:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", "'default'"])
        elif self.prefer_dark_mode == -1:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", "'prefer-light'"])
        else:
            logging.error("Error, use: 0 for default, 1 for prefer_dark, -1 for prefer_light")

        # Set color scheme for libadwaita apps using AdwStyleManager
        style_manager = Adw.StyleManager.get_default()
        if self.prefer_dark_mode == 1:
            style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        elif self.prefer_dark_mode == 0:
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        elif self.prefer_dark_mode == -1:
            style_manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)

        # Quit nautilus if running
        logging.debug("Quitting nautilus")
        subprocess.run(["nautilus", "-q"])

        # Reload hyprland
        logging.debug("Reload hyprland")
        subprocess.run(["hyprctl", "reload"])

        logging.info("GTK settings reloaded")

    
    def get_available_themes(self) -> list[str]:
        return self.themes
    
    def get_available_icon_themes(self) -> list[str]:
        return self.icon_themes

    def get_available_cursor_themes(self) -> list[str]:
        return self.cursor_themes


if __name__ == "__main__":
    theme_switcher = GTKThemeManager(
        theme_name="Catppuccin-Mocha",
    )
    theme_switcher.apply_theme()