
## Run tests

```shell
docker build . -f tests/Dockerfile -t pynvr2-tests
docker run -it -v `pwd`:/project pynvr2-tests
```

Optionally, you can specify `--build-arg GROUP_ID=$(id -g) --build-arg USER_ID=$(id -u)` to `docker build`
to match your host user/group ids. Both values default to `1000`.
