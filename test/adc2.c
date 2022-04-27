#include <stdio.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include <i2c/smbus.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <signal.h>

#define MASK_12_BIT 0x0FFF
#define MASK_UPPER_BYTE 0xFF00
#define MASK_LOWER_BYTE 0x00FF
#define ADC1 0x08
#define ADC2 0x09
#define CH0 0x80
#define CH1 0xC0
#define NUM_PT 1024
#define BROADCAST 0x6B

void adc_meas(uint8_t CH, uint16_t N_samp, uint16_t *data_ADC1, uint16_t *data_ADC2){
  // variables
  int file_i2c_ADC1, file_i2c_ADC2, file_i2c_BRDC, length = 2;
  //static uint16_t data_ADC[2*NUM_PT] = {0};
  uint16_t data [2] = {0};

  struct timeval t1, t2;
  long long elapsedTime;

  // open I2C Bus
  char *filename = (char*)"/dev/i2c-1";
  if((file_i2c_ADC1 = open(filename, O_RDWR))<0){
    printf("Failed to open the i2c bus\n");
  }

  if((file_i2c_ADC2 = open(filename, O_RDWR))<0){
    printf("Failed to open the i2c bus\n");
  }

  if((file_i2c_BRDC = open(filename, O_RDWR))<0){
    printf("Failed to open the i2c bus\n");
  }

  if(ioctl(file_i2c_ADC1, I2C_SLAVE, ADC1) < 0){
    printf("Failed to acquire bus accss and/or talk to ADC1.\n");
  }

  if(ioctl(file_i2c_ADC2, I2C_SLAVE, ADC2) < 0){
    printf("Failed to acquire bus accss and/or talk to ADC2.\n");
  }
  
  if(ioctl(file_i2c_BRDC, I2C_SLAVE, BROADCAST) < 0){
    printf("Failed to acquire bus accss and/or talk to Broadcast.\n");
  }

  // write config
  switch(CH){
    case 0: data [0] = CH0;
      break;
    case 1: data [0] = CH1;
      break;
    default:
      break;
  }

  if((write(file_i2c_ADC1, data, 1) != 1) || (write(file_i2c_ADC2, data, 1) != 1)){
  printf("Failed to write to the i2c Bus.\n");
  }

  
  // read bytes
  gettimeofday(&t1, NULL);
  for(int i=0;i<N_samp;i++){
    write(file_i2c_BRDC, data, 1);
    //i2c_smbus_write_byte(file_i2c_BRDC,data[0]);
    //i2c_smbus_write_quick(0x6b,0x0);
    //i2c_smbus_write_quick(file_i2c_BRDC,0x0);
    if(read(file_i2c_ADC1, data_ADC1 + i, length) != length){
      printf("Failed to read from the ADC1.\n");
    }
    if(read(file_i2c_ADC2, data_ADC2 + i, length) != length){
      //printf("Failed to read from the ADC2.\n");
    }
  }
    
  gettimeofday(&t2, NULL);
  elapsedTime = ((t2.tv_sec * 1000000) + t2.tv_usec)- ((t1.tv_sec * 1000000) + t1.tv_usec);
  printf("Elapsed Time: %lld\n",elapsedTime);

  //shift values
  for(int i=0;i<16;i++){
    data_ADC1[i] = ((data_ADC1[i] & MASK_UPPER_BYTE)>>12) | ((data_ADC2[i] & MASK_LOWER_BYTE)<<4);
    data_ADC2[i] = ((data_ADC2[i] & MASK_UPPER_BYTE)>>12) | ((data_ADC2[i] & MASK_LOWER_BYTE)<<4);
    printf("ADC1: %u ADC2: %u\n", data_ADC1[i],data_ADC2[i]);
  }
}
