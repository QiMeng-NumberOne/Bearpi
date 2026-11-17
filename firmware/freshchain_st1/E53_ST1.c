/*
 * Copyright (c) 2020 Nanjing Xiaoxiongpai Intelligent Technology Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include "ohos_init.h"
#include "cmsis_os2.h"

#include "E53_ST1.h"
#include "wifiiot_errno.h"
#include "wifiiot_gpio.h"
#include "wifiiot_gpio_ex.h"
#include "wifiiot_pwm.h"
#include "wifiiot_uart.h"

gps_msg             gpsmsg;
static unsigned char gps_uart[1000];


/***************************************************************
* 鍑芥暟鍚嶇О: GPS_Init
* 璇?   鏄? 鍒濆鍖朑PS妯″潡
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void GPS_Init(void)
{

    uint32_t ret;

    WifiIotUartAttribute uart_attr = {

        //baud_rate: 9600
        .baudRate = 115200,

        //data_bits: 8bits
        .dataBits = 8,
        .stopBits = 1,
        .parity = 0,
    };

    //Initialize uart driver
    ret = UartInit(WIFI_IOT_UART_IDX_1, &uart_attr, NULL);
    if (ret != WIFI_IOT_SUCCESS)
    {
        printf("Failed to init uart! Err code = %d\n", ret);
        return;
    }
    
}

/***************************************************************
* 鍑芥暟鍚嶇О: Init_E53_ST1
* 璇?   鏄? 鍒濆鍖朎53_ST1鎵╁睍鏉?
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Init_E53_ST1(void)
{
    GpioInit();                                                           //鍒濆鍖朑PIO
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_8, WIFI_IOT_IO_FUNC_GPIO_8_PWM1_OUT); //璁剧疆GPIO_8寮曡剼澶嶇敤鍔熻兘涓篜WM
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_8, WIFI_IOT_GPIO_DIR_OUT);           //璁剧疆GPIO_8寮曡剼涓鸿緭鍑烘ā寮?
    PwmInit(WIFI_IOT_PWM_PORT_PWM1);                                      //鍒濆鍖朠WM1绔彛

    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_4, WIFI_IOT_IO_FUNC_GPIO_4_GPIO);     //璁剧疆GPIO_4寮曡剼澶嶇敤鍔熻兘涓篏PIO
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_4, WIFI_IOT_GPIO_DIR_OUT);           //璁剧疆GPIO_4寮曡剼涓鸿緭鍑烘ā寮?
    GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_4, 0);

    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_2, WIFI_IOT_IO_FUNC_GPIO_2_GPIO);     //璁剧疆GPIO_2寮曡剼澶嶇敤鍔熻兘涓篏PIO
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_2, WIFI_IOT_GPIO_DIR_OUT);           //璁剧疆GPIO_2寮曡剼涓鸿緭鍑烘ā寮?
    GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_2, 0);

	GPS_Init();
}

/***************************************************\
* 鍑芥暟鍚嶇О: NMEA_Comma_Pos
*	鍑芥暟鍔熻兘锛氫粠buf閲岄潰寰楀埌绗琧x涓€楀彿鎵€鍦ㄧ殑浣嶇疆
*	杈撳叆鍊硷細
*	杩斿洖鍊硷細0~0xFE锛屼唬琛ㄩ€楀彿鎵€鍦ㄤ綅缃殑渚垮疁
*				 	0xFF锛屼唬琛ㄤ笉瀛樺湪绗琧x涓€楀彿
\***************************************************/

