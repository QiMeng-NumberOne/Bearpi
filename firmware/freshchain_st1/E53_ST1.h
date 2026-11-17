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

#ifndef __E53_ST1_H__
#define __E53_ST1_H__

#include <stdint.h>

/***************************************************************
* 鍚?	绉? GasStatus_ENUM
* 璇?   鏄庯細鏋氫妇鐘舵€佺粨鏋勪綋
***************************************************************/
typedef enum
{
	OFF = 0,
	ON
} E53_ST1_Status_ENUM;

/***************************************************\
*GPS NMEA-0183鍗忚閲嶈鍙傛暟缁撴瀯浣撳畾涔?
*鍗槦淇℃伅
\***************************************************/
typedef struct
{
	uint32_t latitude_bd;					//绾害   鍒嗘墿澶?00000鍊嶏紝瀹為檯瑕侀櫎浠?00000
	uint8_t nshemi_bd;						//鍖楃含/鍗楃含,N:鍖楃含;S:鍗楃含	
	uint32_t longitude_bd;			  //缁忓害 鍒嗘墿澶?00000鍊?瀹為檯瑕侀櫎浠?00000
	uint8_t ewhemi_bd;						//涓滅粡/瑗跨粡,E:涓滅粡;W:瑗跨粡
}gps_msg;

/* E53_ST1浼犳劅鍣ㄦ暟鎹被鍨嬪畾涔?------------------------------------------------------------*/
typedef struct
{
		float    Longitude;				//缁忓害
		float    Latitude;        //绾害
		uint8_t  Valid;           //1: 鏈璇诲埌鏈夋晥GPRMC锛?: 鏃犳柊瀹氫綅
} E53_ST1_Data_TypeDef;


void Init_E53_ST1(void);
void E53_ST1_Read_Data(E53_ST1_Data_TypeDef *ReadData);
void Beep_StatusSet(E53_ST1_Status_ENUM status);

#endif /* __E53_ST1_H__ */


