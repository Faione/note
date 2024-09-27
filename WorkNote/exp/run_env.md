```shell
# redis
podman run -d --network host ict.acs.edu/app/redis:latest

# memcached
podman run -d --network host ict.acs.edu/app/memcached:latest -c 4096 -m 256

# mysql
podman run -d --network host -e ALLOW_EMPTY_PASSWORD=yes -e MYSQL_ROOT_PASSWORD=123456 ict.acs.edu/app/mysql:8.0.33

# nginx
podman run -d --rm --network host ict.acs.edu/app/nginx:latest

# monitor
podman run -d --network host --rm --privileged --name epollmonitor ict.acs.edu/infra/epoll_monitor:0.0.1

# scheduler
# podman run -d --rm --network host --privileged ict.acs.edu/scheduler/scx_simple:0.0.1 /schedulers/scx_simple -f -p
# podman run -d --rm --network host --privileged ict.acs.edu/scheduler/scx_exclusive:0.0.3 /schedulers/scx_exclusive -p -c 4

podman run -d --rm --network host --privileged ict.acs.edu/scheduler/scx_exclusive:0.0.4 /schedulers/scx_exclusive -p -c 4 -t 4
podman run -d --rm --network host --privileged ict.acs.edu/scheduler/scx_exclusive:0.0.5 /schedulers/scx_exclusive -p -c 4 -t 4 -s 4000000
podman run -d --name scheduler --rm --network host --privileged ict.acs.edu/scheduler/scx_exclusive:0.0.6 /schedulers/scx_exclusive -p -c 4 -t 4 -s 4000000

podman run -d --name scheduler --rm --network host --privileged ict.acs.edu/scheduler/scx_exclusive:0.0.6 /schedulers/scx_exclusive -p -c 2 -t 2 -s 1000000

# memtier
docker exec -it redis-client-1 memtier_benchmark -s 10.208.129.196 --port=11211 --protocol=memcache_text --generate-keys --test-time 30 -t 80 --hide-histogram

# tpcc
docker exec -it mysql-client-1 ./run.sh -h 10.208.129.2 -u root -p 123456 -d tpcc init
docker exec -it mysql-client-1 ./run.sh -h 10.208.129.2 -u root -p 123456 -d tpcc load
docker exec -it mysql-client-1 ./run.sh -h 10.208.129.2 -u root -p 123456 -d tpcc run

# graph500
podman run -d --name graph500 --network host ict.acs.edu/bench/graph500:moonkyung bash -c "time ./graph500/seq-csr/seq-csr -s 19 -e 16"

# ffmpeg
podman run -d --cpuset-cpus 1 --name ffmpeg --network host -v .controlzone/chicken_3840x2160_30.mkv:/test.mkv ict.acs.edu/app/ffmpeg:latest -benchmark -i /test.mkv  -f null -

./ffmpegwrapper.sh -benchmark -i /test.mkv -c:v libx264 -preset veryslow -f null -

podman run -d --cpuset-cpus 1 --name ffmpeg --network host -v .controlzone/chicken_3840x2160_30.mkv:/test.mkv ict.acs.edu/app/ffmpeg:latest -benchmark -i /test.mkv -s 640*360 -f null -

# wrk2
docker run --network host -it --rm ict.acs.edu/bench/wrk2:latest http://10.208.129.195  -t4 -c12 -d10s -R10000 -L

# stress
podman run -d --network host --name stress ict.acs.edu/bench/stress-ng:v0.4 sleep infinity

podman exec -d stress /stress-ng --cpu 4

for i in `pgrep stress`; do chsd w -p $i -s ext; done

chsd w -p `pgrep graph500` -s ext
```

nohup podman stats -i 1 --no-reset > test &