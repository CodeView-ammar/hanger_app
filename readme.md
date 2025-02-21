systemctl restart hanger_app.service && systemctl restart nginx

sudo systemctl stop hanger_app.service && sudo systemctl stop nginx

systemctl daemon-reload

sudo systemctl start hanger_app.socket && sudo systemctl start nginx


559372109