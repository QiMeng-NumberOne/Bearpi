# BearPi-HM Nano 椤圭洰浠ｇ爜姊崇悊涓庝簩娆″紑鍙戞墜鍐?
> 閫傜敤浠撳簱锛歚D:\MyProject\bearpi\bearpi-hm_nano`锛圙itee `bearpi/bearpi-hm_nano` 蹇収锛?>
> 闃呰鑼冨洿锛氫互搴旂敤灞?`applications/BearPi/BearPi-HM_Nano` 鐨?30+ 涓ず渚嬨€侀┍鍔ㄣ€佸ご鏂囦欢鍜屾瀯寤鸿剼鏈负涓伙紱鍚戜笅杩芥函鍒?Hi3861 鐨?`app_main`銆丱penHarmony 鍚姩妗嗘灦銆乄iFi/GPIO/I2C/UART/ADC/PWM/Flash 鎺ュ彛銆丗lash 鍒嗗尯琛ㄥ拰閾炬帴鑴氭湰銆侽penHarmony 鍏朵綑鍐呮牳涓庢湇鍔′唬鐮佷笉閫愯灞曞紑锛屽彧璇存槑涓庢湰鏉夸笟鍔＄浉鍏崇殑鍚姩閾捐矾銆?>
> 缁撹鍏堣锛氳繖鏄?**OpenHarmony 1.0 + LiteOS-M + Hi3861 鐨?C 璇█宸ョ▼**锛屼笉鏄?DevEco/ArkTS 搴旂敤宸ョ▼锛涙墍鏈夌ず渚嬮€氳繃 `APP_FEATURE_INIT()` 娉ㄥ唽锛岀郴缁熷惎鍔ㄦ椂鑷姩鎵ц锛岀ず渚嬫湰韬病鏈?`main()`銆傚悓涓€鍥轰欢涓€娆″彧鑳藉惎鐢ㄤ竴涓ず渚嬶紝鍒囨崲绀轰緥鏀?`sample/BUILD.gn` 鍚庨噸鏂扮紪璇戙€?
---

## 鐩綍

1. [椤圭洰绠€浠嬩笌鍔熻兘鑼冨洿](#1-椤圭洰绠€浠嬩笌鍔熻兘鑼冨洿)
2. [灏忕唺娲剧‖浠惰祫婧愬崰鐢╙(#2-灏忕唺娲剧‖浠惰祫婧愬崰鐢?
3. [缂栬瘧銆佺儳褰曚笌璋冭瘯鐜](#3-缂栬瘧鐑у綍涓庤皟璇曠幆澧?
4. [鏁翠綋鏂囦欢缁撴瀯涓庢枃浠跺垎宸(#4-鏁翠綋鏂囦欢缁撴瀯涓庢枃浠跺垎宸?
5. [绋嬪簭杩愯娴佺▼](#5-绋嬪簭杩愯娴佺▼)
6. [澶栬椹卞姩娓呭崟涓庨┍鍔ㄩ€昏緫](#6-澶栬椹卞姩娓呭崟涓庨┍鍔ㄩ€昏緫)
7. [鍏抽敭鍙橀噺銆佸畯瀹氫箟涓庝腑鏂?鍥炶皟](#7-鍏抽敭鍙橀噺瀹忓畾涔変笌涓柇鍥炶皟)
8. [宸插彂鐜扮殑闂涓庝簩娆″紑鍙戦闄(#8-宸插彂鐜扮殑闂涓庝簩娆″紑鍙戦闄?
9. [棰勭暀鎺ュ彛涓庡彲鎵╁睍鐐逛綅](#9-棰勭暀鎺ュ彛涓庡彲鎵╁睍鐐逛綅)
10. [蹇€熸帓闅滄竻鍗昡(#10-蹇€熸帓闅滄竻鍗?

---

## 1. 椤圭洰绠€浠嬩笌鍔熻兘鑼冨洿

### 1.1 椤圭洰瀹氫綅

鏈粨搴撴槸 **BearPi-HM Nano锛堝皬鐔婃淳楦胯挋瀛ｏ級** 鐨勫畬鏁?OpenHarmony 1.0 婧愮爜鏍戯紝涓绘帶涓烘捣鎬?**Hi3861V100**锛圧ISC-V锛?60 MHz锛學i-Fi SoC锛夈€傚簲鐢ㄥ眰浣嶄簬锛?
```text
applications/BearPi/BearPi-HM_Nano/
鈹溾攢鈹€ docs/       鍘熺悊鍥俱€佽姱鐗囨墜鍐屻€丒53 鍘熺悊鍥俱€佽绋?PPT銆佸揩閫熶笂鎵嬫枃妗?鈹斺攢鈹€ sample/     30+ 涓彲鍒囨崲鐨勭ず渚嬪伐绋?```

`sample/BUILD.gn` 鏄€滅ず渚嬮€夋嫨鍣ㄢ€濓細鍙妸 `features` 涓湭娉ㄩ噴鐨勪竴椤圭紪杩涘浐浠躲€傚綋鍓嶆簮鐮侀粯璁ゅ惎鐢ㄧ殑鏄?**D1 Wi-Fi AP 鐑偣**锛?
```gn
"D1_iot_wifi_ap:wifi_ap"
```

鍏朵綑绀轰緥鍏ㄩ儴琚敞閲娿€?*娉ㄦ剰锛歚out/BearPi-HM_Nano/` 閲岀殑鐜版垚鍥轰欢骞朵笉鏄?D1锛岃€屾槸涓婁竴娆?B2 鎸夐敭绀轰緥鐨勬瀯寤轰骇鐗?*锛坄out/BearPi-HM_Nano/build.log:7` 缂栬瘧鐨勬槸 `B2_basic_button/button_example.o`锛宍:552` 鏄剧ず `BUILD SUCCESS`锛夈€傚洜姝ょ洿鎺ョ儳褰?`out/` 閲岀殑 `allinone.bin` 浼氬緱鍒?B2 鐨勮涓猴紝涓嶆槸褰撳墠婧愮爜閫夋嫨鐨?D1銆傜儳褰曞墠蹇呴』閲嶆柊缂栬瘧銆?
### 1.2 鍔熻兘鐭╅樀

绀轰緥鎸?A/B/C/D/Z 浜旂被缁勭粐锛岃鐩栤€滃唴鏍?鈫?鍩虹澶栬 鈫?E53 浼犳劅鍣?鈫?缃戠粶/浜戝钩鍙?鈫?寮€鍙戣€呰础鐚€濓細

| 绫诲埆 | 缂栧彿 | 鍔熻兘 | 鍏抽敭澶栬/鍗忚 |
|---|---|---|---|
| 鍐呮牳 | A1 | 绾跨▼鍒涘缓銆佹寕璧枫€佹仮澶嶃€佺粓姝€佷紭鍏堢骇 | CMSIS-RTOS2 绾跨▼ |
| 鍐呮牳 | A2 | 杞欢瀹氭椂鍣ㄥ垱寤?鍋滄/閲嶅惎/鍒犻櫎 | `osTimer*` |
| 鍐呮牳 | A3 | 浜嬩欢鏍囧織鈥滀换涓€/鍏ㄩ儴鈥濈瓑寰咃紙鎵╁睍瀹為獙锛?| `osEventFlags*` |
| 鍐呮牳 | A4 | 浜掓枼閿佷笌浼樺厛绾х户鎵?| `osMutex*` |
| 鍐呮牳 | A5 | 淇″彿閲忔紨绀轰紭鍏堢骇缈昏浆锛堟墿灞曞疄楠岋級 | `osSemaphore*` |
| 鍐呮牳 | A6 | 娑堟伅闃熷垪 | `osMessageQueue*` |
| 鍩虹 | B1 | GPIO 杈撳嚭锛孡ED 闂儊 | GPIO2 |
| 鍩虹 | B2 | 鎸夐敭涓柇鎺у埗 LED | GPIO11/12 涓嬮檷娌夸腑鏂?|
| 鍩虹 | B3 | PWM 鍛煎惛鐏?| GPIO2 澶嶇敤 PWM2 |
| 鍩虹 | B4 | ADC 璇诲彇 F1 鎸夐敭鐢靛帇 | ADC 閫氶亾 5 |
| 鍩虹 | B5 | I2C 璇诲啓鏉胯浇 NFC锛屽啓鍏ユ枃鏈?缃戝潃 | I2C1锛孨T3H1201 |
| 鍩虹 | B6 | UART1 鑷彂鑷敹 | UART1锛?600 8N1 |
| E53 | C1 | 鐑熼浘浼犳劅鍣?MQ2 + 铚傞福鍣?| ADC6銆丳WM1 |
| E53 | C2 | 娓╂箍搴?SHT30 + 鍏夌収 BH1750 + 鐢垫満/LED | I2C1銆丟PIO8/14 |
| E53 | C3 | 鍏夌収 BH1750 + LED | I2C1銆丟PIO7 |
| E53 | C4 | 鍏酱 MPU6050 + 鍙?LED | I2C1銆丟PIO7/8 |
| E53 | C5 | 浜轰綋绾㈠ + 铚傞福鍣?| GPIO7 涓婂崌娌夸腑鏂€丳WM1 |
| E53 | C6 | 鈥滄姢鑺变娇鑰呪€濆弻 E53锛氬湡澹ゆ箍搴?+ SHT30 + BH1750 + 姘存车/椋庢墖/琛ュ厜 | ADC6銆両2C0銆両2C1銆丟PIO5/8/14 |
| 鐗╄仈缃?| D1 | Wi-Fi AP 鐑偣 + DHCP + UDP 鍥炴樉 | Wi-Fi AP銆乴wIP銆丼ocket |
| 鐗╄仈缃?| D2 | Wi-Fi STA 鎵弿/杩炴帴/ DHCP | Wi-Fi STA銆乴wIP |
| 鐗╄仈缃?| D3 | UDP 瀹㈡埛绔?| Socket UDP |
| 鐗╄仈缃?| D4 | TCP 鏈嶅姟绔?| Socket TCP |
| 鐗╄仈缃?| D5 | Paho-MQTT 瀹㈡埛绔?| MQTT 3.1.1 |
| 鐗╄仈缃?| D6 | 鍗庝负 IoTDA锛圤ceanConnect锛夊睘鎬т笂鎶?鍛戒护涓嬪彂 | Paho + 鑷畾涔?profile |
| 鐗╄仈缃?| D7 | 涓浗绉诲姩 OneNET MQTT | OneNET `$dp` |
| 鐗╄仈缃?| D8 | 鏅烘収鐑熸劅锛堝崕涓轰簯锛?| E53_SF1 + IoTDA |
| 鐗╄仈缃?| D9 | 鏅烘収璺伅锛堝崕涓轰簯锛?| E53_SC1 + IoTDA |
| 鐗╄仈缃?| D10 | 鏅烘収浜曠洊锛堝崕涓轰簯锛?| E53_SC2 + IoTDA |
| 鐗╄仈缃?| D11 | 鏅烘収浜轰綋鎰熷簲锛堝崕涓轰簯锛?| E53_IS1 + IoTDA |
| 鐗╄仈缃?| D12 | 鏅烘収鍐滀笟锛堝崕涓轰簯锛?| E53_IA1 + IoTDA |
| 鐗╄仈缃?| D13 | 鏅烘収鐗╂祦 GPS锛堝崕涓轰簯锛?| E53_ST1 + UART1 |
| 寮€鍙戣€?| Z1 | Hi3861 UART1 甯﹁秴鏃舵敹鍙?| `hi_uart_*` |
| 寮€鍙戣€?| Z2 | 鍐呴儴 Flash 璇诲啓娴嬭瘯 | `FlashRead/FlashWrite` |
| 妯℃澘 | Zx | 寮€鍙戣€呰础鐚ā鏉匡紙涓嶅弬涓庢瀯寤猴紝浠ｇ爜涓嶅畬鏁达級 | 鈥?|
| 鍏ラ棬 | my_first_app | Hello World | `SYS_RUN` |

### 1.3 閲嶈浜嬪疄

- **娌℃湁 `main()`**锛氫笟鍔″叆鍙ｇ敱 `APP_FEATURE_INIT()` 鐧昏鍒?`.zinitcall.app.feature2.init` 娈碉紝绯荤粺鍚姩鍒板簲鐢ㄧ壒鎬ч樁娈垫椂缁熶竴璋冪敤锛沗my_first_app` 鐢ㄧ殑鏄洿鏃╃殑 `SYS_RUN()`銆?- **涓嶆槸鈥滀竴涓浐浠跺悓鏃惰窇 30 涓姛鑳解€?*锛氱ず渚嬩箣闂村ぇ閲忓鐢?GPIO7/8/14銆両2C1銆丄DC6銆丳WM1锛屽悓鏃跺惎鐢ㄤ細浜掔浉瑕嗙洊锛屽繀椤讳竴娆″彧閫変竴涓€?- **绀轰緥浠ｇ爜瀛樺湪鈥滄暀瀛︽敞閲?+ 鎵╁睍瀹為獙鈥濇贩鍚?*锛欰1/A2/A3/A5 宸蹭笉鏄渶鍘熷鐨勭ず渚嬶紝A3/A5 琚敼鎴愭墿灞曟紨绀猴紱C1/C2/C3 绛夐┍鍔ㄤ腑鏈変笉灏戞敞閲婁笌瀹為檯寮曡剼涓嶇锛堣绗?8 鑺傦級銆?- **涓ゅ浜戞帴鍏ユ爤**锛欴6/D7 鍦ㄧず渚嬬洰褰曞唴鑷甫 MQTT 灏佽锛汥8鈥揇13 浣跨敤 `third_party/iot_link` 鐨?`oc_mqtt_al` + `oc_mqtt_profile`銆?
---

## 2. 灏忕唺娲剧‖浠惰祫婧愬崰鐢?
### 2.1 涓绘帶瑙勬牸

| 椤圭洰 | 鍙傛暟 |
|---|---|
| 鑺墖 | Hi3861V100 / Hi3861锛孮FN-32锛? mm 脳 5 mm |
| CPU | 32 浣?RISC-V锛屾渶楂?160 MHz |
| 瀛樺偍 | SRAM 352 KB銆丷OM 288 KB銆佺墖鍐?Flash 2 MB |
| Wi-Fi | 2.4 GHz锛孖EEE 802.11 b/g/n锛孲TA + AP锛孉P 鏈€澶?6 涓?STA |
| GPIO | 15 涓紙GPIO0鈥揋PIO14锛?|
| ADC | 7 璺紙閫氶亾 0鈥? 鍙敤锛岄€氶亾 7 涓鸿竟鐣岋級 |
| PWM | 6 璺紙PWM0鈥揚WM5锛?|
| I2C | 2 璺紙I2C0/I2C1锛?|
| UART | 3 璺紙UART0/UART1/UART2锛?|
| SPI | 2 璺紙SPI0/SPI1锛?|
| 鍏朵粬 | 1 璺?SDIO銆? 璺?I2S銆佸唴缃?PA/LNA |
| 渚涚數 | 2.3鈥?.6 V锛汭O 鏀寔 1.8 V/3.3 V |

鏉ユ簮锛歚applications/BearPi/BearPi-HM_Nano/docs/quick-start/BearPi-HM_Nano寮€鍙戞澘浠嬬粛.md:44-56`锛屼互鍙婃牴鐩綍 `README.md:17-24`銆?
### 2.2 鏉胯浇璧勬簮

| 璧勬簮 | 璇存槑 | 浠ｇ爜涓殑浣跨敤 |
|---|---|---|
| 绾㈣壊 LED | 鎺?GPIO2锛岄珮鐢靛钩鐐逛寒 | B1/B2/B3 |
| 鐢ㄦ埛鎸夐敭 F1 | 鎺?GPIO11锛屽閮ㄤ笂鎷夛紝鎸変笅鎺ュ湴锛屼笅闄嶆部 | B2锛汢4 鐢?ADC5 璇诲叾鐢靛帇 |
| 鐢ㄦ埛鎸夐敭 F2 | 鎺?GPIO12锛屽閮ㄤ笂鎷夛紝鎸変笅鎺ュ湴锛屼笅闄嶆部 | B2 |
| NFC | NT3H1201锛?K锛塈2C 鏍囩 + 鏉胯浇澶╃嚎锛? 浣嶅湴鍧€ 0x55 | B5 |
| E53 鎺ュ彛 | 鏍囧噯 10/20 pin 鎵╁睍鍙ｏ紝鍚?I2C銆乁ART銆丟PIO銆丄DC銆?.3 V/5 V | C1鈥揅6銆丏8鈥揇13 |
| USB | Type-C锛孋H340 USB 杞覆鍙ｏ紝鐢ㄤ簬渚涚數/鐑у綍/璋冭瘯 | 鍏ㄩ儴 |
| 澶嶄綅閿?| RESET锛岀儳褰曟椂鎸変竴涓嬭繘鍏ヤ笅杞?| 鐑у綍 |
| Wi-Fi | Hi3861 鍐呯疆 | D1鈥揇13 |

### 2.3 GPIO/澶栬鍗犵敤鎬昏〃

