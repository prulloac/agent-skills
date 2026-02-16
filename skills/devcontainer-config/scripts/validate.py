#!/usr/bin/env python3
"""
Validate devcontainer.json files for common issues and best practices.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class DevContainerValidator:
    """Validates devcontainer.json configuration files."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> bool:
        """Run all validation checks."""
        if not self._load_config():
            return False
            
        self._check_required_properties()
        self._check_scenario_properties()
        self._check_user_configuration()
        self._check_lifecycle_scripts()
        self._check_port_configuration()
        self._check_variable_usage()
        
        return len(self.errors) == 0
    
    def _load_config(self) -> bool:
        """Load and parse the JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.config_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
    
    def _check_required_properties(self):
        """Check for recommended basic properties."""
        if 'name' not in self.config:
            self.warnings.append("Missing 'name' property - recommended for UI display")
    
    def _check_scenario_properties(self):
        """Validate scenario-specific properties."""
        has_image = 'image' in self.config
        has_dockerfile = 'build' in self.config and 'dockerfile' in self.config.get('build', {})
        has_compose = 'dockerComposeFile' in self.config
        
        scenario_count = sum([has_image, has_dockerfile, has_compose])
        
        if scenario_count == 0:
            self.errors.append(
                "Must specify one of: 'image', 'build.dockerfile', or 'dockerComposeFile'"
            )
        elif scenario_count > 1:
            self.errors.append(
                "Cannot specify multiple scenarios - choose only one of: "
                "'image', 'build.dockerfile', or 'dockerComposeFile'"
            )
        
        # Validate Docker Compose specific requirements
        if has_compose:
            if 'service' not in self.config:
                self.errors.append(
                    "When using 'dockerComposeFile', 'service' property is required"
                )
        
        # Validate Dockerfile build configuration
        if has_dockerfile:
            build_config = self.config.get('build', {})
            dockerfile_path = self.config_path.parent / build_config.get('dockerfile', '')
            if not dockerfile_path.exists():
                self.warnings.append(
                    f"Dockerfile not found at: {build_config.get('dockerfile')}"
                )
    
    def _check_user_configuration(self):
        """Check user-related configuration."""
        if 'containerUser' in self.config and 'remoteUser' not in self.config:
            self.warnings.append(
                "Consider setting 'remoteUser' when using 'containerUser' to specify "
                "the user for dev tools separately from the container"
            )
    
    def _check_lifecycle_scripts(self):
        """Validate lifecycle script properties."""
        lifecycle_props = [
            'initializeCommand',
            'onCreateCommand',
            'updateContentCommand',
            'postCreateCommand',
            'postStartCommand',
            'postAttachCommand'
        ]
        
        for prop in lifecycle_props:
            if prop in self.config:
                value = self.config[prop]
                if not isinstance(value, (str, list, dict)):
                    self.errors.append(
                        f"'{prop}' must be a string, array, or object, got {type(value).__name__}"
                    )
    
    def _check_port_configuration(self):
        """Validate port forwarding configuration."""
        if 'forwardPorts' in self.config:
            ports = self.config['forwardPorts']
            if not isinstance(ports, list):
                self.errors.append("'forwardPorts' must be an array")
            else:
                for port in ports:
                    if not isinstance(port, (int, str)):
                        self.errors.append(
                            f"Invalid port in 'forwardPorts': {port}. "
                            "Must be a number or 'host:port' string"
                        )
        
        if 'portsAttributes' in self.config:
            attrs = self.config['portsAttributes']
            if not isinstance(attrs, dict):
                self.errors.append("'portsAttributes' must be an object")
            else:
                valid_keys = ['label', 'protocol', 'onAutoForward', 'requireLocalPort', 'elevateIfNeeded']
                for port, settings in attrs.items():
                    for key in settings:
                        if key not in valid_keys:
                            self.warnings.append(
                                f"Unknown port attribute '{key}' for port {port}"
                            )
    
    def _check_variable_usage(self):
        """Check for proper variable usage."""
        def check_string_value(value: str, path: str):
            if '${' in value:
                # Basic validation of variable syntax
                if value.count('${') != value.count('}'):
                    self.warnings.append(
                        f"Unmatched variable brackets in '{path}': {value}"
                    )
        
        def walk_config(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    walk_config(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    walk_config(item, f"{path}[{i}]")
            elif isinstance(obj, str):
                check_string_value(obj, path)
        
        walk_config(self.config)
    
    def print_results(self):
        """Print validation results."""
        print(f"\n{'='*60}")
        print(f"Validation Results for: {self.config_path.name}")
        print(f"{'='*60}\n")
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  - {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ No issues found!\n")
        elif not self.errors:
            print("✅ No critical errors (warnings only)\n")
        else:
            print(f"❌ Validation failed with {len(self.errors)} error(s)\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <path-to-devcontainer.json>")
        sys.exit(1)
    
    validator = DevContainerValidator(sys.argv[1])
    is_valid = validator.validate()
    validator.print_results()
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
