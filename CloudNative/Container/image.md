# Image Format

image dir

```
.
├── 3bbce41bd9adf98341716bd7fea660315a17e14258dd140bad27fe59d27dd7d8
│   ├── json
│   ├── layer.tar
│   └── VERSION
├── a1f3735d558fd4f7df9b74ba68f4a493bc1a3a68233edce77869eab8d37c3443
│   ├── json
│   ├── layer.tar
│   └── VERSION
├── a9fa6a1fe312035c282f5e90e2932250af79a3b71d74e1dce7ae0314b238bcc0.json
├── f930b014600c3642ae73e0dbb1159ad518514236f57846a849d1bf610bcfe9a0
│   ├── json
│   ├── layer.tar
│   └── VERSION
└── manifest.json
```

`./*.json` 会被放到 `/var/lib/docker/image/overlay2/imagedb/content/sha256` 中

[^1]: [moby_image_spec](https://github.com/moby/moby/blob/master/image/spec/v1.md)
[^2]: [opencontainer_image_spec](https://github.com/opencontainers/image-spec/blob/main/spec.md)

## Image Save

关键目录 `image/overlay2`, `distribution` 中记录了 `diffid-by-digest` 与 `v2metadata-by-diffid`, 用以进行 `diffid <-> digest` 的相互转换, 后者为压缩时的 sha256 值, 前者为未压缩的 sha256 值, 需要注意的是, 这些 id 都与 layer 有关, 通常在 image 中保存的是 `diffid`, 通过diffid 可以计算得到 chainid, 通过此id可以在 `layerdb/sha256` 中找到layer的相关文件, 其中 `cache-id` 指向了 `overlay2` 中的实际解压后的文件系统的存储位置, `diff` 则表示 diffid

[^3]: [image_ids](https://blog.csdn.net/qq_24433609/article/details/120763486)
[^4]: [understand_image_ids](https://kingdo.club/2022/02/21/understand-layerid-diffid-chainid-cache-id/)