涓嬭〃鏄€滀唬鐮佷腑瀹為檯鍑虹幇鈥濈殑鍗犵敤锛屼笉鏄師鐞嗗浘鍏ㄩ噺寮曡剼琛紱鏈垪鍑虹殑 GPIO 涓嶄竴瀹氬紩鍑哄埌鎺掗拡銆?
| 鍔熻兘 | 寮曡剼/閫氶亾 | 澶嶇敤/鏂瑰悜 | 浣跨敤绀轰緥 | 璇存槑 |
|---|---|---|---|---|
| 鏉胯浇 LED | GPIO2 | GPIO 杈撳嚭锛汢3 澶嶇敤 PWM2 | B1銆丅2銆丅3 | 楂樼數骞崇偣浜?|
| F1 鎸夐敭 | GPIO11 | GPIO 杈撳叆锛屼笂鎷夛紝涓嬮檷娌夸腑鏂?| B2 | 鍚屾椂鏄?ADC 閫氶亾 5 |
| F2 鎸夐敭 | GPIO12 | GPIO 杈撳叆锛屼笂鎷夛紝涓嬮檷娌夸腑鏂?| B2 | 鈥?|
| NFC NT3H | GPIO0 = I2C1_SDA锛孏PIO1 = I2C1_SCL | I2C1锛?00 kbps | B5 | 7 浣嶅湴鍧€ 0x55 |
| E53 LED_SW | GPIO7 | GPIO 杈撳嚭 | C3銆丆4銆丏9銆丏10 | SC1 鐏?/ SC2 D1 |
| E53 INT | GPIO7 | GPIO 杈撳叆锛屼笂鎷夛紝涓婂崌娌夸腑鏂?| C5銆丏11 | 浜轰綋绾㈠杈撳嚭 |
| E53 Motor_SW/铚傞福鍣?| GPIO8 | GPIO 杈撳嚭鎴?PWM1 | C1銆丆2銆丆5銆丆6銆丏8銆丏10銆丏11銆丏12銆丏13 | 铚傞福鍣?鐢垫満/SC2 D2 |
| E53 LED锛堣ˉ鍏夛級 | GPIO14 | GPIO 杈撳嚭 | C2銆丆6銆丏12 | 楂樼數骞崇偣浜?|
| E53 ADC6 | ADC 閫氶亾 6 | 妯℃嫙杈撳叆 | C1銆丆6銆丏8 | MQ2 / 鍦熷￥婀垮害 |
| E53 ADC2 | ADC 閫氶亾 2 | 妯℃嫙杈撳叆 | 鏈娇鐢?| 棰勭暀 |
| E53 UART | GPIO5 = UART1_RXD锛孏PIO6 = UART1_TXD | UART1 | B6銆丏13銆乑1 | 9600 鎴?115200 |
| I2C0 | GPIO9 = I2C0_SCL锛孏PIO10 = I2C0_SDA | I2C0锛?00 kbps | C6 | 鑺卞尃 SHT30 |
| 鎶芥按鐢垫満 | GPIO5 | GPIO 杈撳嚭锛屼綆鐢靛钩鏈夋晥 | C6 | 涓?UART1_RXD 鍐茬獊 |
| 璋冭瘯涓插彛 | GPIO3 = UART0_TXD锛孏PIO4 = UART0_RXD | UART0锛?15200 8N1 | 鎵€鏈夌ず渚嬬殑 `printf` | D13 鎶?GPIO4 璁炬垚鏅€氳緭鍑?|
| 绌洪棽 GPIO | GPIO13 | 鈥?| 鏈娇鐢?| 鑺墖渚у敮涓€瀹屽叏鏈崰鐢?|
| SPI | SPI0/SPI1 | 鈥?| 鏈娇鐢?| SDK 鍙寜闇€鍒濆鍖?|
| I2S/SDIO | 鈥?| 鈥?| 鏈娇鐢?| 鈥?|
| PWM0/3/4/5 | 鍙槧灏勫埌 GPIO7/9銆丟PIO0/12銆丟PIO1銆丟PIO14 | 鈥?| 鏈娇鐢?| 闇€瑕佹敼寮曡剼澶嶇敤 |

鍏抽敭澶嶇敤鏋氫妇鏉ヨ嚜 `base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_gpio_ex.h`锛?
- GPIO0 鍙綔 `UART1_TXD`銆乣SPI1_CK`銆乣PWM3_OUT`銆乣I2C1_SDA` 绛夛紱
- GPIO1 鍙綔 `UART1_RXD`銆乣SPI1_RXD`銆乣PWM4_OUT`銆乣I2C1_SCL` 绛夛紱
- GPIO2 鍙綔 `UART1_RTS_N`銆乣SPI1_TXD`銆乣PWM2_OUT` 绛夛紱
- GPIO5 鍙綔 `UART1_RXD`銆乣SPI0_CSN`銆乣PWM2_OUT`銆乣I2S0_MCLK` 绛夛紱
- GPIO8 鍙綔 `UART1_RTS_N`銆乣SPI0_TXD`銆乣PWM1_OUT`銆乣I2S0_WS` 绛夛紱
- GPIO9/10 鍙綔 I2C0銆丼PI0銆丼DIO銆両2S0 绛夛紱
- GPIO14 鍙綔 `UART0_RXD`銆乣PWM5_OUT`銆乣I2C0_SCL` 绛夈€?
> 缁撹锛?*GPIO2/7/8/14 鏄澘杞戒笌 E53 鐨勨€滈粍閲戝紩鑴氣€?*锛屽嚑涔庢墍鏈夋渚嬮兘鍦ㄨ繖鍥涙牴绾夸笂鍋氭枃绔狅紱GPIO0/1 鏄?I2C1 鍥哄畾鎼厤锛汫PIO11/12 琚寜閿崰鐢ㄣ€備簩娆″紑鍙戦€夊紩鑴氭椂锛屽厛鏌ヨ繖寮犺〃锛屽啀鏌?`wifiiot_gpio_ex.h` 鐨勫鐢ㄦ灇涓俱€?
### 2.4 E53 鎺ュ彛寮曡剼

E53 鏍囧噯鎺ュ彛锛堜互 `docs/quick-start/BearPi-HM_Nano 鎶よ姳浣胯€呮渚嬫暀绋嬶紙鍙屾墿灞曟澘闆嗘垚鏂瑰紡锛?md:25-35` 鍜?`B6_basic_uart/README.md:58-62` 涓哄噯锛夛細

| E53 寮曡剼 | 鍚嶇О | 鏂瑰悜 | 鏉夸笂瀵瑰簲 |
|---|---|---|---|
| 1 | LED_SW | OUT | GPIO7 |
| 2 | INT | OUT | GPIO7锛堣緭鍏ワ級 |
| 3 | Motor_SW | OUT | GPIO8 |
| 4 | IIC_SCL | OUT/IN | GPIO1锛圛2C1_SCL锛?|
| 5 | IIC_SDA | OUT/IN | GPIO0锛圛2C1_SDA锛?|
| 6 | GND | PWR | GND |
| 7 | V3.3 | PWR | 3.3 V |
| 8 | GND | PWR | GND |
| 9 | V5.0 | PWR | 5 V |
| 18 | UART_TXD | OUT | GPIO6锛圲ART1_TXD锛?|
| 19 | UART_RXD | IN | GPIO5锛圲ART1_RXD锛?|
| 鍏朵粬 | ADC6 / ADC2 | 妯℃嫙 | ADC 閫氶亾 6 / 2 |

> 娉ㄦ剰锛欵53 鐨?UART 涓庘€滆姳鍖犫€濈殑鎶芥按鐢垫満閮借惤鍦?GPIO5锛沗C6` 鎶?GPIO5 閰嶆垚鏅€氳緭鍑哄悗锛孶ART1 鐨?RX 灏卞け鏁堜簡銆傝繖鏄弻鎵╁睍鏉块泦鎴愮殑鍏稿瀷鍐茬獊鐐广€?
### 2.5 璧勬簮鍐茬獊鐭╅樀锛堥噸鐐癸級

| 鍐茬獊 | 娑夊強绀轰緥 | 璇存槑 |
|---|---|---|
| GPIO2锛歀ED vs PWM2 | B1/B2 vs B3 | 鍚屼竴鏍瑰紩鑴氾紝鍔熻兘涓嶅悓锛屼笉鑳藉悓鏃剁敤 |
| GPIO7锛歀ED 杈撳嚭 vs 绾㈠杈撳叆 | C3/C4/D9/D10 vs C5/D11 | 鏂瑰悜鐩稿弽锛屼笉鑳藉悓鏃剁敤 |
| GPIO8锛氳渹楦ｅ櫒 PWM vs 鐢垫満/LED | C1/C5/D8/D11/D13 vs C2/C4/C6/D10/D12 | 鍚屼竴寮曡剼涓嶅悓鎵ц鍣?|
| GPIO14锛氳ˉ鍏夌伅 / PWM5 / UART0_RXD 澶嶇敤 | C2/C6/D12 | 褰撳墠 UART0 榛樿鍦?GPIO4锛孏PIO14 浠呭湪琚噸鏄犲皠鏃舵墠涓庤皟璇曚覆鍙ｅ啿绐侊紱鍋氳ˉ鍏夌伅鏃朵笉瑕佸啀鎶?GPIO14 鍒囧埌 UART0 |
| GPIO5锛氭娊姘寸數鏈?vs UART1_RXD | C6 vs B6/D13/Z1 | C6 鎶?GPIO5 鎷夋垚杈撳嚭锛孶ART1 鏀朵笉鍒版暟鎹?|
| GPIO4锛歎ART0_RXD vs D13 杈撳嚭 | 鎵€鏈夎皟璇曚覆鍙?vs D13 | D13 鎶?GPIO4 璁句负鏅€氳緭鍑哄苟鎷変綆锛岃皟璇曚覆鍙ｂ€滆兘鎵撳嵃浣嗕笉鑳芥敹鈥?|
| I2C1锛歂FC vs E53 浼犳劅鍣?| B5 vs C2/C3/C4/C6/D6/D7/D8鈥揇13 | 鍚屼竴鏉?I2C1 鎬荤嚎锛屽湴鍧€涓嶅悓鍙互鍏卞瓨锛屼絾涓嶈鍚屾椂鍒濆鍖栨垚涓嶅悓閫熺巼/妯″紡 |
| ADC6锛歁Q2 vs 鍦熷￥ | C1/D8 vs C6 | 鍚屼竴閫氶亾锛屾帴涓嶅悓鎵╁睍鏉?|
| UART1锛欸PS vs AT 鍛戒护鍙?| D13 vs 绯荤粺 `peripheral_init` | 绯荤粺鍚姩鏃跺厛鎶?UART1 鍒濆鍖栦负 115200 鐨?AT 鍙ｏ紝D13 鍐嶆敼鎴?9600 |

### 2.6 Flash 鍒嗗尯锛? MB锛?
榛樿鍒嗗尯琛ㄥ湪 `vendor/hisi/hi3861/hi3861/platform/system/partition_table/flash_partition_table.c:25-52`銆傚鏋滃伐鍘?NV 鍖洪噷瀛樹簡鍒嗗尯琛紝鍒欎互宸ュ巶琛ㄤ负鍑嗭紱涓嬮潰鏄粯璁ゅ€硷細

| 鍒嗗尯 | 璧峰鍦板潃 | 澶у皬 | 鐢ㄩ€?|
|---|---:|---:|---|
| BOOT | 0x000000 | 0x8000锛?2 KB锛?| Boot |
| FACTORY_NV | 0x008000 | 0x2000锛? KB锛?| 宸ュ巶 NV |
| NORMAL_NV | 0x00A000 | 0x2000锛? KB锛?| 鏅€?NV |
| NORMAL_NV_BACKUP | 0x00C000 | 0x1000锛? KB锛?| NV 澶囦唤 |
| KERNEL_A | 0x00D000 | 0xE4000锛?12 KB锛?| 鍐呮牳 A |
| KERNEL_B | 0x0F1000 | 0xF2000锛?68 KB锛?| 鍐呮牳 B |
| HILINK | 0x1E3000 | 0x2000锛? KB锛?| HiLink |
| FILE_SYSTEM | 0x1E5000 | 0xB000锛?4 KB锛?| 鏂囦欢绯荤粺 |
| USER_RESERVE | 0x1F0000 | 0x5000锛?0 KB锛?| 鐢ㄦ埛淇濈暀 |
| HILINK_PKI | 0x1F5000 | 0x2000锛? KB锛?| HiLink PKI |
| CRASH_INFO | 0x1F7000 | 0x1000锛? KB锛?| 姝绘満淇℃伅 |
| BOOT_BACK | 0x1F8000 | 0x8000锛?2 KB锛?| Boot 澶囦唤 |

`Z2_hi3861_flash_ylc` 鐨勫啓娉曟槸锛?
```c
FlashWrite(addr - 0x400000, len, buf, 1);
```

`FlashRead/FlashWrite` 鐨勭涓€涓弬鏁版槸 **flashOffset**锛屼笉鏄?CPU 鍦板潃锛坄wifiiot_flash.h:49-74`锛夈€俍2 鎶?`0x600000` 褰撲綔鈥淐PU 鍦板潃鈥濓紝鍑忓幓 `0x400000` 鍚庡緱鍒?`0x200000` 闄勮繎鐨勫亸绉伙紱`0x600000-200` 鏈€缁堣惤鍦?`0x1FFF38`锛屽凡缁忓湪 **BOOT_BACK** 鍒嗗尯鍐呫€傝繖鏍蜂細鐮村潖 boot 澶囦唤锛屼簩娆″紑鍙戜笉瑕佺収鎶勮繖涓湴鍧€锛屽缓璁敼鐢?`USER_RESERVE`锛?x1F0000锛?0 KB锛夊苟鑷繁鍋氱（鎹?鏍￠獙銆?
---

## 3. 缂栬瘧銆佺儳褰曚笌璋冭瘯鐜

### 3.1 寮€鍙戣蒋浠朵笌宸ュ叿閾?
| 鐜妭 | 宸ュ叿/鐗堟湰 | 璇存槑 |
|---|---|---|
| 缂栬緫 | VS Code | Windows 绔啓浠ｇ爜锛屽彲閫氳繃 SFTP/Samba 鍚屾鍒?Ubuntu |
| 缂栬瘧涓绘満 | Ubuntu 16.04 鍙婁互涓?64 浣嶏紝bash | OpenHarmony 1.0 鐨?GN/Ninja 鏋勫缓 |
| 浜ゅ弶缂栬瘧鍣?| `gcc_riscv32` 7.3.0 | Hi3861 鏄?RISC-V锛涗粎鏀寔闈欐€侀摼鎺?libgcc |
| 鏋勫缓宸ュ叿 | Python 3.7+锛堟帹鑽?3.8.5锛夈€丼Cons 3.0.4+銆丟N銆丯inja | `python build.py` 浼氳皟鐢?GN/Ninja/SCons |
| Python 鍖?| kconfiglib 13.2+銆乸ycryptodome銆乻ix銆乪cdsa | 闀滃儚绛惧悕銆侀厤缃?|
| 涓插彛 | CH340/CH341SER 椹卞姩銆丮obaXterm/PuTTY | 璋冭瘯涓插彛 UART0锛?15200 8N1 |
| 鐑у綍 | HiBurn锛圵indows锛?| 涓插彛 921600锛孉uto burn |
| 鎶撳寘/缃戠粶璋冭瘯 | 缃戠粶璋冭瘯鍔╂墜銆丮QTT.fx 绛?| D1鈥揇5 楠岃瘉 |

### 3.2 鑺墖鍨嬪彿涓庝骇鍝侀厤缃?
- 鑺墖锛?*Hi3861V100**锛圚i3861 绯诲垪锛夈€?- 浜у搧閰嶇疆锛歚build/lite/product/BearPi-HM_Nano.json:2-5`锛?  - `board: hi3861v100`
  - `kernel: liteos_riscv`
  - `compiler: gcc`
- 骞冲彴閰嶇疆锛歚build/lite/platform/hi3861v100_liteos_riscv/platform.json`銆?- 搴旂敤缁勪欢锛歚//applications/BearPi/BearPi-HM_Nano/sample:app`锛坄BearPi-HM_Nano.json:10`锛夈€?
### 3.3 缂栬瘧鍛戒护

鍦ㄤ粨搴撴牴鐩綍鎵ц锛?
```bash
python build.py BearPi-HM_Nano
```

鎴愬姛鏃舵棩蹇楀嚭鐜?`BUILD SUCCESS`銆備骇鐗╃洰褰曪細

```text
out/BearPi-HM_Nano/
鈹溾攢鈹€ Hi3861_wifiiot_app_allinone.bin   鈫?HiBurn 閫夎繖涓?鈹溾攢鈹€ Hi3861_wifiiot_app_burn.bin
鈹溾攢鈹€ Hi3861_wifiiot_app_ota.bin
鈹溾攢鈹€ Hi3861_wifiiot_app_vercfg.bin
鈹溾攢鈹€ Hi3861_boot_signed.bin
鈹溾攢鈹€ Hi3861_boot_signed_B.bin
鈹溾攢鈹€ Hi3861_loader_signed.bin
鈹溾攢鈹€ Hi3861_wifiiot_app.map             鈫?绗﹀彿/娈靛ぇ灏忓垎鏋?鈹溾攢鈹€ Hi3861_wifiiot_app.asm             鈫?鍙嶆眹缂?鈹斺攢鈹€ build.log
```

鏋勫缓閾捐矾锛?
```text
build.py
  鈫?build/lite/build.py
    鈫?璇诲彇 product JSON / platform JSON
    鈫?GN 鐢熸垚 build.ninja
    鈫?Ninja 缂栬瘧 OpenHarmony 鍚勫瓙绯荤粺
    鈫?SCons 缂栬瘧 Hi3861 SDK / 閾炬帴 / 绛惧悕
    鈫?鐢熸垚 allinone.bin
```

绀轰緥鐨勯摼鎺ヤ緷璧栵細

| 绀轰緥 | 棰濆渚濊禆 |
|---|---|
| A/B/C 绯诲垪 | 浠?CMSIS-RTOS2 + `wifiiot_lite` 澶栬鎺ュ彛锛圔5 棰濆甯?NFC 婧愭枃浠讹級 |
| D1鈥揇4 | lwIP/Socket锛坄lwip_sack`锛?|
| D5/D6/D7 | `//third_party/paho_mqtt:pahomqtt_static` + cJSON |
| D8鈥揇13 | `//third_party/iot_link:iot_link`锛堝唴閮ㄥ啀渚濊禆 paho/mqtt_al/dtls_al/queue锛?|

