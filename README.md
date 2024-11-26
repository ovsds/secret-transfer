# Secret Transfer

[![CI](https://github.com/ovsds/secret-transfer/workflows/Check%20PR/badge.svg)](https://github.com/ovsds/secret-transfer/actions?query=workflow%3A%22%22Check+PR%22%22)

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

### Custom class definitions

You can define custom classes for sources, destinations, collections, and transfers.

#### Any resource

```python
import typing
import typing_extensions

import secret_transfer.core as secret_transfer_core


class CustomResource(...):
    __register__ = ... # bool: Should the class be registered on creation (optional, default: True)
    __default__ = ... # bool: Should the class be used as default for its type (optional, default: False)

    @classmethod
    def parse_init_arguments(
      cls,
      **arguments: secret_transfer_core.InitArgumentType
    ) -> typing.Mapping[str, typing.Any]:
        # Optional to implement
        # Parse and validate init arguments passed from the YaML definition for the future instance creation
        ...

    @classmethod
    def get_default_instances(cls) -> typing.Mapping[str, typing_extensions.Self]:
        # Optional to implement
        # Return default instances of the class to be registered at import-time
        ...
```

#### Source

```python
import secret_transfer.core as secret_transfer_core
import secret_transfer.utils.types as secret_transfer_types


class CustomSource(secret_transfer_core.AbstractSource):
    def __getitem__(self, key: str) -> secret_transfer_types.Literal:
        # Required to implement
        # Return the value of the secret by key
        ...
```

#### Destination

```python
import secret_transfer.core as secret_transfer_core
import secret_transfer.utils.types as secret_transfer_types


class CustomDestination(secret_transfer_core.AbstractDestination):
    def __setitem__(self, key: str, value: secret_transfer_types.Literal) -> None:
        # Required to implement
        # Set the value of the secret by key
        ...

    def __delitem__(self, key: str) -> None:
        # Optional to implement
        # Clean all secrets in the destination
        ...
```

#### Collection

```python
import typing

import secret_transfer.core as secret_transfer_core
import secret_transfer.utils.types as secret_transfer_types


class CustomCollection(secret_transfer_core.AbstractCollection):
    def __getitem__(self, key: str) -> secret_transfer_types.Literal:
        # Required to implement
        # Return the value of the secret by key
        ...

    def __iter__(self) -> typing.Iterator[str]:
        # Required to implement
        # Return an iterator over the keys of the collection
        ...

    def items(self) -> typing.Iterator[tuple[str, secret_transfer_types.Literal]]:
        # Required to implement
        # Return an iterator over the items of the collection
        ...
```

#### Transfer

```python
import secret_transfer.core as secret_transfer_core


class CustomTransfer(secret_transfer_core.AbstractTransfer):
    def run(self) -> None:
        # Required to implement
        # Transfer secrets
        ...

    def clean(self) -> None:
        # Required to implement
        # Clean all secrets in the transfer
        ...
```

### Usage Examples

Check [examples](examples/README.md) for usage examples.

## Development

### Global dependencies

- [Taskfile](https://taskfile.dev/installation/)
- [nvm](https://github.com/nvm-sh/nvm?tab=readme-ov-file#install--update-script)

### Taskfile commands

For all commands see [Taskfile](Taskfile.yaml) or `task --list-all`.

## License

[MIT](LICENSE)
