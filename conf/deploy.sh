# 代码更新
git pull

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f /root/ying-3.com/yingsan.conf /etc/supervisor/conf.d/yingsan.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /root/ying-3.com/yingsan.nginx /etc/nginx/sites-enabled/yingsan

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy success'