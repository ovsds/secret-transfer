# Secret Transfer

YaML-based secret manager for secret load/transfer from different sources to destinations.

## Base idea

The base idea is to have a simple and flexible way to transfer secrets from different sources to different destinations.

The main components are:

- **Source** - A place where secrets are stored. It can be a file, environment variables, a database, a cloud service, etc.
- **Destination** - A place where secrets are transferred. It can be environment variables, a file, a cloud service, etc.
- **Collection** - A collection of secrets from sources. It can be used to combine secrets from different sources.
- **Transfer** - A transfer of secrets from a collection to a destination.

## Features

- **YaML-based** - Define sources, destinations, collections, and transfers in a YaML file.
- **Lazy loading** - Define objects in no particular order and reference them from one another.
- **Cross-referencing** - Reference sources, destinations, collections, and transfers from one another.
- **Built-in classes** - Use built-in classes for sources, destinations, collections, and transfers.
- **Extensible** - Add custom classes for sources, destinations, collections, and transfers.

## Usage

### CLI Commands

#### Run

Run all transfers in the given YaML file.

```bash
secret-transfer run -f <path_to_yaml_file>
```

Options:

- `-f, --file <path_to_yaml_file>` - Path to the YaML file with secrets. [required]
- `-n, --name <name>` - Name of the transfer to run. [optional]

#### Clean

Clean all secrets in all transfer destinations in the given YaML file.

```bash
secret-transfer clean -f <path_to_yaml_file>
```

Options:

- `-f, --file <path_to_yaml_file>` - Path to the YaML file with secrets. [required]
- `-n, --name <name>` - Name of the transfer to clean. [optional]

### YaML schema

The YaML file should contain the following optional sections:

Custom class definitions for sources, destinations, collections, and transfers.

```yaml
source_classes:
  <name>: # Name to be registered
    module: <module> # Module to import from
    class_name: <class_name> # Class to be registered
destination_classes: ...
collection_classes: ...
transfer_classes: ...
```

Sources, destinations, collections, and transfers.

```yaml
sources:
  <name>:
    class_name: <source_class_name> # Class to use, either from source_classes or built-in
    init_args: # Arguments to pass to the class constructor, can be omitted if no arguments are needed
      <arg_name>: <arg_value>
      ...
destinations:
  ...
collections:
  ...
transfers:
  ...
```

### Lasy loading

All items are lazily loaded, so they are not created until they are used. This allows to define objects in no particular order and reference them from one another. The only exception is built-in classes, which are registered at import-time.

Cross-referencing is allowed, so you can reference sources, destinations, collections, transfers and their values from init_args. Circular references are not allowed.

### Cross-referencing

#### Instance references

To reference instances of sources, destinations, collections, and transfers, use the following syntax:

```yaml
$<type>[<name>]
```

Where:

- `<type>` - Type of the instance (source, destination, collection, or transfer).
- `<name>` - Name of the instance.

#### Value references

To reference values from sources or collections, use the following syntax:

```yaml
$<type>[<name>][<key>]
```

Where:

- `<type>` - Type of the gettable instance (usually, but not necessarily source or collection).
- `<name>` - Name of the instance.
- `<key>` - Key of the value.

Where:

### Built-in classes

#### Sources

##### DotEnvSource

Load secrets from a .env file using `dotenv` package.
Arguments:

- `file_path` - Path to the .env file. [required]

Example:

```yaml
sources:
  dotenv:
    class_name: DotEnvSource
    init_args:
      file_path: .env
```

##### EnvSource

Load secrets from environment variables.
Arguments: none.

Already registered with name `env`, no need to define in the YaML file.

Example:

```yaml
collections:
  default:
    init_args:
      TEST_KEY:
        source: $sources[env]
```

##### PresetSource

Load secrets from a preset dictionary.
Arguments: key-value pairs of variables.

Example:

```yaml
sources:
  preset:
    class_name: PresetSource
    init_args:
      TEST_KEY: test_value
```

##### UserInputSource

Asks the user for input.
Arguments: none.

Already registered with name `user_input`, no need to define in the YaML file.

Example:

```yaml
collections:
  default:
    init_args:
      TEST_KEY:
        source: $sources[user_input]
```

##### VaultCLIKVSource

Load secrets from HashiCorp Vault KV using `vault kv get` CLI command.
Arguments:

- `address` - Address of the Vault server. [required]
- `mount` - Mount point of the KV engine. [required]
- `secret_name` - Name(path) of the secret. [required]

Pre-requisites:

- `vault` CLI installed and authenticated.

Example:

```yaml
sources:
  vault:
    class_name: VaultCLIKVSource
    init_args:
      address: https://vault.example.com
      mount: secrets
      secret_name: TEST_SECRET
```

##### YCCLILockboxSource

Load secrets from Yandex.Cloud Lockbox using `yc lockbox payload get` CLI command.
Arguments:

- `profile` - Name of the Yandex.Cloud CLI profile. [required]
- `folder` - Folder name. [required]
- `lockbox` - Lockbox name. [required]

Pre-requisites:

- `yc` CLI installed and authenticated.

Example:

```yaml
sources:
  yc_lockbox:
    class_name: YCCLILockboxSource
    init_args:
      profile: my-profile
      folder: my-folder
      lockbox: my-lockbox
```

#### Destinations

##### BashExportDestination

Print secrets as `export` commands to the console. Useful for setting environment variables. Never let stdout to be captured by a process, as it will expose the secrets.
Arguments: none.

Already registered with name `bash_export`, no need to define in the YaML file.

Example:

```yaml
transfers:
  default:
    init_args:
      source: ...
      destination: $destinations[bash_export]
```

##### EnvDestination

Set secrets as environment variables.
Arguments: none.

Already registered with name `env`, no need to define in the YaML file.

Example:

```yaml
transfers:
  default:
    init_args:
      source: ...
      destination: $destinations[env]
```

##### GithubCliSecretsDestination

Set secrets as GitHub repository secrets using `gh secret set` CLI command.
Arguments:

- `repo_name` - Name of the repository. [required]
- `owner_name` - Name of the repository owner. [required]
- `base_url` - Base URL of the GitHub API. [optional] (default: https://github.com)

Pre-requisites:

- `gh` CLI installed and authenticated.

Example:

```yaml
destinations:
  github:
    class_name: GithubCliSecretsDestination
    init_args:
      repo_name: my-repo
      owner_name: my-org
```

#### Collections

##### DefaultCollection

Default collection to combine secrets from sources. Default collection class, so class_name can be omitted.

Example:

```yaml
collections:
  default:
    init_args:
      COLLECTION_KEY:
        source: $sources[env]
        key: SOURCE_KEY
```

#### Transfers

##### DefaultTransfer

Default transfer to transfer secrets from collection to destination. Default transfer class, so class_name can be omitted.

Example:

```yaml
transfers:
  default:
    init_args:
      collection: $collections[default]
      destination: $destinations[env]
```

### Usage Examples

Check [examples](examples/README.md) for usage examples.

## Development

### Taskfile commands

For all commands see [Taskfile](Taskfile.yaml) or `task --list-all`.
