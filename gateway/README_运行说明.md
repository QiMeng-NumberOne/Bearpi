# FreshChain 鏈湴杩愯璇存槑锛堝凡鏀剧疆濂斤級

> **涓撳睘鐜**锛歚D:\CodeTools\conda_envs\freshchain`  
> Python 3.11.18 + paho-mqtt 2.1.0 + scikit-learn 1.9.1 + pandas 3.1.0 + statsmodels 0.15.0 + joblib 1.6.0  
> 婵€娲伙細`conda activate D:\CodeTools\conda_envs\freshchain`  
> 鎴栫洿鎺ヤ娇鐢細`D:\CodeTools\conda_envs\freshchain\python.exe`

鏈洰褰曟槸鐢佃剳绔綉鍏充笌鍙傝€冨浐浠躲€侽penHarmony 鍥轰欢鏍蜂緥宸茬粡鏀惧埌锛?
```text
applications/BearPi/BearPi-HM_Nano/sample/freshchain_ia1/
applications/BearPi/BearPi-HM_Nano/sample/freshchain_st1/
```

褰撳墠 `sample/BUILD.gn` **鍙惎鐢ㄤ簡 IA1**銆傜儳瀹?IA1 鍚庯紝鏀规垚 ST1 鍐嶇紪璇戜竴娆★紝鍒嗗埆鐑у埌涓ゅ潡鏉裤€?
> IA1 閲囨牱鍛ㄦ湡宸叉敼涓?**1 绉?*锛汼T1 浠嶄繚鎸?**5 绉?*锛圙PS 涓€娆¤鍙栫害 1 绉掞紝鍏堜笉鍔級銆?
## AI 棰勬祴涓庨璀?
缃戝叧宸叉帴鍏?`gateway/ai_service.py`锛屼笉棰濆鍚姩鏈嶅姟锛岄殢 `server.py` 涓€璧疯繍琛岋細

```text
GET  /api/ai           # 棰勬祴 + 褰撳墠棰勮 + 闃堝€?GET  /api/forecast     # 鍙彇棰勬祴
GET  /api/alerts       # 鍘嗗彶棰勮
POST /api/alerts/{id}/ack
```

棰勬祴浣跨敤 **SARIMAX**锛坰tatsmodels锛夛細鎶婅矾绾跨偣鎴栨渶杩?IA1 瀹炴椂閬ユ祴鎸?10 绉掗噸閲囨牱鍚庢嫙鍚?`SARIMAX(1,1,1)`锛屽苟鍔犲叆涓€澶╀腑鐨勫皬鏃讹紙涓や釜璋愭尝锛夊拰鏄熸湡鍑犵殑鍌呴噷鍙跺鐢熷彉閲忥紝鐢ㄦ潵琛ㄨ揪鏃ュ懆鏈?鍛ㄥ懆鏈熴€傝繑鍥炴俯搴?婀垮害鏈潵 10 鍒嗛挓鐨勯娴嬪€笺€?0% 棰勬祴鍖洪棿鍜岀疆淇″害锛涙牱鏈笉瓒虫垨鎷熷悎澶辫触鏃惰嚜鍔ㄥ洖閫€鍒版渶灏忎簩涔樼嚎鎬ц秼鍔匡紝骞舵槑纭繑鍥炩€滄暟鎹笉瓒斥€濓紝涓嶄細浼€犻珮缃俊搴︺€?
缃戦〉鏀寔涓ょ妯″紡锛屽彲鎵嬪姩鍒囨崲锛?
- **鍗曠偣妯″紡**锛氬皬杞︿笉鍔紝璇诲彇鏈€杩?30 鍒嗛挓 IA1 閬ユ祴锛岀敾娓╁害/婀垮害/鍏夌収鎶樼嚎鍥撅紝骞剁敤铏氱嚎鏄剧ず鏈潵 10 鍒嗛挓娓╂箍搴﹂娴嬶紱
- **鍖哄煙鍦板浘妯″紡**锛氱偣鍑烩€滃紑濮嬭矾绾库€濊灏忚溅绉诲姩閲囬泦锛岀粨鏉熷悗鐢熸垚鍖哄煙娓╁害鐑姏鍥俱€?
鑺傜偣鍦ㄧ嚎鐘舵€佹寜鏈€杩戜竴娆?MQTT 閬ユ祴鍒ゆ柇锛岃秴杩?**15 绉?*娌℃湁鏂版暟鎹氨瑙嗕负绂荤嚎锛氱绾胯妭鐐圭殑鍗＄墖鍜屾帶鍒堕潰鏉夸粛鐒朵繚鐣欙紝浣嗘暟鍊煎叏閮ㄦ竻绌轰负 `--`銆佺姸鎬佹樉绀衡€滄湭杩炴帴鈥濄€佹帶鍒舵寜閽鐢紝涓嶅啀鏄剧ず鏃ф暟鎹紱鎺ュ洖瀵瑰簲鑺傜偣鍚庤嚜鍔ㄦ仮澶嶆暟鍊笺€?
鍗曠偣鍘嗗彶鏁版嵁鎺ュ彛锛?
```text
GET /api/series?node=ia1&minutes=30&limit=1200
```

鍗曠偣棰勬祴锛?
```text
GET /api/ai?scope=single&horizon=10
```

棰勮鎸夋俯搴?婀垮害/鍏夌収鍒嗕负 `watch / warning / critical`锛屽悓涓€鎸囨爣鍚岀骇鍒?60 绉掑喎鍗达紱榛樿鍙湪缃戦〉缁欏缓璁姩浣溿€傞渶瑕?AI 棰勮鐩存帴鎺у埗椋庢墖/琛ュ厜鏃讹紝鍚姩缃戝叧鍔狅細

```powershell
D:\CodeTools\conda_envs\freshchain\python.exe server.py --mqtt-host 127.0.0.1 --mqtt-port 1884 --ai-auto-control
```

---

## 涓€銆佺數鑴戠锛氬彧鐪嬬綉椤垫紨绀猴紙涓嶉渶瑕佹澘瀛愶級

瑕佹眰 Python 3.10+锛坄server.py` 浣跨敤浜?`int | None` 绫诲瀷鍐欐硶锛夈€?
```powershell
cd D:\MyProject\bearpi\bearpi-hm_nano\freshchain\gateway
D:\CodeTools\conda_envs\freshchain\python.exe server.py --demo --reset-db
```

