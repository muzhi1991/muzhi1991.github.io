#!/bin/bash 
npm install
npm install hexo-generator-cname --save
npm install hexo-generator-sitemap --save
npm install hexo-generator-baidu-sitemap --save
# for bug??
npm install highlight.js --save
# next 5.x
# git clone https://github.com/iissnan/hexo-theme-next themes/next
# next 6.x
# git clone https://github.com/theme-next/hexo-theme-next themes/next-reloaded
# next lastest release
rm -rf themes/next
mkdir themes/next
curl -s https://api.github.com/repos/theme-next/hexo-theme-next/releases/latest | grep tarball_url | cut -d '"' -f 4 | wget -i - -O- | tar -zx -C themes/next --strip-components=1

# next-reloaded is next6.x
echo '请手动修改一些问题bac_20190615'
#cp -Rf ./bac/bac_20190615/* ./

