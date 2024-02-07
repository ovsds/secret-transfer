import secret_transfer


def main():
    with open("secrets.yaml") as f:
        app_settings = secret_transfer.ApplicationSettings.from_yaml(f.read())
    app = secret_transfer.Application.from_settings(app_settings)

    print(f"Secret from source: {app.resources.sources['lockbox']['TEST_KEY']}")

    print("All secrets from collection:")
    for key, value in app.resources.collections["default"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