涔熷彲浠ョ洿鎺ュ弻鍑?`鍚姩鐪嬫澘.bat`锛屽畠宸茬粡榛樿浣跨敤杩欎釜涓撳睘鐜銆?
> 鍙屽嚮鍚庝細寮瑰嚭涓€涓爣棰樹负 **FreshChain Gateway** 鐨勭獥鍙ｏ紝杩欎釜绐楀彛瑕佷竴鐩村紑鐫€锛涘惎鍔ㄨ剼鏈湰韬殑绐楀彛涓€闂€岃繃鏄甯哥殑銆? 
> 濡傛灉 **FreshChain Gateway** 绐楀彛鏄剧ず閿欒骞跺仠浣忥紝鎸夌獥鍙ｉ噷鐨勬彁绀烘帓鏌ワ紝涓嶈鐩存帴鍏虫帀銆?
娴忚鍣ㄦ墦寮€锛?
```text
http://127.0.0.1:8080
```

婕旂ず鎿嶄綔锛?
1. 绛?2鈥? 绉掞紝IA1 娓╂箍搴?鍏夌収寮€濮嬪彉鍖栥€?2. 鐐光€滃紑椋庢墖鈥濃€滃紑琛ュ厜鈥濃€滆嚜鍔ㄦā寮忊€濄€?3. 鐐光€滃紑濮嬭繍杈撯€濓紝绾?16 绉掑悗瓒婄晫鎶ヨ銆?4. 鐐光€滄秷闊虫姤璀︹€濄€?5. 鐐光€滅粨鏉熻繍杈撯€濄€?
> 鎵嬪姩妯″紡涓嬭ˉ鍏夌伅涓嶄細鏍规嵁鍏夌収鑷姩浜紱鎸夐挳浼氶珮浜樉绀哄綋鍓嶇姸鎬併€? 
> 瑕佹仮澶嶈嚜鍔ㄦ帶鍒讹紝鐐光€滆嚜鍔ㄦā寮忊€濄€?
鍋滄锛歚Ctrl+C`銆?
---

## 浜屻€佺數鑴戠锛氭帴鐪熷疄 MQTT

1. 瀹夎渚濊禆锛?
```powershell
cd D:\MyProject\bearpi\bearpi-hm_nano\freshchain\gateway
D:\CodeTools\conda_envs\freshchain\python.exe -m pip install -r ..\requirements.txt
```

2. 鍚姩 Mosquitto锛堝眬鍩熺綉璁块棶鏃讹級銆傞」鐩噷宸茬粡鏀惧ソ閰嶇疆鍜屽惎鍔ㄨ剼鏈細

```text
freshchain\broker\mosquitto.conf
freshchain\broker\start_broker.bat
```

閰嶇疆鍐呭锛?
```conf
listener 1884 0.0.0.0
allow_anonymous true
```

瀹夎 Mosquitto 鍚庡弻鍑?`start_broker.bat`锛屾垨鎵嬪姩鎵ц锛?
```powershell
cd D:\MyProject\bearpi\bearpi-hm_nano\freshchain\broker
mosquitto -c mosquitto.conf -v
```

Windows 闃茬伀澧欓渶瑕佸厑璁?1884 鍏ョ珯銆?
> Windows 瀹夎鍖呴€氬父浼氭妸 Mosquitto 娉ㄥ唽鎴愮郴缁熸湇鍔★紝榛樿鍙洃鍚?`127.0.0.1:1883`锛屽紑鍙戞澘杩炰笉涓娿€? 
> 鏈」鐩壒鎰忎娇鐢?**1884**锛岄€氳繃 `start_broker.bat` 鍚姩椤圭洰鑷繁鐨?Broker锛涗笉瑕佺敤绯荤粺鏈嶅姟鐨?1883 绔彛銆?
3. 鍚姩缃戝叧锛?
```powershell
D:\CodeTools\conda_envs\freshchain\python.exe server.py --mqtt-host 127.0.0.1 --mqtt-port 1884 --reset-db
```

> 浠?`--demo` 鍒囨崲鍒扮湡瀹?MQTT 鏃讹紝绗竴娆′竴瀹氳鍔?`--reset-db`銆? 
> 鍚﹀垯 SQLite 浼氬姞杞戒箣鍓嶆ā鎷熷櫒鍐欏叆鐨勬棫娓╂箍搴﹀拰鍋囪建杩癸紝鐪嬭捣鏉ュ儚鈥滄病鎺ユ澘瀛愪篃鏈夋暟鎹€濄€?
4. 娴忚鍣ㄦ墦寮€ `http://127.0.0.1:8080`銆?
---