### 3.4 鐑у綍姝ラ锛圚iBurn锛?
1. Type-C 杩炴帴寮€鍙戞澘锛屽畨瑁?CH340 椹卞姩锛岀‘璁?Windows 璁惧绠＄悊鍣ㄥ嚭鐜?COM 鍙ｃ€?2. 鎵撳紑 HiBurn锛宍Refresh`锛岄€夋嫨 COM 鍙ｃ€?3. `Setting 鈫?Com settings`锛屾尝鐗圭巼璁句负 **921600**銆?4. `Select file` 閫夋嫨 `out/BearPi-HM_Nano/Hi3861_wifiiot_app_allinone.bin`銆?5. 鍕鹃€?`Auto burn`锛岀偣鍑?`Connect`銆?6. 鎸変竴涓嬪紑鍙戞澘 `RESET`锛岀瓑寰呬笅杞姐€?7. 鍑虹幇 `Execution Successful` 鍚庣偣鍑?`Disconnect`銆?8. 鐢?MobaXterm/PuTTY 鎵撳紑鍚屼竴 COM 鍙ｏ紝**115200 8N1** 鏌ョ湅鏃ュ織銆?
> 鐑у綍鍓嶅姟蹇呯‘璁?`out/` 鏄渶鏂版瀯寤恒€傚綋鍓嶄粨搴撶殑 `out/` 鏄?B2 鐨勬棫浜х墿锛岃 1.1 鑺傘€?
### 3.5 璋冭瘯鎵嬫

| 鎵嬫 | 鐢ㄩ€?|
|---|---|
| UART0 `printf` | 涓昏皟璇曢€氶亾锛?15200锛涙墍鏈夌ず渚嬬殑鏃ュ織閮戒粠杩欓噷杈撳嚭 |
| `out/.../Hi3861_wifiiot_app.map` | 鏌ョ鍙峰湴鍧€銆佹澶у皬銆佸簱閾炬帴鎯呭喌 |
| `out/.../Hi3861_wifiiot_app.asm` | 鍙嶆眹缂栧畾浣嶅紓甯?PC |
| `out/.../build.log` | 鏌ョ紪璇?閾炬帴/绛惧悕杩囩▼锛岀‘璁ゅ疄闄呭弬涓庣紪璇戠殑绀轰緥 |
| `hi_shell` / AT | 榛樿鏈惎鐢紱鍚敤鍚庝笌 UART1 澶嶇敤锛屾敞鎰忓啿绐?|
| 閫昏緫鍒嗘瀽浠?绀烘尝鍣?| 娴?PWM銆両2C銆乁ART 娉㈠舰 |
| 涓囩敤琛?| 娴?E53 3.3 V/5 V銆丄DC 鐢靛帇 |

---

## 4. 鏁翠綋鏂囦欢缁撴瀯涓庢枃浠跺垎宸?
### 4.1 椤跺眰鐩綍

```text
bearpi-hm_nano/
鈹溾攢鈹€ applications/                 # 搴旂敤灞傦紝BearPi 绀轰緥閮藉湪杩欓噷
鈹?  鈹斺攢鈹€ BearPi/BearPi-HM_Nano/
鈹?      鈹溾攢鈹€ docs/                 # 鍘熺悊鍥俱€佽姱鐗囨墜鍐屻€丒53 鍘熺悊鍥俱€丳PT銆佸揩閫熶笂鎵?鈹?      鈹斺攢鈹€ sample/               # 30+ 涓ず渚?+ BUILD.gn 閫夋嫨鍣?鈹溾攢鈹€ base/                         # OpenHarmony 鍩虹瀛愮郴缁?鈹?  鈹溾攢鈹€ startup/                  # 鍚姩妗嗘灦锛欻OS_SystemInit銆乥ootstrap銆乻yspara
鈹?  鈹溾攢鈹€ iot_hardware/             # wifiiot_lite 澶栬鎺ュ彛锛圙PIO/I2C/UART/ADC/PWM/Flash锛?鈹?  鈹溾攢鈹€ hiviewdfx/                # hilog/hievent
鈹?  鈹溾攢鈹€ security/                 # hichainsdk銆乤pp_verify銆乧rypto
鈹?  鈹斺攢鈹€ global/                   # resmgr_lite
鈹溾攢鈹€ foundation/                   # 绯荤粺鏈嶅姟
鈹?  鈹溾攢鈹€ communication/            # wifi_lite銆乻oftbus_lite
鈹?  鈹斺攢鈹€ distributedschedule/      # samgr_lite
鈹溾攢鈹€ kernel/liteos_m/              # LiteOS-M 鍐呮牳 + CMSIS-RTOS2 閫傞厤
鈹溾攢鈹€ third_party/                  # paho_mqtt銆乧JSON銆乮ot_link銆乴wIP銆乵bedtls銆乵usl 绛?鈹溾攢鈹€ utils/native/lite/            # kv_store銆乫ile銆乷hos_init.h
鈹溾攢鈹€ vendor/hisi/hi3861/           # Hi3861 SDK锛歜oot銆侀┍鍔ㄣ€乄i-Fi銆佸垎鍖恒€侀摼鎺ヨ剼鏈?鈹溾攢鈹€ build/lite/                   # GN/Ninja 鏋勫缓妗嗘灦銆乸roduct/platform JSON
鈹斺攢鈹€ out/BearPi-HM_Nano/           # 鏋勫缓浜х墿锛堝綋鍓嶄负鏃?B2 鏋勫缓锛?```

### 4.2 搴旂敤灞傜洰褰?
```text
applications/BearPi/BearPi-HM_Nano/sample/
鈹溾攢鈹€ BUILD.gn                      # 鈽?绀轰緥閫夋嫨鍣細涓€娆″彧鍙栨秷娉ㄩ噴涓€涓?鈹溾攢鈹€ README.md                     # 绀轰緥鎬昏〃
鈹溾攢鈹€ A1_kernal_thread/             # thread_example.c + BUILD.gn + README
鈹溾攢鈹€ A2_kernel_timer/
鈹溾攢鈹€ A3_kernel_event/
鈹溾攢鈹€ A4_kernel_mutex/
鈹溾攢鈹€ A5_kernel_semaphore/
鈹溾攢鈹€ A6_kernel_message/
鈹溾攢鈹€ B1_basic_led_blink/
鈹溾攢鈹€ B2_basic_button/
鈹溾攢鈹€ B3_basic_pwm_led/
鈹溾攢鈹€ B4_basic_adc/
鈹溾攢鈹€ B5_basic_i2c_nfc/             # i2c_example.c + nfc/ 椹卞姩搴?鈹溾攢鈹€ B6_basic_uart/
鈹溾攢鈹€ C1_e53_sf1_mq2/               # src/E53_SF1.c + include/E53_SF1.h + example
鈹溾攢鈹€ C2_e53_ia1_temp_humi_pls/
鈹溾攢鈹€ C3_e53_sc1_pls/
鈹溾攢鈹€ C4_e53_sc2_axis/
鈹溾攢鈹€ C5_e53_is1_infrared/
鈹溾攢鈹€ C6_e53_flower_ia1/            # src/flower.c + include/flower.h + example
鈹溾攢鈹€ D1_iot_wifi_ap/
...
鈹溾攢鈹€ D13_iot_cloud_oc_gps/         # src/E53_ST1.c + include/E53_ST1.h + example
鈹溾攢鈹€ Z1_hi3861_uart_ylc/
鈹溾攢鈹€ Z2_hi3861_flash_ylc/
鈹溾攢鈹€ Zx_Developer/                 # 妯℃澘锛屼笉鍙備笌鏋勫缓
鈹斺攢鈹€ my_first_app/                 # Hello World
```

### 4.3 姣忎釜 `.c/.h` 鐨勮亴璐?
#### A 绯诲垪锛堝唴鏍革級

| 鏂囦欢 | 鑱岃矗 | 鍏ュ彛/鍏抽敭鐐?|
|---|---|---|
| [thread_example.c](applications/BearPi/BearPi-HM_Nano/sample/A1_kernal_thread/thread_example.c) | 绾跨▼鍒涘缓銆佹寕璧枫€佹仮澶嶃€佺粓姝?| `threadHi` 浼樺厛绾?25锛宍threadLo` 24锛沗APP_FEATURE_INIT(Thread_example)` |
| [Timer_example.c](applications/BearPi/BearPi-HM_Nano/sample/A2_kernel_timer/Timer_example.c) | 涓や釜鍛ㄦ湡杞欢瀹氭椂鍣紝鍚仠姝?閲嶅惎/鍒犻櫎鎵╁睍 | `Timer1_Callback` 100 tick锛宍Timer2_Callback` 300 tick |
| [Event_example.c](applications/BearPi/BearPi-HM_Nano/sample/A3_kernel_event/Event_example.c) | 浜嬩欢鏍囧織鈥滀换涓€/鍏ㄩ儴鈥濇墿灞曟紨绀?| 4 涓嚎绋嬶紝`evtAny`/`evtAll`锛宐it0/bit1 |
| [Mutex_example.c](applications/BearPi/BearPi-HM_Nano/sample/A4_kernel_mutex/Mutex_example.c) | 浜掓枼閿?+ 浼樺厛绾х户鎵?| 楂?涓?浣庝紭鍏堢骇 26/25/24锛宍mutex_id` |
| [Semaphore_example.c](applications/BearPi/BearPi-HM_Nano/sample/A5_kernel_semaphore/Semaphore_example.c) | 淇″彿閲?+ 浼樺厛绾х炕杞紨绀?| `sem1` 鏈€澶?1 鍒濆 1锛涗綆 24銆佷腑 26銆侀珮 27 |
| [Message_example.c](applications/BearPi/BearPi-HM_Nano/sample/A6_kernel_message/Message_example.c) | 娑堟伅闃熷垪锛屼紶閫掔粨鏋勪綋 | 16 涓秷鎭紝`MSGQUEUE_OBJ_t`锛屼袱涓嚎绋?|
| `BUILD.gn` | 缂栬瘧涓?`libthread_example.a` 绛?| 姣忎釜鐩綍涓€涓?`static_library` |

#### B 绯诲垪锛堝熀纭€澶栬锛?
| 鏂囦欢 | 鑱岃矗 | 鍏抽敭鐐?|
|---|---|---|
| [led_example.c](applications/BearPi/BearPi-HM_Nano/sample/B1_basic_led_blink/led_example.c) | GPIO2 杈撳嚭闂儊 | 1 s 楂?1 s 浣庯紱绾跨▼鏍?512 |
| [button_example.c](applications/BearPi/BearPi-HM_Nano/sample/B2_basic_button/button_example.c) | GPIO11/12 涓嬮檷娌夸腑鏂帶鍒?LED | `F1_Pressed` 鐐逛寒锛宍F2_Pressed` 鐔勭伃 |
| [pwm_example.c](applications/BearPi/BearPi-HM_Nano/sample/B3_basic_pwm_led/pwm_example.c) | GPIO2 澶嶇敤 PWM2锛屽崰绌烘瘮 0鈫?00% | `PwmStart(PWM2, i, 40000)`锛屾瘡妗?1 s |
| [adc_example.c](applications/BearPi/BearPi-HM_Nano/sample/B4_basic_adc/adc_example.c) | ADC5 璇?F1 鐢靛帇 | `data * 1.8 * 4 / 4096`锛? 娆″钩鍧?|
| [i2c_example.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/i2c_example.c) | I2C1 鍒濆鍖?+ 鍐?NFC 鏂囨湰/缃戝潃 | `storeText`銆乣storeUrihttp` |
| [B5 nfc/NT3H.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/NT3H.c) | NT3H 搴曞眰 I2C 璇诲啓銆侀〉璇诲啓銆佸ご/閰嶇疆/ SRAM | `readTimeout`/`writeTimeout`锛屽啓鍚?300 ms 寤舵椂 |
| [B5 nfc/NT3H.h](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/NT3H.h) | NT3H 鍦板潃/椤?閿欒鐮?NDEF 鏁版嵁缁撴瀯 | 0x55锛沗NFC_PAGE_SIZE=16`锛沗RecordPosEnu` |
| [B5 nfc/nfc.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/nfc.c) | 涓婂眰 API锛歚storeText`銆乣storeUrihttp` | 缁勮 `NDEFDataStr` 鍚庤皟 `NT3HwriteRecord` |
| [B5 nfc/ndef/ndef.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/ndef.c) | NDEF 璁板綍鍐欏叆锛氶鏉?杩藉姞/涓棿/鏈潯 | `firstRecord`銆乣addRecord`銆乣writeUserPayload` |
| [B5 nfc/ndef/ndef.h](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/ndef.h) | `NT3HwriteRecord` 澹版槑 | 鈥?|
| [B5 nfc/ndef/rtd/nfcForum.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/nfcForum.c) | NDEF 璁板綍澶?Text/URI 璐熻浇缂栫爜 | `composeRtdText`銆乣composeRtdUri`銆丮B/ME 浣?|
| [B5 nfc/ndef/rtd/nfcForum.h](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/nfcForum.h) | NDEF 澶?璁板綍缁撴瀯銆佷綅鎺╃爜 | `NDEF_START_BYTE=0x03`锛宍NDEF_END_BYTE=0xFE` |
| [B5 nfc/ndef/rtd/rtdText.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/rtdText.c) | Text RTD 鍑嗗锛坋n 璇█锛?| `prepareText` |
| [B5 nfc/ndef/rtd/rtdText.h](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/rtdText.h) | Text RTD 绫诲瀷 | `RtdTextTypeStr` |
| [B5 nfc/ndef/rtd/rtdUri.c](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/rtdUri.c) | URI RTD 鍑嗗锛坔ttp://www.锛?| `prepareUrihttp` |
| [B5 nfc/ndef/rtd/rtdUri.h](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/rtdUri.h) | URI 鍓嶇紑鏋氫妇/缁撴瀯 | `UriTypeE` |
| [B5 nfc/ndef/rtd/rtdTypes.h](applications/BearPi/BearPi-HM_Nano/sample/B5_basic_i2c_nfc/nfc/ndef/rtd/rtdTypes.h) | Text/URI 鑱斿悎绫诲瀷 | `RTD_TEXT='T'`锛宍RTD_URI='U'` |
| [uart_example.c](applications/BearPi/BearPi-HM_Nano/sample/B6_basic_uart/uart_example.c) | UART1 鑷彂鑷敹 | 9600 8N1锛汿X/RX 鐭帴锛? s 涓€娆?|

> B5 鐨?`BUILD.gn` 瀹為檯寮曠敤鐨勬槸 `nfc/ndef/...`锛屼笉鏄?`nfc/def/...`锛涙煇浜涙枃浠舵祻瑙堝櫒/宸ュ叿浼氭妸涓棿鐩綍鏄剧ず鎴?`def`锛屼互 `BUILD.gn:16-22` 涓哄噯銆?
#### C 绯诲垪锛圗53 浼犳劅鍣?鎵ц鍣級

| 鏂囦欢 | 鑱岃矗 | 鍏抽敭鐐?|
|---|---|---|
| [E53_SF1.h](applications/BearPi/BearPi-HM_Nano/sample/C1_e53_sf1_mq2/include/E53_SF1.h) | 鐑熼浘鏉?API/鐘舵€佹灇涓?| `Init_E53_SF1`銆乣Get_MQ2_PPM`銆乣Beep_StatusSet` |
| [E53_SF1.c](applications/BearPi/BearPi-HM_Nano/sample/C1_e53_sf1_mq2/src/E53_SF1.c) | MQ2 ADC 閲囨牱銆丷S/R0 鎹㈢畻銆丳PM銆佽渹楦ｅ櫒 PWM | ADC6锛汸WM1 GPIO8锛沗CAL_PPM=20`銆乣RL=1` |
| [e53_sf1_example.c](applications/BearPi/BearPi-HM_Nano/sample/C1_e53_sf1_mq2/e53_sf1_example.c) | 1 s 璇?PPM锛?16 寮€铚傞福鍣?| 寮€鏈?1 s 鏍″噯 |
| [E53_IA1.h](applications/BearPi/BearPi-HM_Nano/sample/C2_e53_ia1_temp_humi_pls/include/E53_IA1.h) | 娓╂箍搴?鍏夌収鏉?API/鏁版嵁缁撴瀯 | `SHT30_Addr=0x44`銆乣BH1750_Addr=0x23` |
| [E53_IA1.c](applications/BearPi/BearPi-HM_Nano/sample/C2_e53_ia1_temp_humi_pls/src/E53_IA1.c) | SHT30 CRC/娓╂箍搴︽崲绠椼€丅H1750 璇诲厜銆佺數鏈?LED | I2C1锛汫PIO8 鐢垫満銆丟PIO14 鐏?|
| [e53_ia1_example.c](applications/BearPi/BearPi-HM_Nano/sample/C2_e53_ia1_temp_humi_pls/e53_ia1_example.c) | 1 s 璇讳笁鍙傛暟锛屽厜鐓?20 寮€鐏紝婀垮害>70 鎴栨俯搴?35 寮€鐢垫満 | 鍏ㄥ眬 `E53_IA1_Data` |
| [E53_SC1.h](applications/BearPi/BearPi-HM_Nano/sample/C3_e53_sc1_pls/include/E53_SC1.h) | 鍏夌収鏉?API | `E53_SC1_Read_Data` |
| [E53_SC1.c](applications/BearPi/BearPi-HM_Nano/sample/C3_e53_sc1_pls/src/E53_SC1.c) | BH1750 鍒濆鍖?璇诲€笺€丟PIO7 鐏?| I2C1 400 kbps |
| [e53_sc1_example.c](applications/BearPi/BearPi-HM_Nano/sample/C3_e53_sc1_pls/e53_sc1_example.c) | 1 s 璇?Lux锛?20 寮€鐏?| 鈥?|
| [E53_SC2.h](applications/BearPi/BearPi-HM_Nano/sample/C4_e53_sc2_axis/include/E53_SC2.h) | MPU6050 瀵勫瓨鍣?API/鏁版嵁缁撴瀯 | 0x68锛涘姞閫熷害 0x3B銆佹俯搴?0x41銆乄HO_AM_I 0x75 |
| [E53_SC2.c](applications/BearPi/BearPi-HM_Nano/sample/C4_e53_sc2_axis/src/E53_SC2.c) | MPU6050 鍒濆鍖?璇诲姞閫熷害/娓╁害銆佸弻 LED | I2C1锛汫PIO7/8锛涢噺绋?卤16 g |
| [e53_sc2_example.c](applications/BearPi/BearPi-HM_Nano/sample/C4_e53_sc2_axis/e53_sc2_example.c) | 1 s 璇绘暟鎹紝卤100 闃堝€煎垽鏂€炬枩锛屽垏鎹?LED | 棣栨璇诲€间綔涓哄熀鍑?|
| [E53_IS1.h](applications/BearPi/BearPi-HM_Nano/sample/C5_e53_is1_infrared/include/E53_IS1.h) | 浜轰綋绾㈠ API/鍥炶皟绫诲瀷 | `E53_IS1_CallbackFunc` |
| [E53_IS1.c](applications/BearPi/BearPi-HM_Nano/sample/C5_e53_is1_infrared/src/E53_IS1.c) | GPIO7 涓婂崌娌夸腑鏂敞鍐屻€佽渹楦ｅ櫒 PWM1 | 鍥炶皟鐢变笂灞備紶鍏?|
| [e53_is1_example.c](applications/BearPi/BearPi-HM_Nano/sample/C5_e53_is1_infrared/e53_is1_example.c) | 涓柇缃簨浠朵綅锛岀嚎绋嬬瓑浜嬩欢鍚庤渹楦?300 tick | `evt_id`銆乣FLAGS_MSK1` |
| [flower.h](applications/BearPi/BearPi-HM_Nano/sample/C6_e53_flower_ia1/include/flower.h) | 鑺卞尃鏁版嵁缁撴瀯/API | Lux/Smo/Humidity/Temperature |
| [flower.c](applications/BearPi/BearPi-HM_Nano/sample/C6_e53_flower_ia1/src/flower.c) | 鍙?I2C锛欼2C0 SHT30銆両2C1 BH1750锛汚DC6 鍦熷￥锛汫PIO5 姘存车銆丟PIO8 椋庢墖銆丟PIO14 琛ュ厜 | 姘存车浣庣數骞虫湁鏁?|
| [e53_flower_ia1_example.c](applications/BearPi/BearPi-HM_Nano/sample/C6_e53_flower_ia1/e53_flower_ia1_example.c) | 1 s 璇诲洓鍙傛暟锛屾俯搴?10 寮€椋庢墖 | 鍙帶鍒堕鎵囷紝姘存车/琛ュ厜鏈棴鐜?|

> C6 鐨?`BUILD.gn` 鐩爣鍚嶆槸 `e53_flower_ia1_example`锛屼絾 `sample/BUILD.gn` 閲屾牴鏈病鏈?C6 杩欎竴琛岋紱瑕佺紪璇?C6锛岄渶瑕佹墜鍔ㄥ姞锛?> `"C6_e53_flower_ia1:e53_flower_ia1_example"`銆?
#### D 绯诲垪锛堢綉缁滀笌浜戯級

| 鏂囦欢 | 鑱岃矗 | 鍏抽敭鐐?|
|---|---|---|
| [wifi_ap.c](applications/BearPi/BearPi-HM_Nano/sample/D1_iot_wifi_ap/wifi_ap.c) | AP 鐑偣 + DHCP 鏈嶅姟 + UDP 8888 鍥炴樉 | SSID `BearPi`锛屽瘑鐮?`0987654321`锛屼俊閬?7锛孖P 192.168.1.1 |
| [wifi_sta_connect.c](applications/BearPi/BearPi-HM_Nano/sample/D2_iot_wifi_sta_connect/wifi_sta_connect.c) | STA 鎵弿/鍖归厤/杩炴帴/DHCP | 鐩爣 `BearPi`/`0987654321`锛涜秴鏃?15 s |
| [udp_client_demo.c](applications/BearPi/BearPi-HM_Nano/sample/D3_iot_udp_client/udp_client_demo.c) | UDP 瀹㈡埛绔?| 鏈嶅姟鍣?192.168.0.175:8888锛?0 s 涓€娆?|
| [wifi_connect.c](applications/BearPi/BearPi-HM_Nano/sample/D3_iot_udp_client/src/wifi_connect.c) | 閫氱敤 STA 杩炴帴鍑芥暟 `WifiConnect(ssid, psk)` | D3/D4/D5/D6/D7/D8鈥揇13 鍚勮嚜鏈変竴浠藉壇鏈?|
| [tcp_server_demo.c](applications/BearPi/BearPi-HM_Nano/sample/D4_iot_tcp_server/tcp_server_demo.c) | TCP 鏈嶅姟绔?| 8888锛宐acklog 10锛宺ecv/send 鍚?2 s |
| [iot_mqtt.c](applications/BearPi/BearPi-HM_Nano/sample/D5_iot_mqtt/iot_mqtt.c) | Paho MQTT 瀹㈡埛绔?| Broker 192.168.0.176:1883锛宍pubtopic`/`substopic`锛孮oS2 |
| [oc_mqtt.h](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/include/oc_mqtt.h) | 鍗庝负 OC MQTT 灏佽 API/鏋氫妇/缁撴瀯 | 鏈嶅姟鍣?117.78.5.125:1883锛沗OC_SERVER_URL` 鏄?OneNET 鍦板潃锛堟湭鐢級 |
| [oc_mqtt.c](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/src/oc_mqtt.c) | Paho 杩炴帴銆佽闃?鍙戝竷銆佸睘鎬?鍛戒护 Topic 缁勮 | `oc_mqtt_profile_*`锛宍$oc/devices/...` |
| [oc_mqtt_profile_package.h](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/include/oc_mqtt_profile_package.h) | profile JSON 鎵撳寘鍑芥暟澹版槑 | 鈥?|
| [oc_mqtt_profile_package.c](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/src/oc_mqtt_profile_package.c) | 鐢?cJSON 鎷煎睘鎬?鍛戒护鍝嶅簲 JSON | `services`/`properties`/`paras` |
| [iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/iot_cloud_oc_sample.c) | 鍐滀笟妗堜緥锛氫紶鎰熷櫒绾跨▼ + 涓荤嚎绋?+ 鍛戒护闃熷垪 | `Agriculture` 鏈嶅姟锛? 涓睘鎬э紝2 涓懡浠?|
| [E53_IA1.c](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/src/E53_IA1.c) | D6 涓撶敤 IA1 椹卞姩鍓湰 | `E53_IA1_Read_Data(E53_IA1_Data_TypeDef*)`锛屼笌 C2 绛惧悕涓嶅悓 |
| [onenet.h](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/include/onenet.h) | OneNET MQTT API/璁惧淇℃伅缁撴瀯 | 183.230.40.39:6002 |
| [onenet_mqtt.c](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/src/onenet_mqtt.c) | OneNET MQTT 杩炴帴銆乣$dp` 鏁版嵁鎵撳寘/涓婁紶 | 3 瀛楄妭澶?`0x03 + len_hi + len_lo` |
| [iot_cloud_onenet_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/iot_cloud_onenet_sample.c) | 涓婃姤绾跨▼ + 浼犳劅鍣ㄧ嚎绋?| 1 s 涓婁紶銆? s 閲囨牱锛涙暟鎹珵浜?|
| [E53_IA1.c](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/src/E53_IA1.c) | D7 涓撶敤 IA1 椹卞姩鍓湰 | 涓?C2 绫讳技锛屼絾 `E53_IA1_Read_Data()` 鏃犲弬 |
| [D8 iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D8_iot_cloud_oc_smoke/iot_cloud_oc_sample.c) | 鏅烘収鐑熸劅锛歁Q2 + 铚傞福鍣?+ IoTDA | 鏈嶅姟 `Smoke`锛涘懡浠?`Smoke_Control_Beep` |
| [D9 iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D9_iot_cloud_oc_light/iot_cloud_oc_sample.c) | 鏅烘収璺伅锛欱H1750 + LED + IoTDA | 鏈嶅姟 `Light`锛涘懡浠?`Light_Control_Led` |
| [D10 iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D10_iot_cloud_oc_manhole_cover/iot_cloud_oc_sample.c) | 鏅烘収浜曠洊锛歁PU6050 + 鍙?LED + IoTDA | 鏈嶅姟 `Manhole_Cover`锛涙棤鍛戒护 |
| [D11 iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D11_iot_cloud_oc_infrared/iot_cloud_oc_sample.c) | 浜轰綋鎰熷簲锛欸PIO7 涓柇 + 铚傞福鍣?+ IoTDA | 鏈嶅姟 `Infrared`锛涘崟绾跨▼ |
| [D12 iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D12_iot_cloud_oc_agriculture/iot_cloud_oc_sample.c) | 鏅烘収鍐滀笟锛欼A1 + IoTDA | 鏈嶅姟 `Agriculture`锛涘懡浠?light/motor |
| [D13 iot_cloud_oc_sample.c](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/iot_cloud_oc_sample.c) | 鏅烘収鐗╂祦锛欸PS + IoTDA | 鏈嶅姟 `Track`锛涘懡浠?`Track_Control_Beep` |
| [E53_ST1.c](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/src/E53_ST1.c) | GPS UART1 鍒濆鍖栥€丯MEA GPRMC 瑙ｆ瀽銆佽渹楦ｅ櫒 | 9600 8N1锛涘彧瑙ｆ瀽缁忕含搴?|
| [E53_ST1.h](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/include/E53_ST1.h) | GPS 鏁版嵁缁撴瀯/API | `gps_msg`銆乣E53_ST1_Data_TypeDef` |
| [wifi_connect.h](applications/BearPi/BearPi-HM_Nano/sample/D3_iot_udp_client/include/wifi_connect.h) | `WifiConnect` 澹版槑 | 鍚?D 宸ョ▼鍚勬湁涓€浠?|

