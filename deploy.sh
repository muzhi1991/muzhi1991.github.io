#!/bin/bash 
hexo clean
hexo generate

# seo优化
cp -Rf ./bac/public/* ./public/

hexo deploy