## 涓夈€佺紪璇?IA1 鍥轰欢

1. 淇敼 `applications/BearPi/BearPi-HM_Nano/sample/freshchain_ia1/freshchain_ia1_example.c` 椤堕儴锛?
```c
#define FRESHCHAIN_WIFI_SSID "浣犵殑WiFi"
#define FRESHCHAIN_WIFI_PASSWORD "浣犵殑瀵嗙爜"
#define FRESHCHAIN_MQTT_HOST "鐢佃剳鐨勫眬鍩熺綉IP"   // 渚嬪 192.168.1.100
```

2. 纭 `sample/BUILD.gn`锛?
```gn
"freshchain_ia1:freshchain_ia1",
#"freshchain_st1:freshchain_st1",
```

3. 鍦?Ubuntu 缂栬瘧鏈烘墽琛岋細

```bash
cd ~/project/bearpi-hm_nano
python build.py BearPi-HM_Nano
```

4. 浜х墿锛?
```text
out/BearPi-HM_Nano/Hi3861_wifiiot_app_allinone.bin
```

5. 澶嶅埗涓€浠界暀妗ｏ細

```text
out/BearPi-HM_Nano/ia1_allinone.bin
```

6. HiBurn 921600 鐑у綍锛屾寜 RESET銆?
---

