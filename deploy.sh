#!/bin/bash 
hexo clean
hexo generate

# seo优化
cp -Rf ./bac/public_bac/* ./public/

hexo deploy

