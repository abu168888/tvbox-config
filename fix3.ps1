# Step 1: Re-read from source (clean copy)
$path = 'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json'
Copy-Item 'C:\Users\Administrator\Desktop\tvbox\newwex\newwex.json' $path -Force

# Step 2: Parse JSON, modify paths, write back
$json = Get-Content $path -Raw -Encoding UTF8 | ConvertFrom-Json
$b = 'https://abu168888.github.io/tvbox-config/'

# Fix spider path
$json.spider = $json.spider -replace './', "$b"

# Fix lives
foreach ($l in $json.lives) {
    if ($l.url -and $l.url.StartsWith('./')) {
        $l.url = $b + $l.url.Substring(2)
    }
}

# Fix site ext paths
foreach ($s in $json.sites) {
    if ($s.ext -and $s.ext -is [string] -and $s.ext.StartsWith('./')) {
        $s.ext = $b + $s.ext.Substring(2)
    }
    if ($s.ext -and $s.ext -is [hashtable]) {
        foreach ($k in $s.ext.Keys) {
            if ($s.ext[$k] -is [string] -and $s.ext[$k].StartsWith('./')) {
                $s.ext[$k] = $b + $s.ext[$k].Substring(2)
            }
        }
    }
}

# Step 3: Write back with proper encoding
$output = $json | ConvertTo-Json -Depth 100
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($path, $output, $utf8NoBom)

Write-Host "Done - spider: $($json.spider)"
Write-Host "Sites count: $($json.sites.Count)"
