Set-Location "C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new"
Copy-Item "C:\Users\Administrator\Desktop\tvbox\newwex\newwex.json" "config.json" -Force
$raw = Get-Content config.json -Raw -Encoding UTF8
$config = $raw | ConvertFrom-Json
$b = 'https://abu168888.github.io/tvbox-config/'

$config.spider = $b + $config.spider.Substring(2)

foreach ($l in $config.lives) {
    if ($l.url -and $l.url.StartsWith('./')) {
        $l.url = $b + $l.url.Substring(2)
    }
}

foreach ($s in $config.sites) {
    if ($s.ext -is [string] -and $s.ext.StartsWith('./')) {
        $s.ext = $b + $s.ext.Substring(2)
    }
    if ($s.ext -is [hashtable]) {
        foreach ($k in @($s.ext.Keys)) {
            if ($s.ext[$k] -is [string] -and $s.ext[$k].StartsWith('./')) {
                $s.ext[$k] = $b + $s.ext[$k].Substring(2)
            }
        }
    }
}

$output = $config | ConvertTo-Json -Depth 50
$enc = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText("config.json", $output, $enc)

git add config.json
git commit -m "fix: replace relative paths with GitHub Pages URLs"
git push

Write-Host "Done - fixed and pushed"
