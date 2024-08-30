# Defining custom SSL client certificates

Using a [proxy](./howto_behind_proxy.md) for https connections typically requires the local machine to trust the proxy’s root certificate. By default, a bundle of SSL certificates is used, through [certifi](https://pypi.org/project/certifi/) (using Mozilla curated list).

> See [Requests official documentation](https://docs.python-requests.org/en/latest/user/advanced/#ca-certificates)

Here comes how to customize which certificates bundle to use or how to require QDT to use the native system certificates store.

## Using `REQUESTS_CA_BUNDLE` or `CURL_CA_BUNDLE`

Point to a certificat bundle file path (*.pem).

### Example on Windows PowerShell

Only for the QDT command scope:

```powershell
$env:REQUESTS_CA_BUNDLE="$env:USERPROFILE\cacerts.pem"; qdt -vvv
```

At the shell session scope:

```powershell
> $env:REQUESTS_CA_BUNDLE="$env:USERPROFILE\cacerts.pem"
> qdt -vvv
```

## Using native system certificates store

If the `QDT_SSL_USE_SYSTEM_STORES` environment variable is set to `true`, HTTPS requests rely on the native system certificates store.

:::{note}
If enabled, this environment variable take precedence over `REQUESTS_CA_BUNDLE` or `CURL_CA_BUNDLE` which are ignored.
:::

### Example on Windows PowerShell

Only for the QDT command scope:

```powershell
$env:QDT_SSL_USE_SYSTEM_STORES='true'; qdt -vvv
```

At the shell session scope:

```powershell
> $env:QDT_SSL_USE_SYSTEM_STORES='true'
> qdt -vvv
```
