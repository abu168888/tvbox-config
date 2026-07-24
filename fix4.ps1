$path = 'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'
$b = 'https://abu168888.github.io/tvbox-config/'

# Read and parse as JSON to preserve encoding
$raw = Get-Content $path -Raw -Encoding UTF8
$config = $raw | ConvertFrom-Json

# Fix spider path
$config.spider = $b + $config.spider.Substring(2)

# Fix live URLs
foreach ($l in $config.lives) {
    if ($l.url -and $l.url.StartsWith('./')) {
        $l.url = $b + $l.url.Substring(2)
    }
}

# Fix site ext paths
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

# Serialize back with depth to preserve all properties
$output = $config | ConvertTo-Json -Depth 50
$enc = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($path, $output, $enc)

Write-Host 'OK - paths fixed'