D8鈥揇13 姣忎釜宸ョ▼杩樺甫涓€浠芥湰鍦?E53 椹卞姩鍜?`wifi_connect` 鍓湰锛?
| 宸ョ▼ | 鏈湴椹卞姩婧愭枃浠?| 鏈湴澶存枃浠?| 瀵瑰簲 C 绯诲垪 |
|---|---|---|---|
| D8 | [src/E53_SF1.c](applications/BearPi/BearPi-HM_Nano/sample/D8_iot_cloud_oc_smoke/src/E53_SF1.c) | [include/E53_SF1.h](applications/BearPi/BearPi-HM_Nano/sample/D8_iot_cloud_oc_smoke/include/E53_SF1.h)銆乣include/E53_IA1.h`锛堟湭浣跨敤锛?| C1 |
| D9 | [src/E53_SC1.c](applications/BearPi/BearPi-HM_Nano/sample/D9_iot_cloud_oc_light/src/E53_SC1.c) | [include/E53_SC1.h](applications/BearPi/BearPi-HM_Nano/sample/D9_iot_cloud_oc_light/include/E53_SC1.h) | C3 |
| D10 | [src/E53_SC2.c](applications/BearPi/BearPi-HM_Nano/sample/D10_iot_cloud_oc_manhole_cover/src/E53_SC2.c) | [include/E53_SC2.h](applications/BearPi/BearPi-HM_Nano/sample/D10_iot_cloud_oc_manhole_cover/include/E53_SC2.h) | C4 |
| D11 | [src/E53_IS1.c](applications/BearPi/BearPi-HM_Nano/sample/D11_iot_cloud_oc_infrared/src/E53_IS1.c) | [include/E53_IS1.h](applications/BearPi/BearPi-HM_Nano/sample/D11_iot_cloud_oc_infrared/include/E53_IS1.h) | C5 |
| D12 | [src/E53_IA1.c](applications/BearPi/BearPi-HM_Nano/sample/D12_iot_cloud_oc_agriculture/src/E53_IA1.c) | [include/E53_IA1.h](applications/BearPi/BearPi-HM_Nano/sample/D12_iot_cloud_oc_agriculture/include/E53_IA1.h) | C2锛坄Read_Data` 鏀逛负鎸囬拡鍙傛暟锛?|
| D13 | [src/E53_ST1.c](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/src/E53_ST1.c) | [include/E53_ST1.h](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/include/E53_ST1.h) | 鏃狅紙GPS 涓撶敤锛?|

> 姣忎釜 D8鈥揇13 鐩綍涔熷悇鏈変竴浠?`src/wifi_connect.c` 鍜?`include/wifi_connect.h`锛屽唴瀹逛笌 D3 鐨?278 琛岀増鏈熀鏈竴鑷淬€?
> D8鈥揇13 鐨?`wifi_connect.c` 鏄悓涓€浠?278 琛屼唬鐮佺殑鎷疯礉锛汥8鈥揇12 鐨?E53 椹卞姩鏄?C 绯诲垪椹卞姩鐨勬嫹璐濓紙瀛樺湪绛惧悕/娉ㄩ噴/閫昏緫鍒嗗弶锛岃绗?8 鑺傦級锛孌13 鐨?`E53_ST1` 鏄嫭绔?GPS 椹卞姩銆備簩娆″紑鍙戝簲鎶婂畠浠娊鎴愬叕鍏辩粍浠讹紝鑰屼笉鏄户缁鍒躲€?
#### Z 绯诲垪涓庢ā鏉?
| 鏂囦欢 | 鑱岃矗 | 鍏抽敭鐐?|
|---|---|---|
| [uart_hi3861.c](applications/BearPi/BearPi-HM_Nano/sample/Z1_hi3861_uart_ylc/uart_hi3861.c) | UART1 甯﹁秴鏃舵敹鍙戯紙115200锛?| `hi_uart_read_timeout(...,20ms)`锛涙敹鍒颁竴甯ф垨缂撳啿婊¤繑鍥?|
| [flash_example.c](applications/BearPi/BearPi-HM_Nano/sample/Z2_hi3861_flash_ylc/flash_example.c) | 鍐呴儴 Flash 鍐?璇讳竴娆?| 鍦板潃鎹㈢畻鏈夐闄╋紝瑙?2.6 |
| [zx_developer_sample.c](applications/BearPi/BearPi-HM_Nano/sample/Zx_Developer/src/zx_developer_sample.c) | 寮€鍙戣€呮ā鏉?| 缂哄ご鏂囦欢銆乣ZX_Demo` 鏈畾涔夈€乣APP_FEATURE_INIT` 閲屾寰幆锛涗笉鍙備笌鏋勫缓 |
| [hello_world.c](applications/BearPi/BearPi-HM_Nano/sample/my_first_app/hello_world.c) | Hello World | `SYS_RUN(HelloWorld)`锛屾瘮 `APP_FEATURE_INIT` 鏇存棭鎵ц |

### 4.4 妗嗘灦涓庢澘绾у叧閿枃浠?
| 鏂囦欢 | 浣滅敤 |
|---|---|
| [ohos_init.h](utils/native/lite/include/ohos_init.h) | `APP_FEATURE_INIT`/`SYS_RUN` 绛夊惎鍔ㄦ瀹?|
| [system_init.c](base/startup/services/bootstrap_lite/source/system_init.c) | `HOS_SystemInit()` 鐨?7 涓惎鍔ㄩ樁娈?|
| [bootstrap_service.c](base/startup/services/bootstrap_lite/source/bootstrap_service.c) | 鏀跺埌 `BOOT_SYS_COMPLETED` 鍚庤皟鐢?`INIT_APP_CALL(service/feature)` |
| [app_main.c](vendor/hisi/hi3861/hi3861/app/wifiiot_app/src/app_main.c) | Hi3861 鐨?`app_main()`锛氬璁?Flash/NV/Wi-Fi/鍚姩 OpenHarmony |
| [app_io_init.c](vendor/hisi/hi3861/hi3861/app/wifiiot_app/init/app_io_init.c) | 鏉跨骇榛樿寮曡剼澶嶇敤锛歎ART0/1/2銆丼PI銆両2C銆丳WM銆両2S銆丼DIO |
| [flash_partition_table.c](vendor/hisi/hi3861/hi3861/platform/system/partition_table/flash_partition_table.c) | 2 MB Flash 榛樿鍒嗗尯琛?|
| [link.ld.S](vendor/hisi/hi3861/hi3861/build/link/link.ld.S) | 閾炬帴鑴氭湰锛孠EEP 鍚?`.zinitcall.*` 娈?|
| [BearPi-HM_Nano.json](build/lite/product/BearPi-HM_Nano.json) | 浜у搧閰嶇疆锛歜oard/kernel/compiler/瀛愮郴缁?|
| [platform.json](build/lite/platform/hi3861v100_liteos_riscv/platform.json) | 骞冲彴缁勪欢涓庝緷璧?|
| [sample/BUILD.gn](applications/BearPi/BearPi-HM_Nano/sample/BUILD.gn) | 绀轰緥閫夋嫨鍣紙褰撳墠 D1锛?|

---

## 5. 绋嬪簭杩愯娴佺▼

### 5.1 涓婄數鍒?`app_main`

```text
涓婄數
  鈫?Boot ROM锛堣姱鐗囧浐鍖栵級
  鈫?Hi3861_boot_signed.bin锛圔oot锛?  鈫?Hi3861_loader_signed.bin锛圠oader锛?  鈫?Hi3861_wifiiot_app_allinone.bin锛堝簲鐢級
  鈫?app_main()
```

`app_main()` 鐨勫叧閿『搴忥紙`app_main.c:400-497`锛夛細

1. 鎵撳嵃 SDK 鐗堟湰銆?2. `peripheral_init()`锛?   - 鍏虫椂閽熼棬鎺с€佸垵濮嬪寲 Flash锛?   - 鍒濆鍖?UART1 涓?115200 鐨?AT 鍙ｏ紱
   - `app_io_init()` 閰嶇疆榛樿寮曡剼澶嶇敤锛圲ART0 GPIO3/4銆乁ART1 GPIO5/6銆両2C0 GPIO9/10銆丳WM1 GPIO8 绛夛級锛?   - 鍒濆鍖?cipher銆丏MA銆両2C0锛?00 kbps锛夈€両2S銆丼PI0锛? MHz锛夈€丳WM1銆?3. `peripheral_init_no_sleep()`銆?4. 宸ュ巶 NV銆丗lash 鍒嗗尯琛ㄣ€佹櫘閫?NV銆丱TA銆佹枃浠剁郴缁熴€?5. 浜嬩欢銆丼AL銆佺湅闂ㄧ嫍銆佷綆鍔熻€椼€丄T/Diag/Shell銆?6. `tcpip_init()`锛坙wIP锛夈€?7. `hi_wifi_init(2, 2)`銆?8. `HOS_SystemInit()`銆?
> 閲嶈锛氱郴缁熷惎鍔ㄦ椂 **UART1 宸茬粡琚垵濮嬪寲涓?115200 鐨?AT 鍛戒护鍙?*銆侭6/D13 鍐嶈皟鐢?`UartInit(UART1, 9600, ...)` 浼氶噸鏂伴厤缃紱濡傛灉鍚屾椂鍚敤 AT/Shell锛屼細鍐茬獊銆?
### 5.2 OpenHarmony 鍚姩闃舵

`HOS_SystemInit()`锛坄system_init.c:19-28`锛夛細

```c
MODULE_INIT(bsp);       // 鏉跨骇
MODULE_INIT(device);    // 璁惧
MODULE_INIT(core);      // 鍐呮牳
SYS_INIT(service);      // 绯荤粺鏈嶅姟锛堟敞鍐?bootstrap 绛夛級
SYS_INIT(feature);      // 绯荤粺鐗规€?MODULE_INIT(run);       // SYS_RUN 闃舵
SAMGR_Bootstrap();      // 鍚姩鏈嶅姟妗嗘灦
```

`SAMGR_Bootstrap()` 鍒濆鍖栨墍鏈夌郴缁熸湇鍔★紱褰撶郴缁熸湇鍔″叏閮ㄥ垵濮嬪寲瀹屾垚锛宐ootstrap 鏈嶅姟鏀跺埌 `BOOT_SYS_COMPLETED`锛屾墽琛岋細

```c
INIT_APP_CALL(service);   // app.service 娈?INIT_APP_CALL(feature);   // app.feature 娈?鈫?APP_FEATURE_INIT 鍦ㄨ繖閲?```

`APP_FEATURE_INIT(func)` 灞曞紑涓猴細

```c
static const InitCall __zinitcall_app_feature_func
    __attribute__((section(".zinitcall.app.feature2.init"))) = func;
```

