# Cloud Splitter Configuration Examples

## Basic Configuration

```toml
[paths]
download_dir = "~/Music/downloads"
output_dir = "~/Music/stems"

[download]
format = "bestaudio/best"
keep_original = true
```

## High-Quality Processing

```toml
[processing]
separator = "demucs"
stems = ["vocals", "drums", "bass", "other"]

[demucs]
model = "htdemucs"
shifts = 4
cpu_only = false
```

## CPU-Only Configuration

```toml
[processing]
separator = "spleeter"
stems = ["vocals", "drums", "bass", "other"]

[demucs]
cpu_only = true
shifts = 2
```

## Custom Stem Labels

```toml
[processing]
separator = "demucs"
stems = ["vocals", "drums", "bass", "other"]
custom_labels = {
    "vocals" = "lead_vocals",
    "drums" = "percussion",
    "bass" = "bass_guitar",
    "other" = "instruments"
}
```

## Batch Processing

```toml
[download]
batch_enabled = true
format = "bestaudio/best"
keep_original = false

[processing]
separator = "demucs"
stems = ["vocals", "drums", "bass", "other"]
```

## Development Configuration

```toml
[paths]
download_dir = "./downloads"
output_dir = "./output"

[download]
format = "bestaudio"
keep_original = true

[processing]
separator = "demucs"
stems = ["vocals", "drums", "bass", "other"]

[demucs]
model = "htdemucs"
cpu_only = true
shifts = 1
```

## Production Configuration

```toml
[paths]
download_dir = "/var/cloud-splitter/downloads"
output_dir = "/var/cloud-splitter/output"

[download]
format = "bestaudio/best"
keep_original = false
batch_enabled = true

[processing]
separator = "demucs"
stems = ["vocals", "drums", "bass", "other"]

[demucs]
model = "htdemucs"
cpu_only = false
shifts = 4
```
