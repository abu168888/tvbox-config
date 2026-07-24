$c = Get-Content "C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json" -Raw
$b = "https://abu168888.github.io/tvbox-config/"
$c = $c -replace './lib/', "$b`lib/"
$c = $c -replace './f45313da', "$b`f45313da"
$e = [System.Text.Encoding]::UTF8
[System.IO.File]::WriteAllText("C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json", $c, $e)
Write-Host "Path replacement done"