閾炬帴鑴氭湰 `link.ld.S:346-352` 鎶?`.zinitcall.app.feature0..4.init` 鏀堕泦鍒?`__zinitcall_app_feature_start/end`锛宐ootstrap 鏈嶅姟鎸夋椤哄簭閫愪釜璋冪敤銆?
### 5.3 `SYS_RUN` 涓?`APP_FEATURE_INIT` 鐨勫尯鍒?
| 瀹?| 娈?| 鎵ц鏃舵満 | 鍏稿瀷鐢ㄩ€?|
|---|---|---|---|
| `SYS_RUN(func)` | `.zinitcall.run2.init` | `MODULE_INIT(run)`锛屽湪 `SAMGR_Bootstrap()` 涔嬪墠 | 鏈€鏃╃殑涓氬姟鍏ュ彛锛屽 `my_first_app` |
| `APP_FEATURE_INIT(func)` | `.zinitcall.app.feature2.init` | `SAMGR_Bootstrap()` 瀹屾垚绯荤粺鏈嶅姟鍚?| 缁濆ぇ澶氭暟 BearPi 绀轰緥 |
| `APP_FEATURE_INIT_PRI(func, prio)` | `.zinitcall.app.feature{prio}.init` | 鍚屼笂锛屾寜 0鈫? 椤哄簭 | 闇€瑕佹帶鍒跺涓?feature 鐨勫厛鍚?|

**绾︽潫**锛歚APP_FEATURE_INIT` 鐨勫洖璋冭繍琛屽湪 bootstrap 鏈嶅姟浠诲姟涓婁笅鏂囷紝涓嶈兘鍦ㄩ噷闈㈠啓姝诲惊鐜紱姝ｇ‘鍋氭硶鏄€滃垱寤虹嚎绋嬪悗绔嬪埢杩斿洖鈥濄€俙Zx_Developer` 鐨?`while(1);` 浼氳鍚姩娴佺▼鍗℃锛屾墍浠ュ畠涓嶅弬涓庢瀯寤恒€?
### 5.4 涓诲惊鐜ā鍨?
闄?B2銆丏11 澶栵紝绀轰緥鐨勫吀鍨嬬粨鏋勬槸锛?
```c
static void XxxTask(void) {
    Init();                 // 澶栬鍒濆鍖?    while (1) {
        Read/Control();     // 涓氬姟
        usleep(...) / osDelay(...);
    }
}

static void XxxEntry(void) {
    osThreadAttr_t attr = {...};
    osThreadNew((osThreadFunc_t)XxxTask, NULL, &attr);
}
APP_FEATURE_INIT(XxxEntry);
```

- 娌℃湁 `main()`锛?- `APP_FEATURE_INIT` 鍙礋璐ｅ垱寤虹嚎绋嬶紱
- 绾跨▼閲屾槸姝诲惊鐜?+ 闃诲寤舵椂锛?- 涓柇/鍥炶皟鍙仛鈥滅疆浜嬩欢/缃槦鍒椻€濓紝閲嶆椿浜ょ粰绾跨▼銆?
### 5.5 鍚勭ず渚嬪叆鍙ｄ笌涓诲惊鐜?
| 绀轰緥 | 鍏ュ彛锛坄APP_FEATURE_INIT`锛?| 绾跨▼/鏍?浼樺厛绾?| 涓诲惊鐜涓?|
|---|---|---|---|
| A1 | `Thread_example` | `threadHi` 4 KB/25锛宍threadLo` 4 KB/24 | Hi 寤舵椂鈫掓寕璧疯嚜宸憋紱Lo 鎵撳嵃 10 娆♀啋鎭㈠ Hi鈫掕嚜鏉€ |
| A2 | `Timer_example` | 鏃犳柊绾跨▼锛堝畾鏃跺櫒鍥炶皟锛?| 瀹氭椂鍣? 100 tick銆佸畾鏃跺櫒2 300 tick锛?0 s 鍚庡仠姝?閲嶅惎/鍒犻櫎 timer1锛屽啀鍋?timer2 |
| A3 | `EventExtDemo` | 4 涓嚎绋嬶紝4 KB/24 | Button 2 s 缃?bit0锛孏PS 5 s 缃?bit1锛沇aitAny/WaitAll 涓や釜娑堣垂鑰?|
| A4 | `Mutex_example` | 3 涓嚎绋嬶紝4 KB锛?6/25/24 | 楂?浣庣嚎绋嬫姠閿侊紝涓嚎绋嬪懆鏈熸€ф墦鍗板苟寤舵椂锛岃瀵熶簰鏂ラ攣/浼樺厛绾х户鎵?|
| A5 | `PriorityInversionDemo` | 3 涓嚎绋嬶紝4 KB锛?4/26/27 | 浣庣嚎绋嬫寔淇″彿閲忓仛闀挎椿锛屼腑绾跨▼闇稿崰 CPU锛岄珮绾跨▼绛変俊鍙烽噺 |
| A6 | `Message_example` | 2 涓嚎绋嬶紝10 KB/25 | 鐢熶骇鑰?100 tick 鍙戜竴鏉★紝娑堣垂鑰呮案涔呯瓑 |
| B1 | `LedExampleEntry` | 512 B/25 | GPIO2 1 s 缈昏浆 |
| B2 | `ButtonExampleEntry` | 鏃犳柊绾跨▼ | 娉ㄥ唽 F1/F2 涓嬮檷娌夸腑鏂紝涓柇閲岀偣鐏?鐏伅 |
| B3 | `PWMExampleEntry` | 4 KB/25 | PWM2 鍗犵┖姣?0鈫?0000锛屾闀?1000锛屾瘡妗?1 s |
| B4 | `ADCExampleEntry` | 8 KB/24 | 1 s 璇?ADC5锛屾墦鍗扮數鍘?|
| B5 | `I2CExampleEntry` | 8 KB/25 | 鍒濆鍖?I2C1锛屽啓 NFC 鏂囨湰+缃戝潃锛屼箣鍚?1 s 鎻愮ず |
| B6 | `UART_ExampleEntry` | 8 KB/25 | UART1 鍙?`Hello, BearPi!`锛岃鍥炲苟鎵撳嵃锛? s 涓€娆?|
| C1 | `ExampleEntry` | 8 KB/25 | 1 s 璇?PPM锛?16 寮€铚傞福鍣?|
| C2 | `ExampleEntry` | 8 KB/25 | 1 s 璇?Lux/婀垮害/娓╁害锛屾帶鍒剁伅/鐢垫満 |
| C3 | `ExampleEntry` | 8 KB/25 | 1 s 璇?Lux锛?20 寮€鐏?|
| C4 | `ExampleEntry` | 8 KB/25 | 1 s 璇诲姞閫熷害/娓╁害锛屄?00 鍒ゆ柇鍊炬枩锛屽垏鎹?LED |
| C5 | `ExampleEntry` | 8 KB/25 | 绛変簨浠朵綅锛岃渹楦?300 tick锛? s锛?|
| C6 | `ExampleEntry` | 10 KB/25 | 1 s 璇诲湡澹?鍏夌収/娓╂箍搴︼紝娓╁害>10 寮€椋庢墖 |
| D1 | `Wifi_AP_Demo` | 10 KB/25 | AP + DHCP + UDP 8888 鍥炴樉锛岄樆濉?`recvfrom` |
| D2 | `WifiClientSTA` | 10 KB/24 | 鎵弿鈫掑尮閰?`BearPi`鈫掕繛鎺モ啋DHCP鈫掓墦鍗?IP鈫掔┖杞?|
| D3 | `UDPClientDemo` | 10 KB/鏅€?| 10 s 鍙戜竴娆★紝鍐嶆敹 |
| D4 | `TCPServerDemo` | 10 KB/鏅€?| accept 鍚?recv/send锛屽悇 2 s |
| D5 | `MQTT_Demo` | 10 KB/鏅€?| 杩炴帴鈫掕闃呪啋姣?50 tick 鍙戝竷 |
| D6 | `OC_Demo` | 涓?10 KB/24锛屼紶鎰熷櫒 2 KB/25 | 浼犳劅鍣?3 s 鍏ラ槦锛涗富绾跨▼澶勭悊鍛戒护/涓婃姤 |
| D7 | `MQTT_Demo` | 涓や釜 10 KB/鏅€?| 涓婃姤 1 s锛岄噰鏍?2 s |
| D8 | `OC_Demo` | 涓?10 KB/24锛屼紶鎰熷櫒 4 KB/25 | 3 s 璇?PPM锛涗簯鍛戒护鎺у埗铚傞福鍣?|
| D9 | `OC_Demo` | 涓?10 KB/24锛屼紶鎰熷櫒 4 KB/25 | 3 s 璇?Lux锛涗簯鍛戒护鎺у埗 LED |
| D10 | `OC_Demo` | 涓?10 KB/24锛屼紶鎰熷櫒 4 KB/25 | 3 s 璇?MPU6050锛涘€炬枩涓婃姤 |
| D11 | `OC_Demo` | 鍗曠嚎绋?10 KB/24 | 绛?GPIO7 浜嬩欢锛涜渹楦?500 tick 鍚庝笂鎶?|
| D12 | `OC_Demo` | 涓?10 KB/24锛屼紶鎰熷櫒 **2 KB**/25 | 3 s 璇?IA1锛涗簯鍛戒护鎺у埗鐏?鐢垫満 |
| D13 | `OC_Demo` | 涓?10 KB/24锛屼紶鎰熷櫒 4 KB/25 | 3 s 璇?GPS锛涗笂鎶ョ粡绾害锛涗簯鍛戒护鎺у埗铚傞福鍣?|
| Z1 | `UART_ExampleEntry` | 2 KB/15 | UART1 115200锛?0 ms 瓒呮椂鏀朵竴甯у苟鍥炴樉 |
| Z2 | `in_flash_test` | 鏃犳柊绾跨▼ | 鍐?200 瀛楄妭鍒?Flash 鏈熬锛岃鍥炴墦鍗?|
| my_first_app | `HelloWorld`锛坄SYS_RUN`锛?| 鏃?| 鎵撳嵃涓€娆?|
| Zx | `ZX_Demo`锛堟湭瀹氫箟锛?| 鏃?| `while(1);`锛屼笉鍙備笌鏋勫缓 |

---

## 6. 澶栬椹卞姩娓呭崟涓庨┍鍔ㄩ€昏緫

### 6.1 GPIO

**鎺ュ彛**锛歚GpioInit`銆乣GpioSetDir`銆乣GpioSetOutputVal`銆乣GpioGetInputVal`銆乣IoSetFunc`銆乣IoSetPull`銆乣GpioRegisterIsrFunc`銆?
**椹卞姩閫昏緫**锛?
1. `GpioInit()` 鎵撳紑 GPIO 妯″潡銆?2. `IoSetFunc(gpio, func)` 鎶婂紩鑴氫粠榛樿澶嶇敤鍒囧埌鐩爣鍔熻兘锛堟櫘閫?GPIO銆両2C銆丳WM銆乁ART锛夈€?3. `GpioSetDir` 璁捐緭鍏?杈撳嚭锛涜緭鍏ュ彲 `IoSetPull` 閰嶄笂/涓嬫媺銆?4. 杈撳嚭鐢?`GpioSetOutputVal`锛涜緭鍏ョ敤 `GpioGetInputVal`銆?5. 涓柇鐢?`GpioRegisterIsrFunc(id, WIFI_IOT_INT_TYPE_EDGE, 鏋佹€? callback, arg)`銆?
**绀轰緥**锛?
- B1锛欸PIO2 杈撳嚭锛? s 缈昏浆銆?- B2锛欸PIO11/12 杈撳叆涓婃媺锛屼笅闄嶆部涓柇锛涘洖璋冮噷鐩存帴鐐圭伅/鐏伅銆?- C5/D11锛欸PIO7 杈撳叆涓婃媺锛屼笂鍗囨部涓柇锛涘洖璋冨彧 `osEventFlagsSet`锛岀嚎绋嬪鐞嗚渹楦ｃ€?
**娉ㄦ剰**锛?
- `GpioRegisterIsrFunc` 鐨勫洖璋冭繍琛屽湪涓柇涓婁笅鏂囷紝涓嶈兘 `printf` 澶ч噺鍐呭銆佷笉鑳介樆濉烇紱绀轰緥 B2 鍦ㄥ洖璋冮噷 `printf`锛屾暀瀛﹀彲鐢紝宸ョ▼涓婂簲鏀逛负缃簨浠?闃熷垪銆?- 鍚屼竴寮曡剼涓嶈兘鍚屾椂鍋氳緭鍏ュ拰杈撳嚭锛汣3/C4 涓?C5 閮藉崰 GPIO7锛屼笉鑳藉悓鏃跺惎鐢ㄣ€?
### 6.2 PWM

**鎺ュ彛**锛歚PwmInit(port)`銆乣PwmStart(port, duty, freq)`銆乣PwmStop(port)`銆?
**璇箟**锛坄hi_pwm.c:162-182`锛夛細

- `freq` 鏄垎棰戝€硷紙16 浣嶏級锛涙寜榛樿 160 MHz 鏃堕挓锛孭WM 鍛ㄦ湡 = `freq / 160 MHz`锛岄鐜?= `160 MHz / freq`锛?- `duty` 鏄珮鐢靛钩璁℃暟锛屽崰绌烘瘮 = `duty / freq`锛?- 瑕佹眰 `0 < duty <= freq`锛屼笖 `freq != 0`銆?
**绀轰緥**锛?
- B3锛歚PwmStart(PWM2, i, 40000)`锛宨=0..40000锛屽崰绌烘瘮 0鈥?00%锛孭WM 棰戠巼 4 kHz銆?- C1/C5/D8/D11/D13锛歚PwmStart(PWM1, 20000, 40000)`锛?0% 鍗犵┖姣斻€? kHz锛岄┍鍔ㄨ渹楦ｅ櫒銆?- C2/C4锛欸PIO8 浣滀负鏅€氳緭鍑烘帶鍒剁數鏈?LED锛屼笉鍐嶇敤 PWM銆?
**娉ㄦ剰**锛?
- PWM 杈撳嚭鍓嶅繀椤诲厛 `IoSetFunc` 鎶婂紩鑴氬垏鍒板搴?PWM 閫氶亾锛屽啀 `GpioSetDir` 杈撳嚭锛屽啀 `PwmInit`銆?- `PwmStart` 鐨?`duty` 涓嶈兘涓?0锛汢3 浠?i=0 寮€濮嬶紝绗竴娆¤皟鐢ㄤ細杩斿洖鍙傛暟閿欒锛堜唬鐮佹湭妫€鏌ワ級锛屽疄闄呬寒搴︿粠 i=1000 寮€濮嬨€?
### 6.3 ADC

**鎺ュ彛**锛歚AdcRead(channel, &data, equModel, curBais, rstCnt)`銆?
- 12 浣嶅垎杈ㄧ巼锛宍data` 0鈥?095锛?- `equModel` 鍙€?1/2/4/8 娆″钩鍧囷紱
- `curBais` 榛樿鑷姩锛?- `rstCnt` 0鈥?xFF0锛屽崟浣?334 ns锛堝ご鏂囦欢瑕佹眰锛岀ず渚嬬敤 0xFF锛夈€?
**鎹㈢畻**锛?
```c
voltage = data * 1.8 * 4 / 4096.0;
```

- 1.8 V 鏄?ADC 鍙傝€冿紱
- 脳4 鏄澘涓?4:1 鍒嗗帇锛?- 4096 鏄?12 浣嶆弧閲忕▼銆?
**绀轰緥**锛?
- B4锛欰DC5 璇?F1锛屾澗閿害 3.3 V锛屾寜涓嬬害 0.2 V銆?- C1锛欰DC6 璇?MQ2锛宍RS=(5-v)/v*RL`锛宍ppm=613.9*pow(RS/R0,-2.074)`銆?- C6锛欰DC6 璇诲湡澹わ紝`Smo = adc/1500*100`銆?- D8锛欰DC6 璇?MQ2锛屾牎鍑嗗悗涓婃姤 ppm銆?
**娉ㄦ剰**锛?
- ADC 閫氶亾涓?GPIO 缂栧彿涓嶆槸涓€鍥炰簨锛汚DC5 瀵瑰簲 GPIO11锛孉DC6 瀵瑰簲 E53 鐨?ADC6 寮曡剼銆?- `AdcRead` 鐨?`rstCnt` 绀轰緥鐢?`0xff`锛屼笉鏄椂闂存绉掋€?- 鍦熷￥婀垮害鍏紡 `adc/1500*100` 鏄粡楠屽€硷紝鏈仛 3.3 V 褰掍竴鍖栵紝鎹㈡澘/鎹㈠湡闇€瑕侀噸鏂版爣瀹氥€?
### 6.4 I2C

**鎺ュ彛**锛歚I2cInit(id, baudrate)`銆乣I2cSetBaudrate`銆乣I2cWrite`銆乣I2cRead`銆乣I2cWriteread`銆?
**璁惧鍦板潃**锛? 浣嶏級锛?
| 璁惧 | 鍦板潃 | 鎬荤嚎 | 绀轰緥 |
|---|---:|---|---|
| NT3H1201 NFC | 0x55 | I2C1 | B5 |
| BH1750 鍏夌収 | 0x23 | I2C1锛圕2/C3/C6/D6/D7/D9/D12锛夛紱C6 鐨?BH1750 浠嶅湪 I2C1 | C2/C3/C6/D6/D7/D9/D12 |
| SHT30 娓╂箍搴?| 0x44 | I2C1锛圕2/D6/D7/D12锛夛紱C6 鐢?I2C0 | C2/C6/D6/D7/D12 |
| MPU6050 | 0x68 | I2C1 | C4/D10 |

**椹卞姩閫昏緫**锛?
- 鍏?`IoSetFunc(GPIO0, I2C1_SDA)`銆乣IoSetFunc(GPIO1, I2C1_SCL)`锛?- `I2cInit(I2C1, 400000)`锛?- 鍐欙細`sendBuf/sendLen`锛涜锛歚receiveBuf/receiveLen`锛涘啓鍚庤锛歚I2cWriteread`锛?- 鍦板潃鍙傛暟鐢?`(addr << 1) | 0x00` 鍐欍€乣| 0x01` 璇汇€?
**鍚勪紶鎰熷櫒缁嗚妭**锛?
- **BH1750**锛氬垵濮嬪寲鍛戒护 `0x01`锛堜笂鐢碉級锛屾祴閲忓懡浠?`0x10`锛堣繛缁珮鍒嗚鲸鐜囷級锛屽欢鏃?180 ms锛岃 2 瀛楄妭锛宍Lux = raw / 1.2`銆?- **SHT30**锛氬垵濮嬪寲 `0x22 0x36`锛堝懆鏈熸祴閲忥級锛岃 6 瀛楄妭锛堟俯搴?2 + CRC + 婀垮害 2 + CRC锛夛紝CRC 澶氶」寮?`0x131`锛屾俯搴?`175*raw/65535 - 45`锛屾箍搴?`100*raw/65535`銆?- **MPU6050**锛氬浣?`PWR_MGMT_1=0x80`锛屽敜閱?`0x00`锛屽叧涓柇/FIFO/I2C 涓绘ā寮忥紝閰嶇疆 DLPF銆伮?6 g銆佷腑鏂紩鑴氾紱璇?`0x3B` 6 瀛楄妭鍔犻€熷害銆乣0x41` 2 瀛楄妭娓╁害锛沗WHO_AM_I=0x75` 搴斾负 0x68锛涙俯搴?`((raw+13200)/280)-13`銆?- **NT3H**锛氶〉澶у皬 16 瀛楄妭锛岀敤鎴峰尯 0x01鈥?x77锛岄厤缃?0x7A锛孲RAM 0xF8鈥?xFB锛涙瘡娆″啓鍚?`usleep(300000)` 绛夎姱鐗囧唴閮ㄥ啓瀹屾垚锛汵DEF 璁板綍棣栨潯/杩藉姞/涓棿/鏈潯鐢?`ndefPosition` 鎺у埗銆?
**娉ㄦ剰**锛?
- I2C1 涓婃寕浜?NFC銆丅H1750銆丼HT30銆丮PU6050锛屽湴鍧€涓嶅啿绐佸嵆鍙叡瀛橈紱浣嗕笉鍚屾墿灞曟澘鐨?SHT30 鍙兘鍦ㄥ悓涓€鍦板潃锛屼笉鑳藉悓鏃舵帴銆?- C6 鐢?I2C0锛圙PIO9/10锛夋帴 SHT30锛屾槸涓轰簡閬垮紑 I2C1 涓婄殑 IA1锛涜繖鏄弻鎵╁睍鏉块泦鎴愮殑鍏抽敭鏀瑰姩銆?- 浠ｇ爜涓?`I2cWrite` 鐨勮繑鍥炲€煎鏁版湭妫€鏌ワ紝浼犳劅鍣ㄦ湭鎺ユ椂涓嶄細鎶ラ敊锛屽彧浼氳鍒?0/0xFF銆?
### 6.5 UART

