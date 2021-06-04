#!/bin/sh

LOCAL_PORT=18888
REMOTE_PORT=14443

dir=`dirname $0`
abs_dir=`cd $dir && pwd`
tele_dir="$abs_dir/telegram"

if [ ! -d $tele_dir ]; then
  mkdir $tele_dir
  if [ $? -ne 0 ];then
      echo 'create $ss_dir failure'
      exit 1
  fi
fi

cd $tele_dir
yum install openssl-devel zlib-devel -y && yum groupinstall "Development Tools" -y

git clone https://github.com/TelegramMessenger/MTProxy
cd MTProxy
make clean && make && cd objs/bin

mtproto_proxy="$tele_dir/MTProxy/objs/bin/mtproto-proxy"

cd $tele_dir 
curl -s https://core.telegram.org/getProxySecret -o proxy-secret

curl -s https://core.telegram.org/getProxyConfig -o proxy-multi.conf

secret=$(head -c 16 /dev/urandom | xxd -ps)

cmd="$mtproto_proxy -u nobody -p $LOCAL_PORT -H $REMOTE_PORT -S $secret --aes-pwd proxy-secret proxy-multi.conf -M 1"


