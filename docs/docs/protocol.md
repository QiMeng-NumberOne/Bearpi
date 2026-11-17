# FreshChain 閫氫俊鍗忚

## MQTT涓婚

| 涓婚 | 鏂瑰悜 | 鐢ㄩ€?|
|---|---|---|
| `freshchain/ia1/telemetry` | IA1 鈫?缃戝叧 | 鐜鍜屾墽琛屽櫒鐘舵€?|
| `freshchain/st1/telemetry` | ST1 鈫?缃戝叧 | GPS銆佺數瀛愬洿鏍忓拰鎶ヨ鐘舵€?|
| `freshchain/ia1/command` | 缃戝叧 鈫?IA1 | 鑷姩/鎵嬪姩銆侀鎵囧拰琛ュ厜鐏帶鍒?|
| `freshchain/st1/command` | 缃戝叧 鈫?ST1 | 杩愯緭銆佺數瀛愬洿鏍忓拰娑堥煶鎺у埗 |
| `freshchain/event` | 鑺傜偣 鈫?缃戝叧 | 鎶ヨ鍜屼笟鍔′簨浠?|

## IA1鍛戒护

```json
{"action":"set_mode","mode":"auto"}
{"action":"fan","value":1}
{"action":"fan","value":0}
{"action":"light","value":1}
{"action":"light","value":0}
```

## ST1鍛戒护

```json
{"action":"start_transport"}
{"action":"end_transport"}
{"action":"set_geofence","latitude":31.2304,"longitude":121.4737,"radius_m":80}
{"action":"silence"}
```

## 鏂綉绛栫暐

- IA1锛氱户缁噰鏍峰拰鏈湴闃堝€兼帶鍒讹紱缃戠粶鎭㈠鍚庣户缁笂鎶ャ€?- ST1锛氱户缁璆PS瑙ｆ瀽鍜屾湰鍦扮數瀛愬洿鏍忓垽鏂紱缃戠粶鎭㈠鍚庣户缁笂鎶ャ€?- 缃戝叧锛氫繚瀛樻渶杩戠姸鎬併€佸巻鍙查仴娴嬨€佸懡浠ゅ拰鎶ヨ浜嬩欢鍒癝QLite銆?

