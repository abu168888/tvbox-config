Set-Location "C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new"
$raw = Get-Content config.json -Raw -Encoding UTF8
$config = $raw | ConvertFrom-Json
$b = 'https://abu168888.github.io/tvbox-config/'

Write-Host "Original spider: $($config.spider)"
$config.spider = $b + $config.spider.Substring(2)
Write-Host "Fixed spider: $($config.spider)"

foreach ($l in $config.lives) {
    if ($l.url -and $l.url.StartsWith('./')) {
        Write-Host "Fixing live: $($l.url)"
        $l.url = $b + $l.url.Substring(2)
    }
}

$count = 0
foreach ($s in $config.sites) {
    if ($s.ext -is [string] -and $s.ext.StartsWith('./')) {
        $s.ext = $b + $s.ext.Substring(2)
        $count++
    }
    if ($s.ext -is [hashtable]) {
        foreach ($k in @($s.ext.Keys)) {
            if ($s.ext[$k] -is [string] -and $s.ext[$k].StartsWith('./')) {
                $s.ext[$k] = $b + $s.ext[$k].Substring(2)
                $count++
            }
        }
    }
}
Write-Host "Fixed $count site ext paths"

$output = $config | ConvertTo-Json -Depth 50
$enc = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText("config.json", $output, $enc)

git add config.json
git commit -m "fix: force replace all relative paths with GitHub Pages URLs"
git push origin main

Write-Host "Pushed successfully!"
