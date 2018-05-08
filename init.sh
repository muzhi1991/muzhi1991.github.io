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
git clone https://github.com/theme-next/hexo-theme-next themes/next-reloaded
# next-reloaded is next6.x
cp -Rf ./bac/bac_20180508/* ./themes/next-reloaded/

