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
#ifndef __E53_IA1_H__
#define __E53_IA1_H__

/***************************************************************
* 鍚?	绉? GasStatus_ENUM
* 璇?   鏄庯細鏋氫妇鐘舵€佺粨鏋勪綋
***************************************************************/
typedef enum
{
	OFF = 0,
	ON
} E53_IA1_Status_ENUM;

/* E53_IA1浼犳劅鍣ㄦ暟鎹被鍨嬪畾涔?------------------------------------------------------------*/
typedef struct
{
	float    Lux;							//鍏夌収寮哄害
	float    Humidity;        //婀垮害
	float    Temperature;     //娓╁害
} E53_IA1_Data_TypeDef;



/* 瀵勫瓨鍣ㄥ畯瀹氫箟 --------------------------------------------------------------------*/
#define SHT30_Addr 0x44

#define BH1750_Addr 0x23


void E53_IA1_Init(void);
void E53_IA1_Read_Data(E53_IA1_Data_TypeDef *ReadData);
void Light_StatusSet(E53_IA1_Status_ENUM status);
void Motor_StatusSet(E53_IA1_Status_ENUM status);


#endif /* __E53_IA1_H__ */