## 鍥涖€佺紪璇?ST1 鍥轰欢

1. 淇敼 `sample/freshchain_st1/freshchain_st1_example.c` 椤堕儴鍚屾牱鐨?Wi鈥慒i/IP銆?2. 淇敼 `sample/BUILD.gn`锛?
```gn
#"freshchain_ia1:freshchain_ia1",
"freshchain_st1:freshchain_st1",
```

3. 閲嶆柊缂栬瘧锛屽鍒讹細

```text
out/BearPi-HM_Nano/st1_allinone.bin
```

4. 鐑у綍鍒扮浜屽潡鏉裤€?
> 涓ゅ潡鏉跨殑 `FRESHCHAIN_CLIENT_ID` 蹇呴』涓嶅悓锛岄粯璁ゅ凡缁忔槸 `freshchain-ia1` / `freshchain-st1`銆?
---

## 浜斻€佽仈璋冮『搴?
1. 鐢佃剳鍏堝惎鍔?Mosquitto銆?2. 鐢佃剳鍚姩 `server.py --mqtt-host 127.0.0.1`銆?3. IA1 涓婄數锛岀湅涓插彛鏃ュ織鍜岀綉椤垫槸鍚﹀嚭鐜版俯婀垮害銆?4. ST1 鎷垮埌瀹ゅ锛岀瓑 GPS 瀹氫綅銆?5. 缃戦〉鐐光€滃紑濮嬭繍杈撯€濓紝璧板嚭 80 绫筹紝鐪嬭渹楦ｅ櫒鍜屾姤璀︺€?6. 瀹ゅ唴娌℃湁 GPS 鏃讹紝ST1 鏄剧ず鈥滄悳鏄熶腑鈥濓紝涓嶈鐐光€滃紑濮嬭繍杈撯€濄€?
---

## 鍏€佽矾绾块噰闆嗕笌娓╁害鍦板浘

1. ST1 鏀惧埌瀹ゅ锛岀瓑鍒扮綉椤垫樉绀衡€淕PS宸插畾浣嶁€濓紱
2. 鎶婂皬杞︽斁鍒拌矾绾胯捣鐐癸紱
3. 缃戦〉鐐瑰嚮鈥滃紑濮嬭矾绾库€濓紱
   - 浼氬垱寤轰竴鍦堥噰闆嗚褰曪紱
   - 鍚屾椂鍚?ST1 鍙戦€佲€滃紑濮嬭繍杈撯€濓紱
4. 灏忚溅娌胯矾绾跨Щ鍔紝椤甸潰鏄剧ず鈥滈噰闆嗕腑鈥濆拰璺嚎鐐规暟锛?5. 鍥炲埌缁堢偣鍚庣偣鍑烩€滅粨鏉熻矾绾库€濓紱
6. 绛夊緟 1鈥? 绉掞紝娓╁害鍦板浘鐢熸垚锛?7. 鍦板浘涓婁細鏄剧ず锛?   - 璺嚎锛?   - GPS 閲囨牱鐐癸紱
   - 娓╁害鐑姏鍥撅紱
   - 鏈€浣?鏈€楂?骞冲潎娓╁害銆?
