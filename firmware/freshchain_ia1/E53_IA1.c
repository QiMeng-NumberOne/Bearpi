/*
 * Copyright (c) 2020 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
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
#include "cmsis_os2.h"
#include "E53_IA1.h"
#include "wifiiot_errno.h"
#include "wifiiot_gpio.h"
#include "wifiiot_gpio_ex.h"
#include "wifiiot_i2c.h"
#include "wifiiot_i2c_ex.h"

/***************************************************************
* 鍑芥暟鍚嶇О: E53_IA1_IO_Init
* 璇?   鏄? E53_IA1_GPIO鍒濆鍖?
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
static void E53_IA1_IO_Init(void)
{
    GpioInit();

    //璁剧疆GPIO_2鐨勫鐢ㄥ姛鑳戒负鏅€欸PIO
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_8, WIFI_IOT_IO_FUNC_GPIO_8_GPIO);

    //璁剧疆GPIO_2涓鸿緭鍑烘ā寮?
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_8, WIFI_IOT_GPIO_DIR_OUT);

    //璁剧疆GPIO_2鐨勫鐢ㄥ姛鑳戒负鏅€欸PIO
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_14, WIFI_IOT_IO_FUNC_GPIO_14_GPIO);

    //璁剧疆GPIO_2涓鸿緭鍑烘ā寮?
    GpioSetDir(WIFI_IOT_IO_NAME_GPIO_14, WIFI_IOT_GPIO_DIR_OUT);

    //GPIO_0澶嶇敤涓篒2C1_SDA
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_0, WIFI_IOT_IO_FUNC_GPIO_0_I2C1_SDA);

    //GPIO_1澶嶇敤涓篒2C1_SCL
    IoSetFunc(WIFI_IOT_IO_NAME_GPIO_1, WIFI_IOT_IO_FUNC_GPIO_1_I2C1_SCL);

    //baudrate: 400kbps
    I2cInit(WIFI_IOT_I2C_IDX_1, 400000);
    I2cSetBaudrate(WIFI_IOT_I2C_IDX_1, 400000);
}

/***************************************************************
* 鍑芥暟鍚嶇О: Init_BH1750
* 璇?   鏄? 鍐欏懡浠ゅ垵濮嬪寲BH1750
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Init_BH1750(void)
{
    WifiIotI2cData bh1750_i2c_data = {0};
    uint8_t send_data[1] = {0x01};
    bh1750_i2c_data.sendBuf = send_data;
    bh1750_i2c_data.sendLen = 1;
    I2cWrite(WIFI_IOT_I2C_IDX_1, (BH1750_Addr << 1) | 0x00, &bh1750_i2c_data);
}

/***************************************************************
* 鍑芥暟鍚嶇О: Start_BH1750
* 璇?   鏄? 鍚姩BH1750
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Start_BH1750(void)
{
    WifiIotI2cData bh1750_i2c_data = {0};
    uint8_t send_data[1] = {0x10};
    bh1750_i2c_data.sendBuf = send_data;
    bh1750_i2c_data.sendLen = 1;
    I2cWrite(WIFI_IOT_I2C_IDX_1, (BH1750_Addr << 1) | 0x00, &bh1750_i2c_data);
}

/***************************************************************
* 鍑芥暟鍚嶇О: SHT30_reset
* 璇?   鏄? SHT30澶嶄綅
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void SHT30_reset(void)
{
    WifiIotI2cData sht30_i2c_data = {0};
    uint8_t send_data[2] = {0x30, 0xA2};
    sht30_i2c_data.sendBuf = send_data;
    sht30_i2c_data.sendLen = 2;
    I2cWrite(WIFI_IOT_I2C_IDX_1, (SHT30_Addr << 1) | 0x00, &sht30_i2c_data);
}

/***************************************************************
* 鍑芥暟鍚嶇О: Init_SHT30
* 璇?   鏄? 鍒濆鍖朣HT30锛岃缃祴閲忓懆鏈?
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Init_SHT30(void)
{
    WifiIotI2cData sht30_i2c_data = {0};
    uint8_t send_data[2] = {0x22, 0x36};
    sht30_i2c_data.sendBuf = send_data;
    sht30_i2c_data.sendLen = 2;
    I2cWrite(WIFI_IOT_I2C_IDX_1, (SHT30_Addr << 1) | 0x00, &sht30_i2c_data);
}

/***************************************************************
* 鍑芥暟鍚嶇О: SHT3x_CheckCrc
* 璇?   鏄? 妫€鏌ユ暟鎹纭€?
* 鍙?   鏁? data锛氳鍙栧埌鐨勬暟鎹?
						nbrOfBytes锛氶渶瑕佹牎楠岀殑鏁伴噺
						checksum锛氳鍙栧埌鐨勬牎瀵规瘮楠屽€?
* 杩?鍥?鍊? 鏍￠獙缁撴灉锛?-鎴愬姛		1-澶辫触
***************************************************************/
static uint8_t SHT3x_CheckCrc(uint8_t data[], uint8_t nbrOfBytes, uint8_t checksum)
{

    uint8_t crc = 0xFF;
    uint8_t bit = 0;
    uint8_t byteCtr;
    const int16_t POLYNOMIAL = 0x131;
    //calculates 8-Bit checksum with given polynomial
    for (byteCtr = 0; byteCtr < nbrOfBytes; ++byteCtr)
    {
        crc ^= (data[byteCtr]);
        for (bit = 8; bit > 0; --bit)
        {
            if (crc & 0x80)
                crc = (crc << 1) ^ POLYNOMIAL;
            else
                crc = (crc << 1);
        }
    }

    if (crc != checksum)
        return 1;
    else
        return 0;
}

