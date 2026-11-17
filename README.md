# 鲜运智联 FreshChain — BearPi-HM Nano 课程项目

农产品产地环境与运输轨迹双节点监管系统，包含：

- `firmware/freshchain_ia1`：IA1 温湿度/光照采集、风扇/补光控制、MQTT 上报；
- `firmware/freshchain_st1`：ST1 GPS/蜂鸣器、MQTT 上报、运输状态；
- `gateway/`：Python MQTT/HTTP 网关、SQLite 存储、SARIMAX 预测与分级预警、网页看板；
- `docs/`：需求分析与设计、项目代码梳理。

## 运行环境

- 开发板：BearPi-HM Nano（Hi3861）
- 扩展板：E53_IA1、E53_ST1
- MQTT Broker：Mosquitto，端口 `1884`
- 网关：Python 3.11，HTTP `8080`

## 固件配置

烧录前修改：

```c
#define FRESHCHAIN_WIFI_SSID "YOUR_2.4G_SSID"
#define FRESHCHAIN_WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define FRESHCHAIN_MQTT_HOST "YOUR_PC_IP"
#define FRESHCHAIN_MQTT_PORT 1884
```

`BUILD.gn` 一次只启用一个节点：

```gn
# IA1
"freshchain_ia1:freshchain_ia1",
#"freshchain_st1:freshchain_st1",
```

或：

```gn
#"freshchain_ia1:freshchain_ia1",
"freshchain_st1:freshchain_st1",
```

分别编译、烧录到对应开发板。

## 启动网关

```powershell
C:\Program Files\mosquitto\mosquitto.exe -c gateway\broker\mosquitto.conf -v
D:\CodeTools\conda_envs\freshchain\python.exe gateway\server.py --mqtt-host 127.0.0.1 --mqtt-port 1884
```

浏览器打开：

```text
http://127.0.0.1:8080
```

## MQTT 主题

```text
freshchain/ia1/telemetry
freshchain/st1/telemetry
freshchain/ia1/command
freshchain/st1/command
```

## 说明

本仓库只包含课程项目代码，不包含完整的 BearPi/OpenHarmony SDK。
将 `firmware/` 下的样例复制到 BearPi-HM Nano SDK 的
`applications/BearPi/BearPi-HM_nano/sample/` 后编译。

数据库 `freshchain.db`、构建产物和个人实验报告未上传。
