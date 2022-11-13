# Json Mock

[json-server](https://www.npmjs.com/package/json-server)

docker-compose

```yaml
version: "3"
services:
  mock-server:
    image: clue/json-server:latest
    ports:
      - "27188:80"
    volumes:
    - ./db.json:/data/db.json  

```

定义接口

```
{
  "posts": [
    { "id": 1, "body": "foo" },
    { "id": 2, "body": "bar" }
  ],
  "comments": [
    { "id": 1, "body": "baz", "postId": 1 },
    { "id": 2, "body": "qux", "postId": 2 }
  ]
}
```