/***************************************************************
* 鍑芥暟鍚嶇О: SHT3x_CalcTemperatureC
* 璇?   鏄? 娓╁害璁＄畻
* 鍙?   鏁? u16sT锛氳鍙栧埌鐨勬俯搴﹀師濮嬫暟鎹?
* 杩?鍥?鍊? 璁＄畻鍚庣殑娓╁害鏁版嵁
***************************************************************/
static float SHT3x_CalcTemperatureC(uint16_t u16sT)
{

    float temperatureC = 0;

    u16sT &= ~0x0003;

    temperatureC = (175 * (float)u16sT / 65535 - 45);

    return temperatureC;
}

/***************************************************************
* 鍑芥暟鍚嶇О: SHT3x_CalcRH
* 璇?   鏄? 婀垮害璁＄畻
* 鍙?   鏁? u16sRH锛氳鍙栧埌鐨勬箍搴﹀師濮嬫暟鎹?
* 杩?鍥?鍊? 璁＄畻鍚庣殑婀垮害鏁版嵁
***************************************************************/
static float SHT3x_CalcRH(uint16_t u16sRH)
{

    float humidityRH = 0;

    u16sRH &= ~0x0003;

    humidityRH = (100 * (float)u16sRH / 65535);

    return humidityRH;
}

/***************************************************************
* 鍑芥暟鍚嶇О: E53_IA1_Init
* 璇?   鏄? 鍒濆鍖朎53_IA1
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void E53_IA1_Init(void)
{
    E53_IA1_IO_Init();
    Init_BH1750();
    Init_SHT30();
}

/***************************************************************
* 鍑芥暟鍚嶇О: E53_IA1_Read_Data
* 璇?   鏄? 娴嬮噺鍏夌収寮哄害銆佹俯搴︺€佹箍搴?
* 鍙?   鏁? 鏃?
* 杩?鍥?鍊? 鏃?
***************************************************************/
void E53_IA1_Read_Data(E53_IA1_Data_TypeDef *ReadData)
{
    //鍚姩浼犳劅鍣ㄩ噰闆嗘暟鎹?
    Start_BH1750();

    usleep(180000);
    WifiIotI2cData bh1750_i2c_data = {0};
    uint8_t recv_data[2] = {0};
    bh1750_i2c_data.receiveBuf = recv_data;
    bh1750_i2c_data.receiveLen = 2;

    //璇诲彇浼犳劅鍣ㄦ暟鎹?
    I2cRead(WIFI_IOT_I2C_IDX_1, (BH1750_Addr << 1) | 0x01, &bh1750_i2c_data);
    ReadData->Lux = (float)(((recv_data[0] << 8) + recv_data[1]) / 1.2);

    uint8_t data[3];
    uint16_t dat, tmp;
    uint8_t SHT3X_Data_Buffer[6];

    WifiIotI2cData sht30_i2c_data = {0};
    uint8_t send_data[2] = {0xE0, 0x00};
    sht30_i2c_data.sendBuf = send_data;
    sht30_i2c_data.sendLen = 2;
    sht30_i2c_data.receiveBuf = SHT3X_Data_Buffer;
    sht30_i2c_data.receiveLen = 6;
    I2cWriteread(WIFI_IOT_I2C_IDX_1, (SHT30_Addr << 1) | 0x00, &sht30_i2c_data);

    data[0] = SHT3X_Data_Buffer[0];
    data[1] = SHT3X_Data_Buffer[1];
    data[2] = SHT3X_Data_Buffer[2];

    tmp = SHT3x_CheckCrc(data, 2, data[2]);
    if (!tmp)
    {
        dat = ((uint16_t)data[0] << 8) | data[1];
        ReadData->Temperature = SHT3x_CalcTemperatureC(dat);
    }

    data[0] = SHT3X_Data_Buffer[3];
    data[1] = SHT3X_Data_Buffer[4];
    data[2] = SHT3X_Data_Buffer[5];

    tmp = SHT3x_CheckCrc(data, 2, data[2]);
    if (!tmp)
    {
        dat = ((uint16_t)data[0] << 8) | data[1];
        ReadData->Humidity = SHT3x_CalcRH(dat);
    }
}

/***************************************************************
* 鍑芥暟鍚嶇О: Light_StatusSet
* 璇?   鏄? 鐏姸鎬佽缃?
* 鍙?   鏁? status,ENUM鏋氫妇鐨勬暟鎹?
*									OFF,鍏?
*									ON,寮€
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Light_StatusSet(E53_IA1_Status_ENUM status)
{
    if (status == ON)

        //璁剧疆GPIO_2杈撳嚭楂樼數骞崇偣浜伅
        GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_14, 1);
    if (status == OFF)

        //璁剧疆GPIO_2杈撳嚭浣庣數骞冲叧闂伅
        GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_14, 0);
}

/***************************************************************
* 鍑芥暟鍚嶇О: Motor_StatusSet
* 璇?   鏄? 鐢垫満鐘舵€佽缃?
* 鍙?   鏁? status,ENUM鏋氫妇鐨勬暟鎹?
*									OFF,鍏?
*									ON,寮€
* 杩?鍥?鍊? 鏃?
***************************************************************/
void Motor_StatusSet(E53_IA1_Status_ENUM status)
{
    if (status == ON)

        //璁剧疆GPIO_8杈撳嚭楂樼數骞虫墦寮€鐢垫満
        GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_8, 1);

    if (status == OFF)

        //璁剧疆GPIO_8杈撳嚭浣庣數骞冲叧闂數鏈?
        GpioSetOutputVal(WIFI_IOT_IO_NAME_GPIO_8, 0);
}

