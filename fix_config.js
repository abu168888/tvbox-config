const fs = require('fs');

// Read config.json
const configPath = 'config.json';
let config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

const baseUrl = 'https://abu168888.github.io/tvbox-config/';

// Fix spider path
if (config.spider && config.spider.startsWith('./')) {
    config.spider = baseUrl + config.spider.substring(2);
    console.log('Fixed spider:', config.spider);
}

// Fix lives
for (const live of config.lives || []) {
    if (live.url && live.url.startsWith('./')) {
        live.url = baseUrl + live.url.substring(2);
        console.log('Fixed live:', live.url);
    }
}

// Fix site ext paths
let count = 0;
for (const site of config.sites || []) {
    if (typeof site.ext === 'string' && site.ext.startsWith('./')) {
        site.ext = baseUrl + site.ext.substring(2);
        count++;
    }
    if (typeof site.ext === 'object' && site.ext !== null) {
        for (const key in site.ext) {
            if (typeof site.ext[key] === 'string' && site.ext[key].startsWith('./')) {
                site.ext[key] = baseUrl + site.ext[key].substring(2);
                count++;
            }
        }
    }
}
console.log(`Fixed ${count} site ext paths`);

// Write back with UTF-8 (no BOM)
fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
console.log('✅ Config file updated successfully!');
console.log('\nFirst 3 sites:');
console.log(JSON.stringify(config.sites.slice(0, 3), null, 2));
