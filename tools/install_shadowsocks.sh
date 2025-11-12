#!/bin/sh

SS_PORT=8388
PASSWD=123456
dir=`dirname $0`
abs_dir=`cd $dir && pwd`
ss_dir="$abs_dir/shadowsocks"
if [ ! -d $ss_dir ]; then
  mkdir shadowsocks
  if [ $? -ne 0 ];then
      echo 'create $ss_dir failure'
      exit 1
  fi
fi

printf 'input server port ['$SS_PORT']'
while read LINE; do
   if [ -n "$LINE" ]; then
     SS_PORT=$LINE
   fi
   break
done

printf 'input server password ['$PASSWD']'
while read LINE; do
   if [ -n "$LINE" ]; then
     PASSWD=$LINE
   fi
   break
done

cd $ss_dir 

yum install git -y && yum install python-setuptools -y && easy_install pip && pip install shadowsocks
if [ $? -ne 0 ];then
      echo 'install shadowsocks failur'
      exit 1
fi

echo '{'                                > ssserver.json
echo '    "server": "0.0.0.0",'         >> ssserver.json
echo '    "port_password":'             >> ssserver.json
echo '        {'                        >> ssserver.json
echo '         "'$SS_PORT'": "'$PASSWD'"' >> ssserver.json
echo '       },'                         >> ssserver.json
echo '    "timeout": 300,'              >> ssserver.json
echo '    "method": "aes-256-cfb",'     >> ssserver.json
echo '    "fast_open": false'           >> ssserver.json
echo '}'                                >> ssserver.json

ssserver -c ssserver.json -d start
if [ $? -ne 0 ];then
      echo 'start shadowsocks failur'
      exit 1
fi

firewall-cmd --zone=public --add-port=$SS_PORT/tcp --permanent
firewall-cmd --reload
