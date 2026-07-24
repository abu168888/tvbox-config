const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

const base = 'https://abu168888.github.io/tvbox-config/';

// Fix spider path
if (config.spider && config.spider.startsWith('./')) {
    config.spider = base + config.spider.substring(2);
}

// Fix lives
for (const live of config.lives || []) {
    if (live.url && live.url.startsWith('./')) {
        live.url = base + live.url.substring(2);
    }
}

// Fix site ext paths
for (const site of config.sites || []) {
    if (typeof site.ext === 'string' && site.ext.startsWith('./')) {
        site.ext = base + site.ext.substring(2);
    }
    if (typeof site.ext === 'object' && site.ext !== null) {
        for (const [k, v] of Object.entries(site.ext)) {
            if (typeof v === 'string' && v.startsWith('./')) {
                site.ext[k] = base + v.substring(2);
            }
        }
    }
}

// Write with BOM for UTF-8 compatibility
const utf8BOM = '\uFEFF';
fs.writeFileSync(configPath, utf8BOM + JSON.stringify(config, null, 2), 'utf-8');

console.log('Config updated with GitHub Pages URLs');
console.log('Spider:', config.spider);
console.log('Sites count:', config.sites?.length);
console.log('First site ext:', config.sites?.[0]?.ext);
