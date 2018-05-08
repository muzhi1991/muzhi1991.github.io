#!/bin/bash 
npm install
npm install hexo-generator-cname --save
npm install hexo-generator-sitemap --save
npm install hexo-generator-baidu-sitemap --save
git clone https://github.com/iissnan/hexo-theme-next themes/next
cp -Rf ./bac/bac_20180507/* ./themes/next/