**鎺ュ彛**锛歚UartInit(id, &attr, NULL)`銆乣UartWrite`銆乣UartRead`锛沍1 鐩存帴鐢?`hi_uart_init`銆乣hi_uart_read_timeout`銆乣hi_uart_write`銆?
**鍒嗛厤**锛?
| 涓插彛 | 寮曡剼 | 鐢ㄩ€?| 鍙傛暟 |
|---|---|---|---|
| UART0 | GPIO3 TX / GPIO4 RX | 璋冭瘯 `printf` | 115200 8N1 |
| UART1 | GPIO5 RX / GPIO6 TX | E53 UART / GPS / AT | B6/D13 9600锛沍1 115200 |
| UART2 | GPIO11 TX / GPIO12 RX | 榛樿鏈敤 | 鈥?|

**椹卞姩閫昏緫**锛?
- `UartInit` 閰嶇疆娉㈢壒鐜?鏁版嵁浣?鍋滄浣?鏍￠獙锛?- `UartWrite` 闃诲鍙戦€侊紱
- `UartRead` 闃诲璇伙紝鐩村埌璇绘弧鎴栬秴鏃讹紙鍏蜂綋鐪嬪簳灞傚疄鐜帮級锛汢6 璇?1000 瀛楄妭锛岄潬 TX/RX 鐭帴鍥炵幆锛?- Z1 鐢?`hi_uart_read_timeout` 鍋?20 ms 瓒呮椂锛屾敹瀹屼竴甯ф垨缂撳啿婊¤繑鍥炪€?
**娉ㄦ剰**锛?
- 绯荤粺鍚姩鏃?UART1 宸茶 `peripheral_init` 閰嶆垚 115200 AT 鍙ｏ紱D13 鏀规垚 9600 鍚庯紝AT 鍔熻兘涓嶅彲鐢ㄣ€?- D13 鎶?GPIO4锛圲ART0_RXD锛夎鎴愭櫘閫氳緭鍑哄苟鎷変綆锛岃皟璇曚覆鍙ｄ粛鑳藉彂閫侊紙TX 涓嶅彈褰卞搷锛夛紝浣嗘帴鏀惰鐮村潖銆?- B6 闇€瑕佹妸 E53 鐨?UART_TX/RX 鐢ㄦ潨閭︾嚎鐭帴锛屽惁鍒欒涓嶅埌鏁版嵁銆?
### 6.6 NFC

**鍒嗗眰**锛?
```text
i2c_example.c
  鈫?nfc.c        storeText / storeUrihttp
    鈫?ndef.c     NT3HwriteRecord锛堥鏉?杩藉姞/涓棿/鏈潯锛?      鈫?nfcForum.c  NDEF 璁板綍澶?+ Text/URI 璐熻浇缂栫爜
        鈫?NT3H.c  椤佃鍐?/ I2C 瓒呮椂
          鈫?wifiiot_i2c.c  I2cWrite / I2cWriteread
```

**娴佺▼**锛?
1. GPIO0/1 澶嶇敤 I2C1锛?00 kbps銆?2. `storeText(NDEFFirstPos, TEXT)`锛氬啓绗竴鏉?Text 璁板綍銆?3. `storeUrihttp(NDEFLastPos, WEB)`锛氳拷鍔?URI 璁板綍銆?4. 鎵嬫満 NFC 纰颁竴纰帮紝璇诲彇 NDEF 鏂囨湰/缃戝潃銆?
**娉ㄦ剰**锛?
- NT3H 鍐欎竴椤靛悗蹇呴』绛?300 ms锛屽惁鍒欒繛缁啓浼氬け璐ャ€?- NDEF 棣栨潯璁板綍鐨?header 閲屾湁鎬婚暱搴︼紱杩藉姞璁板綍鏃惰鍏堣鍥炲ご閮ㄥ啀鏇存柊锛屼唬鐮佸凡澶勭悊銆?- B5 鐨?README 鎶?SCL/SDA 鍐欏弽浜嗭紙README 璇?SCL=GPIO0銆丼DA=GPIO1锛涗唬鐮佹槸 SDA=GPIO0銆丼CL=GPIO1锛夛紝浠ヤ唬鐮佷负鍑嗐€?
### 6.7 Wi-Fi

**STA 杩炴帴娴佺▼**锛坄wifi_connect.c:53-168`锛夛細

1. `osDelay(200)` 绛?Wi-Fi 椹卞姩灏辩华銆?2. 娉ㄥ唽浜嬩欢鍥炶皟锛氭壂鎻忕姸鎬併€佽繛鎺ョ姸鎬併€丄P 浜嬩欢銆?3. `EnableWifi()`銆乣IsWifiActive()`銆?4. `Scan()`锛岀瓑 `OnWifiScanStateChanged` 缃?`g_staScanSuccess`銆?5. `GetScanInfoList`锛屾墦鍗?SSID/RSSI銆?6. 鍖归厤鐩爣 SSID锛宍AddDeviceConfig` 鈫?`ConnectTo`銆?7. 绛?`OnWifiConnectionChanged` 缃?`g_ConnectSuccess`銆?8. `netifapi_netif_find("wlan0")`锛宍dhcp_start`锛岀瓑 `dhcp_is_bound`銆?9. 鎵撳嵃 IP锛岃繑鍥炪€?
**AP 娴佺▼**锛圖1锛夛細

1. 娉ㄥ唽 AP 浜嬩欢鍥炶皟銆?2. `HotspotConfig`锛歋SID/PSK/WPA2/2.4G/淇￠亾 7銆?3. `SetHotspotConfig` 鈫?`EnableHotspot` 鈫?`IsHotspotActive`銆?4. `netifapi_netif_find("ap0")`锛岃 IP 192.168.1.1/24锛宍netifapi_dhcps_start`銆?5. `socket(AF_INET, SOCK_DGRAM)` 鈫?`bind(8888)` 鈫?`recvfrom` 鈫?`sendto` 鍥炴樉銆?
**娉ㄦ剰**锛?
- 鍙敮鎸?2.4 GHz锛? GHz SSID 鎵笉鍒般€?- `WifiConnect` 閲?`malloc` 鐨?`info` 娌℃湁 `free`锛屾瘡娆¤皟鐢ㄦ硠婕忕害 `sizeof(WifiScanInfo)*WIFI_SCAN_HOTSPOT_LIMIT`銆?- 鎵句笉鍒扮洰鏍?SSID 鏃?`while(1) osDelay(100)` 姝荤瓑锛屼笉浼氳繑鍥烇紱浜у搧浠ｇ爜搴斿姞瓒呮椂/閲嶈瘯銆?
### 6.8 Socket / MQTT / 浜戝钩鍙?
| 绀轰緥 | 鍗忚 | 鏈嶅姟鍣?| 鍏抽敭 API |
|---|---|---|---|
| D1 | UDP 鏈嶅姟绔?| 鏉垮瓙 192.168.1.1:8888 | `socket/bind/recvfrom/sendto` |
| D3 | UDP 瀹㈡埛绔?| 192.168.0.175:8888 | `socket/sendto/recvfrom` |
| D4 | TCP 鏈嶅姟绔?| 鏉垮瓙 :8888 | `socket/bind/listen/accept/recv/send` |
| D5 | MQTT | 192.168.0.176:1883 | Paho `MQTTClientInit/Connect/Subscribe/Publish` |
| D6 | 鍗庝负 IoTDA | 117.78.5.125:1883 | 鑷畾涔?`oc_mqtt_profile_*` + Paho |
| D7 | OneNET | 183.230.40.39:6002 | Paho + `$dp` 鑷畾涔夎礋杞?|
| D8鈥揇13 | 鍗庝负 IoTDA | 117.78.5.125:1883 | `iot_link` 鐨?`oc_mqtt_profile_*` |

**D6 鏁版嵁妯″瀷**锛?
- 鏈嶅姟 `Agriculture`
- 灞炴€э細`Temperature`銆乣Humidity`銆乣Luminance`銆乣LightStatus`銆乣MotorStatus`
- 鍛戒护锛歚Agriculture_Control_light`锛堝弬鏁?`Light`锛夈€乣Agriculture_Control_Motor`锛堝弬鏁?`Motor`锛?- 涓婃姤 Topic锛歚$oc/devices/{device_id}/sys/properties/report`
- 鍛戒护鍝嶅簲 Topic锛歚$oc/devices/{device_id}/sys/commands/response/request_id={id}`

**D7 鏁版嵁妯″瀷**锛?
- 鏁版嵁娴侊細`Temperature`銆乣Humidity`銆乣Luminance`
- Topic锛歚$dp`
- 璐熻浇锛歚0x03 + len_hi + len_lo + JSON`锛坄{"Temperature":25}`锛?
**D8鈥揇13 鏁版嵁妯″瀷**锛?
| 绀轰緥 | service_id | 灞炴€?| 鍛戒护 |
|---|---|---|---|
| D8 | `Smoke` | `Smoke_Value`锛堝瓧绗︿覆锛夈€乣BeepStatus` | `Smoke_Control_Beep` |
| D9 | `Light` | `Luminance`锛坕nt锛夈€乣LightStatus` | `Light_Control_Led` |
| D10 | `Manhole_Cover` | `Temperature`銆乣Accel_x/y/z`銆乣Cover_Status`锛圱ilt/Level锛?| 鏃?|
| D11 | `Infrared` | `Infrared_Status`锛圛ntrude/Safe锛?| 鏃?|
| D12 | `Agriculture` | `Temperature`銆乣Humidity`銆乣Luminance`銆乣LightStatus`銆乣MotorStatus` | `Agriculture_Control_light`銆乣Agriculture_Control_Motor` |
| D13 | `Track` | `Longitude`銆乣Latitude`銆乣BeepStatus` | `Track_Control_Beep` |

> D8鈥揇13 閮芥槸 **鏄庢枃 1883锛屾棤 DTLS**锛沗connect_para.security.type = EN_DTLS_AL_SECURITY_TYPE_NONE`銆傞噺浜ц涓?TLS/DTLS 鏃讹紝闇€瑕佹敼 `dtls_al` 閰嶇疆鍜岃瘉涔︺€?
### 6.9 Flash

**鎺ュ彛**锛歚FlashRead(offset, size, buf)`銆乣FlashWrite(offset, size, buf, doErase)`銆乣FlashErase(offset, size)`銆?
- `offset` 鏄?Flash 鍋忕Щ锛屼笉鏄?CPU 鍦板潃锛?- `FlashErase` 鐨?`size` 蹇呴』鏄?4000 瀛楄妭鐨勫€嶆暟锛堝ご鏂囦欢娉ㄩ噴锛夛紱
- 鍐欏墠濡傞渶鎿﹂櫎锛宍doErase=1`銆?
**Z2 绀轰緥**锛?
```c
in_flash_write(0x600000 - 200, str, strlen(str) + 1);
in_flash_read(0x600000 - 200, buf, 200);
```

瀹為檯鍋忕Щ = `0x600000 - 200 - 0x400000 = 0x1FFF38`锛岃惤鍦?BOOT_BACK 鍒嗗尯銆?*涓嶈鐓ф妱**锛涘缓璁敤 `USER_RESERVE`锛?x1F0000锛?0 KB锛夋垨 `kv_store`銆?
---

## 7. 鍏抽敭鍙橀噺銆佸畯瀹氫箟涓庝腑鏂?鍥炶皟

### 7.1 鍏抽敭瀹?
| 瀹?| 鍊?| 鏂囦欢 | 浣滅敤 |
|---|---|---|---|
| `AP_SSID` | `"BearPi"` | `wifi_ap.c:54` | D1 鐑偣鍚?|
| `AP_PSK` | `"0987654321"` | `wifi_ap.c:56` | D1 鐑偣瀵嗙爜 |
| `SELECT_WIFI_SSID` | `"BearPi"` | `wifi_sta_connect.c:51` | D2 鐩爣 SSID |
| `SELECT_WIFI_PASSWORD` | `"0987654321"` | `wifi_sta_connect.c:52` | D2 瀵嗙爜 |
| `_PROT_` | `8888` | D3/D4 | UDP/TCP 绔彛 |
| `TCP_BACKLOG` | `10` | `tcp_server_demo.c:26` | TCP 鐩戝惉闃熷垪 |
| `CLIENT_ID` / `USERNAME` / `PASSWORD` | 鍗庝负浜戣澶囦笁鍏冪粍 | `D6/iot_cloud_oc_sample.c:40-42` | D6 鎺ュ叆 |
| `CONFIG_APP_SERVERIP` | `"117.78.5.125"` | D8鈥揇13 | 鍗庝负浜戞爣鍑嗙増 |
| `CONFIG_APP_SERVERPORT` | `"1883"` | D8鈥揇13 | MQTT 鏄庢枃绔彛 |
| `CONFIG_APP_DEVICEID` / `CONFIG_APP_DEVICEPWD` | 璁惧 ID/瀵嗛挜 | D8鈥揇13 | 姣忓彴璁惧涓嶅悓 |
| `ONENET_INFO_DEVID` / `AUTH` / `APIKEY` | OneNET 璁惧淇℃伅 | `D7/iot_cloud_onenet_sample.c:28-30` | D7 鎺ュ叆 |
| `TEXT` / `WEB` | `"Welcome to BearPi-HM_Nano!"` / `"harmonyos.com"` | `i2c_example.c:55-57` | B5 鍐欏叆 NFC |
| `PWM_TASK_STACK_SIZE` | 512锛圔3 瀹為檯鐢?4096锛?| `pwm_example.c:26,71` | B3 鏍?|
| `ADC_TASK_STACK_SIZE` | `1024*8` | `adc_example.c:49` | B4 鏍?|
| `UART_BUFF_SIZE` | 1000 | `uart_example.c:57` | B6 鎺ユ敹缂撳啿 |
| `CAL_PPM` / `RL` | 20 / 1 | `E53_SF1.c:27-28` | MQ2 鏍″噯 |
| `SHT30_Addr` / `BH1750_Addr` | 0x44 / 0x23 | `E53_IA1.h:40-42` | I2C 鍦板潃 |
| `MPU6050_SLAVE_ADDRESS` | 0x68 | `E53_SC2.h:38` | MPU6050 鍦板潃 |
| `MSGQUEUE_OBJECTS` | 16 | A6/D6 | 闃熷垪娣卞害 |
| `FLAGS_MSK1` | `0x00000001U` | C5/D11 | 浜嬩欢浣?0 |
| `UART_TIMEOUT_MS` | 20 | Z1 | 涓插彛璇昏秴鏃?|
| `CONFIG_QUEUE_TIMEOUT` | `5*1000` | D8鈥揇13 | 鍏ラ槦瓒呮椂锛坢s锛?|

### 7.2 鍏抽敭鍏ㄥ眬鍙橀噺

| 鍙橀噺 | 绫诲瀷 | 鏂囦欢 | 浣滅敤 |
|---|---|---|---|
| `threadHiID` / `threadLoID` | `osThreadId_t` | A1 | 绾跨▼鍙ユ焺 |
| `exec1` / `exec2` | `uint32_t` | A2 | 瀹氭椂鍣ㄥ洖璋冨弬鏁?|
| `evtAny` / `evtAll` | `osEventFlagsId_t` | A3 | 涓や釜浜嬩欢缁?|
| `mutex_id` | `osMutexId_t` | A4 | 浜掓枼閿?|
| `sem1` | `osSemaphoreId_t` | A5 | 淇″彿閲?|
| `mid_MsgQueue` | `osMessageQueueId_t` | A6 | 娑堟伅闃熷垪 |
| `g_wifiEventHandler` | `WifiEvent` | D1/D2/wifi_connect | Wi-Fi 鍥炶皟琛?|
| `g_lwip_netif` | `struct netif *` | D1/D2 | lwIP 缃戝崱 |
| `g_apEnableSuccess` | `int` | D1 | 杩炲叆 STA 璁℃暟 |
| `g_staScanSuccess` / `g_ConnectSuccess` | `int` | D2/wifi_connect | 鎵弿/杩炴帴瀹屾垚鏍囧織 |
| `ssid_count` | `int` | D2/wifi_connect | 鎵弿鍒扮殑 AP 鏁?|
| `mq_client` | `MQTTClient` | D6/D7 | Paho 瀹㈡埛绔?|
| `oc_info` | `struct bp_oc_info` | D6 | 鍗庝负浜戣澶囦俊鎭?|
| `onenet_info` | `struct rt_onenet_info` | D7 | OneNET 璁惧淇℃伅 |
| `g_app_cb` | 鍚勭ず渚嬭嚜瀹氫箟 | D1/D6/D8鈥揇13 | 杩炴帴鐘舵€?LED/铚傞福鍣?闃熷垪 |
| `E53_IA1_Data` | `E53_IA1_Data_TypeDef` | C2/D7 | 娓╂箍搴?鍏夌収 |
| `E53_SC2_Data` | `E53_SC2_Data_TypeDef` | C4/D10 | 娓╁害/鍔犻€熷害 |
| `Flower_Data` | `Flower_Data_TypeDef` | C6 | 鍦熷￥/鍏夌収/娓╂箍搴?|
| `gpsmsg` / `gps_uart` | `gps_msg` / `unsigned char[1000]` | D13 | GPS 瑙ｆ瀽缁撴灉/鎺ユ敹缂撳啿 |
| `Infrared_Status` | `int` | D11 | 浜轰綋鎰熷簲鐘舵€?|
| `Cover_Status` | `int` | D10 | 浜曠洊鍊炬枩鐘舵€?|
| `X/Y/Z` | `int` | C4/D10 | 鍔犻€熷害鍩哄噯 |
| `R0` | `float` | C1 | MQ2 娲佸噣绌烘皵闃诲€?|

### 7.3 涓柇/鍥炶皟娓呭崟

| 鍥炶皟 | 娉ㄥ唽浣嶇疆 | 瑙﹀彂鏉′欢 | 涓婁笅鏂?娉ㄦ剰 |
|---|---|---|---|
| `F1_Pressed` | `button_example.c:50` | GPIO11 涓嬮檷娌?| GPIO 涓柇锛涚洿鎺ョ偣鐏?`printf`锛屽伐绋嬩笂寤鸿鍙疆浜嬩欢 |
| `F2_Pressed` | `button_example.c:57` | GPIO12 涓嬮檷娌?| 鍚屼笂 |
| `Beep_Alarm` | `E53_IS1.c:67` / D11 | GPIO7 涓婂崌娌?| 鍙?`osEventFlagsSet`锛岀嚎绋嬪鐞嗚渹楦?|
| `Timer1_Callback` | `Timer_example.c:92` | 瀹氭椂鍣?1 鍒扮偣 | 杞欢瀹氭椂鍣ㄤ笂涓嬫枃锛沗printf` 浠呮暀瀛?|
| `Timer2_Callback` | `Timer_example.c:105` | 瀹氭椂鍣?2 鍒扮偣 | 鍚屼笂 |
| `OnHotspotStaJoinHandler` | D1 `wifi_ap.c:88` | STA 杩炲叆 AP | Wi-Fi 浜嬩欢鍥炶皟锛涘垱寤虹嚎绋嬪鐞嗗垪琛?|
| `OnHotspotStaLeaveHandler` | D1 `wifi_ap.c:89` | STA 绂诲紑 AP | 鎵撳嵃 MAC/鍘熷洜锛岃鏁板噺涓€ |
| `OnHotspotStateChangedHandler` | D1 `wifi_ap.c:90` | AP 鐘舵€佸彉鍖?| 鎵撳嵃鐘舵€?|
| `OnWifiScanStateChangedHandler` | D2/wifi_connect | 鎵弿瀹屾垚 | 缃?`g_staScanSuccess`锛岃褰?AP 鏁?|
| `OnWifiConnectionChangedHandler` | D2/wifi_connect | STA 杩炴帴鐘舵€佸彉鍖?| 缃?娓?`g_ConnectSuccess` |
| `mqtt_callback` | D6 `oc_mqtt.c:72` | 鏀跺埌 MQTT 娑堟伅 | 璋?`cmd_rsp_cb`锛岀粍 `$crsp/...` 鍝嶅簲 |
| `oc_cmd_rsp_cb` | D6 `iot_cloud_oc_sample.c:124` | 浜戠鍛戒护涓嬪彂 | 鍏ラ槦锛沗request_id` 鏈祴鍊兼槸缂洪櫡 |
| `msg_rcv_callback` | D8/D9/D12/D13 | 浜戠鍛戒护涓嬪彂 | 鎷疯礉 request_id/payload 鍏ラ槦锛汥10/D11 鐨?`rcvfunc=NULL`锛屼笉鏀跺懡浠?|
| `Beep_Alarm` | D11 | GPIO7 涓婂崌娌?| 鍚?C5 |
| MPU6050 杩愬姩/鑷敱钀戒綋涓柇 | `E53_SC2.c:243-257` | 閰嶇疆浜嗗瘎瀛樺櫒锛屼絾**娌℃湁娉ㄥ唽 GPIO 涓柇澶勭悊** | 浠呴厤缃紝鏈娇鐢?|

### 7.4 绾跨▼/闃熷垪/瀹氭椂鍣ㄨ祫婧?
| 璧勬簮 | 鏁伴噺/鍙傛暟 | 璇存槑 |
|---|---|---|
| CMSIS 绾跨▼ | 姣忎釜绀轰緥 1鈥? 涓?| 鏍?512 B鈥?0 KB锛屼紭鍏堢骇 15鈥?7 |
| 杞欢瀹氭椂鍣?| A2 涓や釜 | 100 tick/300 tick |
| 浜嬩欢鏍囧織缁?| A3 涓や釜锛汣5/D11 涓€涓?| 32 浣嶄綅鍥?|
| 浜掓枼閿?| A4 涓€涓?| 甯︿紭鍏堢骇缁ф壙 |
| 淇″彿閲?| A5 涓€涓?| 鏈€澶?1銆佸垵濮?1 |
| 娑堟伅闃熷垪 | A6 16 鏉★紱D6 16 鏉∶?0 瀛楄妭 | D6 鏉＄洰澶у皬鏈夐闄?|
| iot_link queue | D8鈥揇13 10 鏉?| `queue_create(...,10,1)`锛屽瓨鎸囬拡 |

---

## 8. 宸插彂鐜扮殑闂涓庝簩娆″紑鍙戦闄?
> 浠ヤ笅鎸夆€滀細褰卞搷鍔熻兘/绋冲畾鎬р€濈殑绋嬪害鎺掑簭銆傛暀瀛︾ず渚嬩腑鐨?`printf`銆佺‖缂栫爜瀵嗙爜绛変笉鍏ㄦ槸 bug锛屼絾鍦ㄤ骇鍝佸寲鏃惰澶勭悊銆?
### 8.1 楂樹紭鍏堢骇

1. **D12 鐢垫満鍛戒护姘歌繙澶辫触**  
   `Agriculture_Control_Motor` 鍒嗘敮鍙栫殑鏄?`"Paras"`锛堝ぇ鍐?P锛夛紝鑰?IoTDA 涓嬪彂鐨勬槸 `"paras"`锛涘悓涓€鏂囦欢鐨勭伅鍏夊懡浠ょ敤鐨勬槸灏忓啓銆傜粨鏋?`obj_paras == NULL`锛岀洿鎺ヨ烦鍒伴敊璇嚭鍙ｏ紝`ret_code=1`銆? 
   浣嶇疆锛歔D12 iot_cloud_oc_sample.c:228-236](applications/BearPi/BearPi-HM_Nano/sample/D12_iot_cloud_oc_agriculture/iot_cloud_oc_sample.c#L228-L236)銆侱6 涔熸湁鍚屾牱闂锛坄:194`锛夈€?
