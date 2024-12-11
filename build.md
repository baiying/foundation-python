# 构建并发布项目
## 构建项目
```shell
poetry build
```
## 发布程序包
```shell
# 首次发布时需要配置Pypi的发布Token
poetry config pypi-token.pypi <your-token>
# 将程序包上传到pypi中
poetry publish --build
```
## 版本管理和升级
在发布新版本前，需要更新 pyproject.toml 中的 version 字段，或者直接使用 poetry 提供的命令：
```shell
poetry version patch  # 更新补丁版本号
poetry version minor  # 更新次版本号
poetry version major  # 更新主版本号
```