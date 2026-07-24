$path = 'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'
$b = 'https://abu168888.github.io/tvbox-config/'
$j = Get-Content $path -Raw -Encoding UTF8
$j = $j -replace '\./lib/', "$b`lib/"
$j = $j -replace '\./f45313da', "$b`f45313da-d63b-4484-8aa9-4a641929455b.png"
Set-Content $path $j -NoNewline -Encoding UTF8
Write-Host 'Done - encoding preserved'
