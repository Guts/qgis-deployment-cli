# How to use behind a network proxy

:::{info}
Only HTTP and HTTPS proxies are supported. No socks, no PAC.
:::

> See [Requests official documentation](https://docs.python-requests.org/en/latest/user/advanced/#proxies)

## Passing as CLI option

- the proxy configuration is scoped to the QDT execution.
- it supports only one URL for both HTTP and HTTPS

```sh
qdt --proxy-http "http://user:password@proxyserver.intra:8765"
```

----

## Using environment variables

### Generic `HTTP_PROXY` and `HTTPS_PROXY`

- it allows a specific URL by protocol (scheme)

### Custom `QDT_PROXY_HTTP`

- it avoids potential conflict with "classic" proxy settings
- it allows to use a specific network proxy for QDT (can be useful for some well controlled systems)

#### Example on Windows PowerShell

Only for the QDT command scope:

```powershell
$env:QDT_PROXY_HTTP='http://user:password@proxyserver.intra:8765'; qdt -vvv
```

At the shell session scope:

```powershell
> $env:QDT_PROXY_HTTP='http://user:password@proxyserver.intra:8765'
> qdt -vvv
```

----

## Defining custom SSL client certificates

Using a proxy for https connections typically requires the local machine to trust the proxy’s root certificate.

> See [Requests official documentation](https://docs.python-requests.org/en/latest/user/advanced/#ca-certificates)

### Using `REQUESTS_CA_BUNDLE` or `CURL_CA_BUNDLE`

Point to a certificat bundle file path (*.pem).

#### Example on Windows PowerShell

Only for the QDT command scope:

```powershell
$env:REQUESTS_CA_BUNDLE="$env:USERPROFILE\cacerts.pem"; qdt -vvv
```

At the shell session scope:

```powershell
> $env:REQUESTS_CA_BUNDLE="$env:USERPROFILE\cacerts.pem"
> qdt -vvv
```
