from textual.widgets import Static, Input, Switch, Select, Button, RadioSet, RadioButton
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.reactive import reactive
from typing import Dict, Any
from pathlib import Path
import tomli
import tomli_w
from cloud_splitter.utils.validation import Validator
from cloud_splitter.exceptions import ConfigurationError

class ConfigView(Container):
    """Configuration management view"""
    
    config: reactive[Dict[str, Any]] = reactive({})
    
    def compose(self):
        with Vertical():
            yield Static("Configuration Settings", id="config-title")
            
            # Paths Section
            with Container(id="paths-section"):
                yield Static("Output Directories")
                yield Input(placeholder="Download Directory", id="download-dir")
                yield Input(placeholder="Output Directory", id="output-dir")
            
            # Download Options
            with Container(id="download-section"):
                yield Static("Download Settings")
                yield Switch("Keep Original Files", id="keep-original", value=True)
                yield Select(
                    [
                        ("Best Audio/Video Quality", "bestaudio/best"),
                        ("Best Audio Only", "bestaudio"),
                        ("Compressed Audio", "worstaudio")
                    ],
                    id="format-select",
                    value="bestaudio/best"
                )
            
            # Processing Options
            with Container(id="processing-section"):
                yield Static("Stem Separation")
                with RadioSet(id="separator-select"):
                    yield RadioButton("Demucs", value=True)
                    yield RadioButton("Spleeter")
                
                yield Static("Stem Types")
                with Grid(id="stem-grid"):
                    yield Switch("Vocals", id="stem-vocals", value=True)
                    yield Switch("Drums", id="stem-drums", value=True)
                    yield Switch("Bass", id="stem-bass", value=True)
                    yield Switch("Other", id="stem-other", value=True)
            
            # Advanced Options
            with Container(id="advanced-section"):
                yield Static("Advanced Settings")
                yield Switch("CPU Only", id="cpu-only", value=False)
                yield Select(
                    [("2", "2"), ("4", "4"), ("6", "6")],
                    id="shifts-select",
                    value="2"
                )
            
            # Actions
            with Horizontal():
                yield Button("Save", id="save-btn", variant="primary")
                yield Button("Reset to Defaults", id="reset-btn", variant="warning")

    def on_mount(self) -> None:
        self.load_config()

    def load_config(self) -> None:
        try:
            config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
            if config_path.exists():
                with open(config_path, "rb") as f:
                    self.config = tomli.load(f)
                self._update_form_values()
            else:
                self.notify("Using default configuration", severity="information")
        except Exception as e:
            self.notify(f"Error loading configuration: {str(e)}", severity="error")

    def _update_form_values(self) -> None:
        # Update form fields based on loaded config
        if "paths" in self.config:
            self.query_one("#download-dir", Input).value = str(self.config["paths"].get("download_dir", ""))
            self.query_one("#output-dir", Input).value = str(self.config["paths"].get("output_dir", ""))
        
        if "download" in self.config:
            self.query_one("#keep-original", Switch).value = self.config["download"].get("keep_original", True)
            self.query_one("#format-select", Select).value = self.config["download"].get("format", "bestaudio/best")
        
        if "processing" in self.config:
            separator = self.config["processing"].get("separator", "demucs")
            self.query_one("#separator-select", RadioSet).press(0 if separator == "demucs" else 1)
            
            stems = self.config["processing"].get("stems", [])
            for stem in ["vocals", "drums", "bass", "other"]:
                self.query_one(f"#stem-{stem}", Switch).value = stem in stems
        
        if "demucs" in self.config:
            self.query_one("#cpu-only", Switch).value = self.config["demucs"].get("cpu_only", False)
            self.query_one("#shifts-select", Select).value = str(self.config["demucs"].get("shifts", "2"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-btn":
            self.save_config()
        elif event.button.id == "reset-btn":
            self.reset_config()

    def save_config(self) -> None:
        try:
            config = self._collect_form_values()
            if errors := Validator.validate_config(config):
                self.notify("\n".join(errors), severity="error")
                return
            
            config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, "wb") as f:
                tomli_w.dump(config, f)
            
            self.notify("Configuration saved successfully", severity="success")
        except Exception as e:
            self.notify(f"Error saving configuration: {str(e)}", severity="error")

    def _collect_form_values(self) -> Dict[str, Any]:
        config = {
            "paths": {
                "download_dir": self.query_one("#download-dir", Input).value,
                "output_dir": self.query_one("#output-dir", Input).value
            },
            "download": {
                "keep_original": self.query_one("#keep-original", Switch).value,
                "format": self.query_one("#format-select", Select).value
            },
            "processing": {
                "separator": "demucs" if self.query_one("#separator-select", RadioSet).pressed_index == 0 else "spleeter",
                "stems": [
                    stem for stem in ["vocals", "drums", "bass", "other"]
                    if self.query_one(f"#stem-{stem}", Switch).value
                ]
            },
            "demucs": {
                "cpu_only": self.query_one("#cpu-only", Switch).value,
                "shifts": int(self.query_one("#shifts-select", Select).value)
            }
        }
        return config

    def reset_config(self) -> None:
        try:
            config_path = Path(__file__).parent.parent.parent / "config" / "default.toml"
            with open(config_path, "rb") as f:
                self.config = tomli.load(f)
            self._update_form_values()
            self.notify("Configuration reset to defaults", severity="information")
        except Exception as e:
            self.notify(f"Error resetting configuration: {str(e)}", severity="error")
