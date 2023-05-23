# Hassio CLI

This is a simple command line tool to control your IoT devices through the Home Assistant API.

# Usage:
The config file should be provided to the command in the yaml format. The default name for the config file is "config.yaml". Look at the "config.yaml.example"!

In case that one needs to use an alternative config file name/path, the path shold be fed to the command by "-c"/"--config" option, e.g.,
```
hassio --config <config file path> set-br-100 hall-lamp
```

# Device type:
TBD