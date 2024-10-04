// Sample PAC File for QDT Test

function FindProxyForURL(url, host)
{
if (shExpMatch(host,"*.no-proxy.fr"))
        return "DIRECT";

else return "PROXY myproxy:8080";
}