uint8_t NMEA_Comma_Pos(uint8_t *buf,uint8_t cx)
{
	uint8_t *p = buf;
	while(cx)
	{
		if(*buf=='*'||*buf<' '||*buf>'z')return 0xFF;
		if(*buf==',')cx--;
		buf++;
	}
	return buf-p;
}
/***************************************************\
* 鍑芥暟鍚嶇О: NMEA_Pow
*	鍑芥暟鍔熻兘锛氳繑鍥瀖鐨刵娆℃柟鍊?
*	杈撳叆鍊硷細搴曟暟m鍜屾寚鏁皀
*	杩斿洖鍊硷細m^n
\***************************************************/
uint32_t NMEA_Pow(uint8_t m,uint8_t n)
{
	uint32_t result = 1;
	while(n--)result *= m;
	return result;
}
/***************************************************\
* 鍑芥暟鍚嶇О: NMEA_Str2num
*	鍑芥暟鍔熻兘锛歴tr鏁板瓧杞崲涓猴紙int锛夋暟瀛楋紝浠?,'鎴栬€?*'缁撴潫
*	杈撳叆鍊硷細buf锛屾暟瀛楀瓨鍌ㄥ尯
*				 	dx锛屽皬鏁扮偣浣嶆暟锛岃繑鍥炵粰璋冪敤鍑芥暟
*	杩斿洖鍊硷細杞崲鍚庣殑鏁板€?
\***************************************************/
int NMEA_Str2num(uint8_t *buf,uint8_t*dx)
{
	uint8_t *p = buf;
	uint32_t ires = 0,fres = 0;
	uint8_t ilen = 0,flen = 0,i;
	uint8_t mask = 0;
	int res;
	while(1)
	{
		if(*p=='-'){mask |= 0x02;p++;}//璇存槑鏈夎礋鏁?
		if(*p==','||*p=='*')break;//閬囧埌缁撴潫绗?
		if(*p=='.'){mask |= 0x01;p++;}//閬囧埌灏忔暟鐐?
		else if(*p>'9'||(*p<'0'))//鏁板瓧涓嶅湪0鍜?涔嬪唴锛岃鏄庢湁闈炴硶瀛楃
		{
			ilen = 0;
			flen = 0;
			break;
		}
		if(mask&0x01)flen++;//灏忔暟鐐圭殑浣嶆暟
		else ilen++;//str闀垮害鍔犱竴
		p++;//涓嬩竴涓瓧绗?
	}
	if(mask&0x02)buf++;//绉诲埌涓嬩竴浣嶏紝闄ゅ幓璐熷彿
	for(i=0;i<ilen;i++)//寰楀埌鏁存暟閮ㄥ垎鏁版嵁
	{
		ires += NMEA_Pow(10,ilen-1-i)*(buf[i]-'0');
	}
	if(flen>5)flen=5;//鏈€澶氬彇浜斾綅灏忔暟
	*dx = flen;
	for(i=0;i<flen;i++)//寰楀埌灏忔暟閮ㄥ垎鏁版嵁
	{
		fres +=NMEA_Pow(10,flen-1-i)*(buf[ilen+1+i]-'0');
	}
	res = ires*NMEA_Pow(10,flen)+fres;
	if(mask&0x02)res = -res;
	return res;
}
/***************************************************\
* 鍑芥暟鍚嶇О: NMEA_BDS_GPRMC_Analysis
*	鍑芥暟鍔熻兘锛氳В鏋怗PRMC淇℃伅
*	杈撳叆鍊硷細gpsx,NMEA淇℃伅缁撴瀯浣?
*				 buf锛氭帴鏀跺埌鐨凣PS鏁版嵁缂撳啿鍖洪鍦板潃
\***************************************************/
uint8_t NMEA_BDS_GPRMC_Analysis(gps_msg *gpsmsg,uint8_t *buf)
{
	uint8_t *p4,dx;			 
	uint8_t posx;     
	uint32_t temp;	   
	float rs;  
	p4=(uint8_t*)strstr((const char *)buf,"$GPRMC");
	if(p4 == NULL) {
		p4=(uint8_t*)strstr((const char *)buf,"$GNRMC");
	}
	if(p4 == NULL) {
		return 0;
	}
	/* field 2: A = valid fix, V = invalid fix */
	posx=NMEA_Comma_Pos(p4,2);
	if(posx==0XFF || *(p4+posx)!='A') {
		return 0;
	}
	posx=NMEA_Comma_Pos(p4,3);								//寰楀埌绾害
	if(posx==0XFF) {
		return 0;
	}
	temp=NMEA_Str2num(p4+posx,&dx);		 	 
	gpsmsg->latitude_bd=temp/NMEA_Pow(10,dx+2);	//寰楀埌掳
	rs=temp%NMEA_Pow(10,dx+2);				//寰楀埌'		 
	gpsmsg->latitude_bd=gpsmsg->latitude_bd*NMEA_Pow(10,5)+(rs*NMEA_Pow(10,5-dx))/60;//杞崲涓郝?
	posx=NMEA_Comma_Pos(p4,4);								//鍗楃含杩樻槸鍖楃含 
	if(posx!=0XFF)gpsmsg->nshemi_bd=*(p4+posx);					 
	posx=NMEA_Comma_Pos(p4,5);								//寰楀埌缁忓害
	if(posx==0XFF) {
		return 0;
	}
	temp=NMEA_Str2num(p4+posx,&dx);		 	 
	gpsmsg->longitude_bd=temp/NMEA_Pow(10,dx+2);	//寰楀埌掳
	rs=temp%NMEA_Pow(10,dx+2);				//寰楀埌'		 
	gpsmsg->longitude_bd=gpsmsg->longitude_bd*NMEA_Pow(10,5)+(rs*NMEA_Pow(10,5-dx))/60;//杞崲涓郝?
	posx=NMEA_Comma_Pos(p4,6);								//涓滅粡杩樻槸瑗跨粡
	if(posx!=0XFF)gpsmsg->ewhemi_bd=*(p4+posx);	
	if(gpsmsg->latitude_bd==0 || gpsmsg->longitude_bd==0) {
		return 0;
	}
	return 1;
}

/***************************************************************
* 鍑芥暟鍚嶇О: E53_ST1_Read_Data
* 璇?   鏄? 鑾峰彇GPS缁忕含搴︿俊鎭?
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void E53_ST1_Read_Data(E53_ST1_Data_TypeDef *ReadData)
{	
    int read_len;

    if (ReadData == NULL) {
        return;
    }
    /* Clear the buffer first: a short read must not re-parse yesterday's sentence. */
    memset(gps_uart, 0, sizeof(gps_uart));
    read_len = UartRead(WIFI_IOT_UART_IDX_1, gps_uart, 1000);
    if (read_len <= 0 || NMEA_BDS_GPRMC_Analysis(&gpsmsg, (uint8_t*)gps_uart) == 0) {
        ReadData->Longitude = 0.0f;
        ReadData->Latitude = 0.0f;
        ReadData->Valid = 0;
        return;
    }
    ReadData->Longitude = (float)((float)gpsmsg.longitude_bd / 100000);
    ReadData->Latitude = (float)((float)gpsmsg.latitude_bd / 100000);
    ReadData->Valid = 1;
}

/***************************************************************
* 鍑芥暟鍚嶇О: Beep_StatusSet
* 璇?   鏄? 铚傞福鍣ㄦ姤璀︿笌鍚?
* 鍙?   鏁? status,ENUM鏋氫妇鐨勬暟鎹?
*									OFF,铚傞福鍣?
*									ON,寮€铚傞福鍣?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Beep_StatusSet(E53_ST1_Status_ENUM status)
{
    if (status == ON)
        PwmStart(WIFI_IOT_PWM_PORT_PWM1, 20000, 40000); //杈撳嚭涓嶅悓鍗犵┖姣旂殑PWM娉?
    if (status == OFF)
        PwmStop(WIFI_IOT_PWM_PORT_PWM1);
}

