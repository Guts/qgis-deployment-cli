# How to use behdin a network proxy

:::{info}
Only HTTP and HTTPS proxies are supported. Not socks, no PAC.
:::

## Passing as CLI option

- the proxy configuration is scoped to the QDT execution.
- it supports only one URL for both HTTP and HTTPS

```sh
qdt --proxy-http "http://user:password@proxyserver.intra:8765"
```

## Using environment variables

### Generic `HTTP_PROXY` and `HTTPS_PROXY`

- it allows a specific URL by protocol (scheme)

### Custom `QDT_PROXY_HTTP`

- it avoids potential conflict with "classic" proxy settings
- it allows to use a specific network proxy for QDT (can be useful for some well controlled systems)
