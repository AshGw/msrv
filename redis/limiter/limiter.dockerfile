FROM redis:6.0.7

WORKDIR .
# do COPY redis/tokens/redis.conf if ure running this from the root compose file
# do COPY redis.conf redis.conf if ure running it from the local compose
COPY redis/limiter/redis.conf redis.conf

# this here dsiables THP support
RUN echo "echo never > /sys/kernel/mm/transparent_hugepage/enabled" > /etc/rc.local \
    && chmod +x /etc/rc.local

# resolving latency memory issues
RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf \
    && cat /etc/sysctl.conf

CMD ["redis-server", "redis.conf"]