娉ㄦ剰锛?
- 鈥滃紑濮嬭矾绾库€濇寜閽伆鑹叉椂锛岃鏄?GPS 杩樻病瀹氫綅锛?- 鍦板浘鏈夋晥鐐瑰皯浜?3 涓椂锛屼笉鐢熸垚鐑姏鍥撅紱
- 褰撳墠鐗堟湰鍙敾娓╁害鍦板浘锛涙箍搴?鍏夌収鍦板浘鏄笅涓€闃舵锛?- 濡傛灉鍦板浘涓嶇敓鎴愶紝妫€鏌?IA1 鏄惁鍦ㄧ嚎銆乣route_points` 鏄惁鏈夋暟鎹€?
---

## 涓冦€佹敞鎰?
- 褰撳墠浠撳簱鐨?`out/` 鏄棫鐨?B2 鏋勫缓锛屽繀椤婚噸鏂扮紪璇戙€?- 缃戝叧鍛戒护宸叉敼鎴愮揣鍑?JSON锛堟棤绌烘牸锛夛紝鍚﹀垯鍥轰欢鍖归厤涓嶅埌銆?- ST1 鐨?`E53_ST1.c` 浼氭妸 GPIO4锛圲ART0_RXD锛夎涓鸿緭鍑猴紝璋冭瘯涓插彛鍙兘鎵撳嵃銆佷笉鑳芥敹锛涜繖鏄畼鏂?D13 鐨勯仐鐣欓棶棰樸€?- 鍥轰欢鐩墠娌℃湁 Flash 绂荤嚎缂撳瓨锛涙柇缃戞湡闂存暟鎹笉浼氳ˉ浼犮€?- GPS 蹇呴』瀹ゅ锛屽ぉ绾挎湞涓娿€?
---

## 鍏€佸弻鍑诲悗缃戦〉鎷掔粷杩炴帴鎬庝箞鍔?
鍏堢‘璁?**FreshChain Gateway** 绐楀彛鏄惁鐪熺殑鍦ㄨ繍琛屻€傚鏋滅獥鍙ｄ竴闂氨娌′簡锛屼紭鍏堢敤涓嬮潰鐨勬墜鍔ㄦ柟寮忕湅瀹屾暣鎶ラ敊锛?
```powershell
cd D:\MyProject\bearpi\bearpi-hm_nano\freshchain\gateway
D:\CodeTools\conda_envs\freshchain\python.exe server.py --demo --host 127.0.0.1 --port 8080
```

姝ｅ父鏃朵細鐪嬪埌锛?
```text
FreshChain gateway listening at http://127.0.0.1:8080
```

甯歌鍘熷洜锛?
1. **绔彛 8080 琚崰鐢?*  
   鎹㈢鍙ｅ惎鍔細

   ```powershell
   D:\CodeTools\conda_envs\freshchain\python.exe server.py --demo --host 127.0.0.1 --port 8081
   ```

   鐒跺悗鎵撳紑 `http://127.0.0.1:8081`銆?
2. **Python 璺緞涓嶅瓨鍦?*  
   纭杩欎釜鏂囦欢瀛樺湪锛?
   ```text
   D:\CodeTools\conda_envs\freshchain\python.exe
   ```

3. **宸ヤ綔鐩綍涓嶅**  
   蹇呴』鍦?`freshchain\gateway` 涓嬭繍琛岋紝`server.py` 浼氭寜褰撳墠鐩綍鎵?`static/`銆?
4. **鏃ц繘绋嬫病鏈夐€€鍑?*  
   鍦?PowerShell 閲屾墽琛岋細

   ```powershell
   Get-NetTCPConnection -LocalPort 8080 -State Listen
   ```

   濡傛灉鏈夎緭鍑猴紝缁撴潫瀵瑰簲 PID锛屾垨鐩存帴鎹?8081 绔彛銆?
5. **鍙屽嚮鎵瑰鐞嗙殑宓屽寮曞彿闂**  
   鏃х増 `鍚姩鐪嬫澘.bat` 浣跨敤 `cmd /k` 宓屽寮曞彿锛岄儴鍒嗘満鍣ㄤ細瑙ｆ瀽澶辫触銆傜幇鍦ㄥ凡鏀规垚锛?
   ```text
   鍚姩鐪嬫澘.bat 鈫?run_server.bat 鈫?涓撳睘 python server.py
   ```

   濡傛灉浠嶇劧闂€€锛岀洿鎺ョ敤涓婇潰鐨勬墜鍔ㄥ懡浠わ紝鑳界ǔ瀹氱湅鍒伴敊璇俊鎭€?
