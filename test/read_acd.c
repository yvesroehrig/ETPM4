/**
 * @file read_acd.c
 * @author Pavel Mueller, Yves Roehrig
 * @brief C module to read adc data
 * @version 0.1
 * @date 2022-04-23
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include <stdint.h>
#include <linux/i2c-dev.h>

void dualReadLTC2305(uint8_t adc1_address, uint8_t adc2_address, u_int16_t samples){
	uint16_t i;
	for(i=0;i<=samples;i++){
		
	}
}