2. **D8 鐑熸劅鍊肩紦鍐插尯婧㈠嚭**  
   `char smokevalue[5]`锛屼絾 `sprintf("%.3f")` 鏈€鍧忎細鍐?7 涓瓧绗?NUL锛堝 `123.456`锛夛紝瓒婄晫鍐欏爢銆? 
   浣嶇疆锛歔D8 iot_cloud_oc_sample.c:65](applications/BearPi/BearPi-HM_Nano/sample/D8_iot_cloud_oc_smoke/iot_cloud_oc_sample.c#L65)銆乕`:296`](applications/BearPi/BearPi-HM_Nano/sample/D8_iot_cloud_oc_smoke/iot_cloud_oc_sample.c#L296)銆傚缓璁?`char smokevalue[16]` + `snprintf`銆?
3. **D13 GPS 缂撳啿鍖?瀛楃涓查闄?*  
   - `gps_uart[1000]` 璇绘弧鍚庢病鏈?NUL 缁撳熬灏?`strstr`锛屽彲鑳借秺鐣岃锛? 
   - `Latitude[9]`/`Longitude[10]` 鍒氬ソ鍙 `"%.5f"`锛岃В鏋愬紓甯告椂浼氭孩鍑猴紱  
   - 鐢ㄤ綅涓?`&` 浠ｆ浛閫昏緫涓?`&&`锛屾潯浠朵笉浼氱煭璺紱  
   - 鏃犲畾浣嶆椂 `app_msg` 娉勬紡銆? 
   浣嶇疆锛歔D13 iot_cloud_oc_sample.c:65-66](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/iot_cloud_oc_sample.c#L65-L66)銆乕`:298-307`](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/iot_cloud_oc_sample.c#L298-L307)銆乕E53_ST1.c:212-215](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/src/E53_ST1.c#L212-L215)銆傚缓璁紦鍐插尯鐣欎綑閲忋€佽鍚?`buf[read_len]='\0'`銆佹牎楠?NMEA 鍜?`A/V` 鐘舵€併€?
4. **C4/D10 MPU6050 ID 澶辫触浼氭寰幆**  
   `E53_SC2_Read_Data()` 閲?`if (MPU6050ReadID() == 0) { while(1); }`锛屼紶鎰熷櫒鏈帴/鍦板潃閿欐椂鏁存満鍗℃锛岀湅闂ㄧ嫍鍙兘澶嶄綅銆? 
   浣嶇疆锛歔C4 E53_SC2.c:332-335](applications/BearPi/BearPi-HM_Nano/sample/C4_e53_sc2_axis/src/E53_SC2.c#L332-L335)銆乕D10 鍚屾枃浠禲(applications/BearPi/BearPi-HM_Nano/sample/D10_iot_cloud_oc_manhole_cover/src/E53_SC2.c#L332-L335)銆傚缓璁繑鍥為敊璇爜锛岀敱涓婂眰閲嶈瘯/涓婃姤銆?
5. **D6 CMSIS 娑堟伅闃熷垪鏉＄洰澶у皬涓嶅尮閰?*  
   `osMessageQueueNew(MSGQUEUE_OBJECTS, 10, NULL)` 鍒涘缓 10 瀛楄妭鏉＄洰锛屼絾 `osMessageQueuePut/Get` 浼犵殑鏄?`app_msg_t *`锛? 瀛楄妭鎸囬拡锛夈€侾ut 浼氫粠鎸囬拡鍙橀噺鍦板潃鎷疯礉 10 瀛楄妭锛孏et 浼氬線鎸囬拡鍙橀噺鍐?10 瀛楄妭锛岃秺鐣岃俯鏍堛€? 
   浣嶇疆锛歔D6 iot_cloud_oc_sample.c:295](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/iot_cloud_oc_sample.c#L295)銆乕`:134`](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/iot_cloud_oc_sample.c#L134)銆乕`:247`](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/iot_cloud_oc_sample.c#L247)銆傚簲鏀逛负 `sizeof(app_msg_t *)`锛屾垨鐩存帴浼犵粨鏋勪綋銆?
6. **D6 鍛戒护鍝嶅簲 `request_id` 鏈垵濮嬪寲**  
   `oc_cmd_rsp_cb` 鍙缃簡 `msg.cmd.payload`锛屾病鏈夎缃?`request_id`锛沗deal_cmd_msg` 鍗存妸瀹冧紶缁?`cmdresp.request_id`锛屽搷搴?Topic 浼氭嫾鍒伴殢鏈哄€笺€? 
   浣嶇疆锛歔D6 iot_cloud_oc_sample.c:124-141](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/iot_cloud_oc_sample.c#L124-L141)銆乕`:226-230`](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/iot_cloud_oc_sample.c#L226-L230)銆傚簲浠?`recv_data` 瀵瑰簲鐨?Topic/鍥炶皟鍙傛暟鍙?request_id锛屾垨鏀圭敤 D8鈥揇13 鐨?`msg_rcv_callback` 妯″紡銆?
7. **D13 鍗犵敤 UART0_RXD锛圙PIO4锛?*  
   `Init_E53_ST1()` 鎶?GPIO4 璁句负鏅€氳緭鍑哄苟鎷変綆锛岃€?GPIO4 鏄皟璇曚覆鍙?UART0 鐨?RX銆傜粨鏋滐細鏃ュ織鑳芥墦鍗帮紙TX 姝ｅ父锛夛紝浣嗕覆鍙ｅ姪鎵嬪彂鐨勫懡浠ゆ敹涓嶅埌锛屼笖鍙兘褰卞搷鐑у綍/AT銆? 
   浣嶇疆锛歔E53_ST1.c:79-81](applications/BearPi/BearPi-HM_Nano/sample/D13_iot_cloud_oc_gps/src/E53_ST1.c#L79-L81)銆傚鏋滅‖浠剁‘瀹為渶瑕佽繖鏍硅剼锛屽缓璁敼鏉挎垨鏀瑰紩鑴氥€?
### 8.2 涓紭鍏堢骇

8. **A2 瀹氭椂鍣?1 閲嶅惎鍛ㄦ湡鐢ㄩ敊鍙橀噺**  
   `timerDelay` 鍏堣涓?100锛坱imer1锛夛紝鍐嶈涓?300锛坱imer2锛夛紱鍚庨潰 `osTimerStart(id1, timerDelay)` 澶嶇敤浜?300锛屽鑷?timer1 閲嶅惎鍚庡彉 3 s銆? 
   浣嶇疆锛歔Timer_example.c:95-127](applications/BearPi/BearPi-HM_Nano/sample/A2_kernel_timer/Timer_example.c#L95-L127)銆傞噸鍚椂搴旈噸鏂拌祴鍊?100銆?
9. **D6/D7 鐨?`init_ok` 姘歌繙涓?0**  
   鍒濆鍖栨垚鍔熷悗浠ｇ爜鍐欑殑鏄?`init_ok = 0`锛岃€屼笉鏄?1锛涢噸澶嶈皟鐢?`oc_mqtt_init()`/`onenet_mqtt_init()` 浼氶噸澶嶅缓閾?娉勬紡銆? 
   浣嶇疆锛歔D6 oc_mqtt.c:180-184](applications/BearPi/BearPi-HM_Nano/sample/D6_iot_cloud_oc/src/oc_mqtt.c#L180-L184)銆乕D7 onenet_mqtt.c:238-243](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/src/onenet_mqtt.c#L238-L243)銆?
10. **D7 `device_info_init` 鍙兘鍐欏彧璇诲瓧绗︿覆**  
    `strncpy(api_key, master_api_key, ...)` 鐨?`api_key` 鏄叆鍙傛寚閽堬紱濡傛灉浼犲叆鐨勬槸瀛楃涓插瓧闈㈤噺锛堝畯 `ONENET_INFO_APIKEY`锛夛紝鐭瘑閽ユ椂浼氬啓鍙娈点€? 
    浣嶇疆锛歔D7 onenet_mqtt.c:189-202](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/src/onenet_mqtt.c#L189-L202)銆傚簲鏀圭敤鏈湴鏁扮粍/`snprintf`銆?
11. **Wi-Fi 杩炴帴鍑芥暟鐨勫唴瀛樻硠婕忎笌姝荤瓑**  
    `WifiConnect` 閲?`malloc(sizeof(WifiScanInfo)*WIFI_SCAN_HOTSPOT_LIMIT)` 娌￠噴鏀撅紱鎵句笉鍒?SSID 鏃?`while(1) osDelay(100)`锛屼笉浼氳繑鍥炪€? 
    浣嶇疆锛歔wifi_connect.c:80-83](applications/BearPi/BearPi-HM_Nano/sample/D3_iot_udp_client/src/wifi_connect.c#L80-L83)銆乕`:135-139`](applications/BearPi/BearPi-HM_Nano/sample/D3_iot_udp_client/src/wifi_connect.c#L135-L139)銆備骇鍝佷唬鐮佸簲鍔犺秴鏃躲€侀噸璇曘€侀噴鏀俱€?
12. **D4 TCP 鎺ユ敹缂撳啿鍖烘湭淇濊瘉 NUL 缁撳熬**  
    `recv(new_fd, recvbuf, sizeof(recvbuf), 0)` 鍚庣洿鎺?`printf("%s", recvbuf)`锛涘鏋滄敹鍒扮殑鏁版嵁娌℃湁 NUL锛屼細瓒婄晫璇汇€? 
    浣嶇疆锛歔tcp_server_demo.c:101-105](applications/BearPi/BearPi-HM_Nano/sample/D4_iot_tcp_server/tcp_server_demo.c#L101-L105)銆傚簲鎸夎繑鍥炲€艰ˉ `recvbuf[ret]='\0'`銆?
13. **D7/D12 浼犳劅鍣ㄤ笌涓婃姤绾跨▼鏃犲悓姝?*  
    D7 鐨?`Sensor_Read_Task` 鍐欏叏灞€ `E53_IA1_Data`锛宍MQTT_Report_Task` 鍚屾椂璇伙紝娌℃湁浜掓枼/闃熷垪锛汥12 鐨勪紶鎰熷櫒绾跨▼涓庝富绾跨▼涔熷叡浜?`E53_IA1_Data` 绫讳技銆? 
    浣嶇疆锛歔D7 iot_cloud_onenet_sample.c:47-82](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/iot_cloud_onenet_sample.c#L47-L82)銆傚缓璁敤娑堟伅闃熷垪浼犻€掑揩鐓э紝鎴栧姞浜掓枼閿併€?
14. **D10/D11/D12/D13 娌℃湁鏂嚎閲嶈繛**  
    `oc_mqtt_profile_connect` 澶辫触鍙墦鍗帮紝涓嶉噸璇曪紱Wi-Fi 鎺夌嚎鍚庝笉浼氶噸杩炪€備骇鍝佸寲闇€瑕佺姸鎬佹満 + 閲嶈繛 + 蹇冭烦銆?
15. **D8鈥揇13 閮芥槸鏄庢枃 1883**  
    `EN_DTLS_AL_SECURITY_TYPE_NONE`锛屾病鏈?TLS锛涘叕缃戦儴缃插繀椤诲惎鐢?DTLS/TLS锛屽苟澶勭悊璇佷功/鏃堕棿銆?
### 8.3 浣庝紭鍏堢骇/浠ｇ爜鏁存磥

16. **澶ч噺閲嶅椹卞姩鍓湰**锛歚wifi_connect.c` 鍦?D3/D4/D5/D6/D7/D8鈥揇13 鍚勪竴浠斤紱`E53_IA1.c`銆乣E53_SC1.c`銆乣E53_SC2.c`銆乣E53_IS1.c`銆乣E53_SF1.c` 鍦?C 绯诲垪鍜?D 绯诲垪鍚勪竴浠斤紝涓旂鍚嶅凡鍒嗗弶锛圕2 鐨?`E53_IA1_Read_Data(void)` vs D6/D12 鐨勬寚閽堝弬鏁帮級銆傛敼涓€涓?bug 瑕佹敼澶氬銆?
17. **娉ㄩ噴涓庝唬鐮佷笉涓€鑷?*锛欳1 娉ㄩ噴鍐?GPIO_3/PWM5锛屽疄闄?GPIO8/PWM1锛汣2 娉ㄩ噴鍐?GPIO_2锛屽疄闄?GPIO8/14锛汣3 娉ㄩ噴鍐?GPIO_2锛屽疄闄?GPIO7锛汢5 README 鎶?SCL/SDA 鍐欏弽锛汣5 澶存枃浠?guard 鍐欐垚 `__E53_IS2_H__`銆?
18. **`Zx_Developer` 妯℃澘涓嶅彲缂栬瘧**锛氭病鏈?`#include`锛宍ZX_Demo` 鏈畾涔夛紝`APP_FEATURE_INIT` 閲?`while(1);`銆備粎浣滅洰褰曠粨鏋勫弬鑰冿紝涓嶈鐩存帴鍚敤銆?
19. **C6 娌℃湁鍑虹幇鍦?`sample/BUILD.gn`**锛氶渶瑕佹墜鍔ㄥ姞 `C6_e53_flower_ia1:e53_flower_ia1_example`锛屽惁鍒欐棤娉曠紪璇戙€?
20. **B1 绾跨▼鏍?512 B 鍋忓皬**锛歚printf` 鍦ㄩ儴鍒?libc 瀹炵幇涓嬪悆鏍堬紱B3 宸蹭粠 512 鏀规垚 4096 骞舵敞閲婅鏄庯紝鍏朵粬绀轰緥鑻ュ姞鏃ュ織寤鸿 鈮? KB銆?
21. **`sample/BUILD.gn` 褰撳墠鏄?D1锛宍out/` 鏄?B2**锛氭渶瀹规槗琚鍒や负鈥滀唬鐮佹病鐢熸晥鈥濈殑鍘熷洜锛涙瘡娆℃敼瀹岄€夋嫨鍣ㄥ繀椤婚噸鏂?`python build.py` 骞剁‘璁?`build.log` 閲屽嚭鐜扮洰鏍囩ず渚嬬殑 `.o`銆?
---

## 9. 棰勭暀鎺ュ彛涓庡彲鎵╁睍鐐逛綅

### 9.1 纭欢鍙墿灞曠偣浣?
| 璧勬簮 | 鍙敤鎬?| 寤鸿 |
|---|---|---|
| GPIO13 | 鑺墖渚ф湭鍗犵敤 | 浼樺厛鍋氭柊鎸夐敭/涓柇/鐗囬€夛紱鏄惁寮曞嚭鐪嬪師鐞嗗浘 |
| GPIO5/6锛圲ART1锛?| B6/D13/Z1 鐢紱C6 鍗?GPIO5 | 鍋?GPS/涓插彛妯″潡鏃剁敤锛涗笉瑕佷笌 C6 姘存车鍚屾椂鐢?|
| GPIO9/10锛圛2C0锛?| C6 鐢紱鍏朵粬绀轰緥鏈敤 | 鍙寕绗簩璺?I2C 浼犳劅鍣紙娉ㄦ剰鍦板潃鍐茬獊锛?|
| GPIO0/1锛圛2C1锛?| NFC/E53 鍏辩敤 | 鍙寕澶氫釜涓嶅悓鍦板潃鐨?I2C 浠庢満锛涗笉瑕佷笌 NFC 鍐欐椂搴忓啿绐?|
| GPIO7/8/14 | E53 鎵ц鍣?浼犳劅鍣ㄥ崰鐢?| 鍋?E53 鎵╁睍鏃朵紭鍏堝鐢紱鍋氭澘杞藉姛鑳芥椂閬垮紑 |
| ADC2 | 鏈娇鐢?| 鍙帴绗簩璺ā鎷熶紶鎰熷櫒锛堥渶纭 E53 寮曞嚭锛?|
| ADC0/1/3/4/7 | 杞欢鏈娇鐢?| 闇€鏌ュ師鐞嗗浘纭寮曡剼 |
| PWM0/3/4/5 | 鏈娇鐢?| 鍙仛 RGB/鐢垫満/铚傞福鍣紱闇€ `IoSetFunc` 鏄犲皠 |
| SPI0/1 | 鏈娇鐢?| 鍙帴 SPI 灞?Flash/浼犳劅鍣紱娉ㄦ剰涓?I2C0/1 寮曡剼澶嶇敤 |
| I2S | 鏈娇鐢?| 鍙帴闊抽 codec |
| SDIO | 鏈娇鐢?| 鍙帴 SD 鍗?Wi-Fi 妯″潡 |
| USER_RESERVE 鍒嗗尯 | 20 KB | 瀛橀厤缃?鏍″噯鍊硷紱姣?Z2 鐨?BOOT_BACK 瀹夊叏 |
| E53 3.3 V/5 V | 鏈?| 娉ㄦ剰 5 V 鍣ㄤ欢鐢靛钩鍜岀數娴?|

### 9.2 杞欢鎵╁睍鐐?
1. **鏂板绀轰緥**  
   澶嶅埗涓€涓渶鎺ヨ繎鐨勭洰褰曪紝鏀?`BUILD.gn` 鐨?`static_library` 鍚嶅拰 `sources`锛屽湪 `sample/BUILD.gn` 涓彧淇濈暀鏂扮洰鏍囥€傛ā鏉匡細

   ```c
   #include <stdio.h>
   #include <unistd.h>
   #include "ohos_init.h"
   #include "cmsis_os2.h"
   #include "wifiiot_gpio.h"
   #include "wifiiot_gpio_ex.h"

   static void MyTask(void *arg) {
       (void)arg;
       GpioInit();
       IoSetFunc(WIFI_IOT_IO_NAME_GPIO_13, WIFI_IOT_IO_FUNC_GPIO_13_GPIO);
       GpioSetDir(WIFI_IOT_GPIO_IDX_13, WIFI_IOT_GPIO_DIR_OUT);
       while (1) {
           GpioSetOutputVal(WIFI_IOT_GPIO_IDX_13, 1);
           usleep(500000);
           GpioSetOutputVal(WIFI_IOT_GPIO_IDX_13, 0);
           usleep(500000);
       }
   }

   static void MyEntry(void) {
       osThreadAttr_t attr = {0};
       attr.name = "MyTask";
       attr.stack_size = 4096;
       attr.priority = 25;
       osThreadNew((osThreadFunc_t)MyTask, NULL, &attr);
   }
   APP_FEATURE_INIT(MyEntry);
   ```

2. **澶嶇敤 Wi-Fi 杩炴帴**  
   鎶?`wifi_connect.c/h` 鎶藉埌鍏叡鐩綍锛孌 绯诲垪缁熶竴寮曠敤锛涘鍔犺秴鏃?閲嶈瘯/浜嬩欢鍥炶皟銆?
3. **澶嶇敤 E53 椹卞姩**  
   鎶?`E53_*` 鎶藉埌 `components/e53`锛岀粺涓€ `Init/Read/Control` 鎺ュ彛锛岄伩鍏?C/D 涓や唤鍒嗗弶銆?
4. **涓柇鍒扮嚎绋嬬殑鏍囧噯妯″紡**  
   ISR 鍙?`osEventFlagsSet`/`osMessageQueuePut`锛岀嚎绋嬮噷澶勭悊涓氬姟锛涘弬鑰?C5/D11銆?
5. **浜戝钩鍙版墿灞?*  
   - 鏂板灞炴€э細寰€ `oc_mqtt_profile_kv_t` 閾捐〃鍔犺妭鐐癸紝濉?`key/type/value/nxt`锛? 
   - 鏂板鍛戒护锛氬湪 `deal_cmd_msg` 閲屽姞 `command_name` 鍒嗘敮锛岃繑鍥?`cmdresp.ret_code`锛? 
   - 鏂板鏈嶅姟锛氭敼 `service_id` 鍜屽睘鎬ц〃锛? 
   - 鏂嚎閲嶈繛锛氬湪 `task_main_entry` 澶栧眰鍔犵姸鎬佹満锛宍oc_mqtt_profile_disconnect` 鍚庨噸杩炪€?
6. **鎸佷箙鍖?*  
   鐢?`utils/native/lite/kv_store` 鎴?`file` 鎺ュ彛锛屼笉瑕佺洿鎺ュ啓瑁?Flash锛涘鏋滃繀椤诲啓锛屼娇鐢?`USER_RESERVE` 骞跺姞 CRC/鍙屽浠姐€?
7. **鍚姩椤哄簭**  
   澶氫釜 feature 闇€瑕侀『搴忔椂鐢?`APP_FEATURE_INIT_PRI(func, 0..4)`锛沗SYS_RUN` 鏇存棭锛屼絾姝ゆ椂绯荤粺鏈嶅姟鍙兘鏈氨缁紝閫傚悎绾墦鍗?鏈€鏃╁垵濮嬪寲銆?
### 9.3 寤鸿鐨勪簩娆″紑鍙戠洰褰?
```text
applications/BearPi/BearPi-HM_Nano/sample/
鈹溾攢鈹€ X1_my_product/
鈹?  鈹溾攢鈹€ BUILD.gn
鈹?  鈹溾攢鈹€ include/
鈹?  鈹?  鈹斺攢鈹€ my_product.h
鈹?  鈹斺攢鈹€ src/
鈹?      鈹溾攢鈹€ my_product.c
鈹?      鈹溾攢鈹€ wifi_connect.c      # 鎴栧紩鐢ㄥ叕鍏辩粍浠?鈹?      鈹斺攢鈹€ e53_xxx.c           # 鎴栧紩鐢ㄥ叕鍏辩粍浠?鈹斺攢鈹€ BUILD.gn                    # 鍙惎鐢?X1_my_product
```

---

## 10. 蹇€熸帓闅滄竻鍗?
| 鐜拌薄 | 浼樺厛妫€鏌?|
|---|---|
| 涓插彛鏃犱换浣曡緭鍑?| USB 绾?CH340 椹卞姩/COM 鍙ｏ紱UART0 115200锛涙槸鍚︽寜浜?RESET锛涙槸鍚︾儳褰曟垚鍔?|
| 鐑у綍澶辫触 | HiBurn 娉㈢壒鐜?921600锛涙槸鍚︽寜 RESET锛汣OM 鍙ｆ槸鍚﹁涓插彛鍔╂墜鍗犵敤锛涙槸鍚﹂€夊 `allinone.bin` |
| 浠ｇ爜鏀逛簡娌℃晥鏋?| `sample/BUILD.gn` 鏄惁鍚敤鐩爣锛涙槸鍚﹂噸鏂扮紪璇戯紱`out/build.log` 鏄惁鍑虹幇鐩爣 `.o`锛沗out/` 鏄惁鏃т骇鐗?|
| Wi-Fi 杩炰笉涓?| 2.4 GHz SSID/瀵嗙爜锛沗WifiConnect` 鐨?`ssid` 鏄惁瀹屽叏鍖归厤锛涜矾鐢卞櫒鏄惁寮€ MAC 杩囨护锛涗覆鍙ｆ槸鍚︽墦鍗版壂鎻忓垪琛?|
| 浜戝钩鍙拌繛涓嶄笂 | 璁惧 ID/瀵嗛挜锛涙湇鍔″櫒 IP/绔彛锛涗骇鍝?鏈嶅姟/灞炴€ф槸鍚︿笌浠ｇ爜涓€鑷达紱鏄惁鏄庢枃 1883 琚綉缁滈檺鍒?|
| 浼犳劅鍣ㄨ鏁?0/涓嶅彉 | 3.3 V/5 V 渚涚數锛汭2C 涓婃媺锛涘湴鍧€锛沗IoSetFunc` 鏄惁閰嶅锛涙槸鍚﹁鍏朵粬绀轰緥鍗犵敤 |
| 铚傞福鍣ㄤ笉鍝?| GPIO8 鏄惁澶嶇敤 PWM1锛沗PwmInit` 鏄惁璋冪敤锛沗duty/freq` 鏄惁鍚堟硶锛涜渹楦ｅ櫒鏄惁 3.3 V 椹卞姩 |
| 鎸夐敭鏃犲弽搴?| GPIO11/12 涓婃媺锛涗笅闄嶆部锛涗腑鏂洖璋冩槸鍚︽敞鍐岋紱鏄惁鏈夊叾浠栫ず渚嬪崰鐢?|
| 绋嬪簭璺戦/閲嶅惎 | 鏍堟孩鍑猴紙灏ゅ叾 printf/澶ф暟缁勶級锛涚湅闂ㄧ嫍锛沗while(1)` 姝荤瓑锛涗腑鏂噷闃诲锛涘爢婧㈠嚭 |
| I2C 璇诲啓澶辫触 | 鍦板潃 7 浣?8 浣嶏紱`(addr<<1)`锛涙€荤嚎閫熺巼锛涗笂鎷夌數闃伙紱鏄惁鍚屾椂鍒濆鍖?I2C0/I2C1 |
| GPS 鏃犳暟鎹?| UART1 9600锛汿X/RX 浜ゅ弶锛涘ぉ绾?瀹ゅ锛汵MEA 鏄惁杈撳嚭锛汫PIO4 鏄惁琚?D13 鍗犵敤 |
| NFC 鎵嬫満璇讳笉鍒?| NFC 澶╃嚎鏄惁闈犺繎锛汵T3H 鍐欏叆鏄惁鎴愬姛锛汵DEF 璁板綍浣嶇疆锛涙墜鏈?NFC 寮€鍏?|

---

## 闄勫綍 A锛氬叧閿簮鐮佺储寮?
| 涓婚 | 鏂囦欢 |
|---|---|
| 绀轰緥閫夋嫨鍣?| [sample/BUILD.gn](applications/BearPi/BearPi-HM_Nano/sample/BUILD.gn) |
| 鍚姩娈靛畯 | [ohos_init.h](utils/native/lite/include/ohos_init.h) |
| 鍚姩闃舵 | [system_init.c](base/startup/services/bootstrap_lite/source/system_init.c) |
| APP_FEATURE 璋冪敤 | [bootstrap_service.c](base/startup/services/bootstrap_lite/source/bootstrap_service.c) |
| Hi3861 鍚姩 | [app_main.c](vendor/hisi/hi3861/hi3861/app/wifiiot_app/src/app_main.c) |
| 榛樿寮曡剼澶嶇敤 | [app_io_init.c](vendor/hisi/hi3861/hi3861/app/wifiiot_app/init/app_io_init.c) |
| Flash 鍒嗗尯 | [flash_partition_table.c](vendor/hisi/hi3861/hi3861/platform/system/partition_table/flash_partition_table.c) |
| 閾炬帴鑴氭湰 | [link.ld.S](vendor/hisi/hi3861/hi3861/build/link/link.ld.S) |
| GPIO 澶嶇敤鏋氫妇 | [wifiiot_gpio_ex.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_gpio_ex.h) |
| GPIO API | [wifiiot_gpio.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_gpio.h) |
| ADC API | [wifiiot_adc.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_adc.h) |
| PWM API | [wifiiot_pwm.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_pwm.h) |
| I2C API | [wifiiot_i2c.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_i2c.h) |
| UART API | [wifiiot_uart.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_uart.h) |
| Flash API | [wifiiot_flash.h](base/iot_hardware/interfaces/kits/wifiiot_lite/wifiiot_flash.h) |
| Wi-Fi STA | [wifi_device.h](foundation/communication/interfaces/kits/wifi_lite/wifiservice/wifi_device.h) |
| Wi-Fi AP | [wifi_hotspot.h](foundation/communication/interfaces/kits/wifi_lite/wifiservice/wifi_hotspot.h) |
| 鍗庝负浜?profile | [oc_mqtt_profile.h](third_party/iot_link/oc_mqtt/oc_mqtt_profile_v5/oc_mqtt_profile.h) |
| OneNET 澶存枃浠?| [onenet.h](applications/BearPi/BearPi-HM_Nano/sample/D7_iot_cloud_onenet/include/onenet.h) |
| 鏋勫缓閰嶇疆 | [BearPi-HM_Nano.json](build/lite/product/BearPi-HM_Nano.json) |

## 闄勫綍 B锛?5 鍒嗛挓鎺ユ墜璺嚎

1. **璇绘瀯寤?*锛歚sample/BUILD.gn` 鈫?纭褰撳墠 D1锛沗build/lite/product/BearPi-HM_Nano.json` 鈫?纭 board/kernel銆?2. **璇诲惎鍔?*锛歚app_main.c` 鈫?`HOS_SystemInit` 鈫?`bootstrap_service.c` 鈫?`APP_FEATURE_INIT`銆?3. **璇讳竴涓渶绠€鍗曚緥瀛?*锛欱1 鐪嬫噦鈥滃叆鍙ｅ垱寤虹嚎绋?+ 绾跨▼姝诲惊鐜?+ `usleep`鈥濄€?4. **璇讳竴涓腑鏂緥瀛?*锛欱2/C5 鐪嬫噦鈥渀GpioRegisterIsrFunc` + 鍥炶皟缃簨浠垛€濄€?5. **璇讳竴涓?I2C 渚嬪瓙**锛欳3 鐪嬫噦鈥渀IoSetFunc` + `I2cInit` + `I2cRead`鈥濄€?6. **璇讳竴涓綉缁滀緥瀛?*锛欴3/D4 鐪嬫噦鈥渀WifiConnect` + Socket鈥濄€?7. **璇讳竴涓簯渚嬪瓙**锛欴6锛圥aho 鑷畾涔夛級鎴?D12锛坕ot_link profile锛夈€?8. **鏀逛竴涓紩鑴?*锛氫粠 B1 寮€濮嬶紝鎶?GPIO2 鏀规垚 GPIO13锛岀‘璁ょ紪璇?鐑у綍/鐜拌薄銆?9. **鍔犱竴涓嚎绋?*锛氬鍒?B1锛屾敼鎴愭瘡 200 ms 缈昏浆锛岄獙璇?`osThreadNew`/`usleep`銆?10. **鎺ヤ竴涓紶鎰熷櫒**锛氬鍒?C3锛屾敼 I2C 鍦板潃/瀵勫瓨鍣紝鍏堢敤 `printf` 楠岃瘉鍘熷鍊硷紝鍐嶅仛鎹㈢畻銆?
---

*鏂囨。鍩轰簬褰撳墠宸ヤ綔鍖烘簮鐮侀潤鎬侀槄璇绘暣鐞嗭紱鏈墽琛屼氦鍙夌紪璇?鐑у綍楠岃瘉銆傛秹鍙婄‖浠舵椂搴忋€佺數骞虫瀬鎬с€佸紩鑴氬紩鍑轰互鍘熺悊鍥惧拰瀹炴祴涓哄噯銆?

