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
#define CH0 0x88
#define CH1 0xC8
#define NUM_PT 1024
#define BROADCAST 0x6B

int main(void){
  // variables
  int file_i2c_ADC1, file_i2c_ADC2, file_i2c_BRDC, length = 2;
  uint16_t data_ADC1[NUM_PT] = {0};
  uint16_t data_ADC2[NUM_PT] = {0};
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
  data [0] = CH0;
  if((write(file_i2c_ADC1, data, 1) != 1) || (write(file_i2c_ADC2, data, 1) != 1)){
  printf("Failed to write to the i2c Bus.\n");
  }

  while(1){
    // read bytes
    gettimeofday(&t1, NULL);
    for(int i=0;i<NUM_PT;i++){
      //write(file_i2c_BRDC, data, 1);
      //i2c_smbus_write_byte(file_i2c_BRDC,data[0]);
      i2c_smbus_write_quick(0x6b,0x0);
      //i2c_smbus_write_quick(file_i2c_BRDC,0x0);
      //close(file_i2c_BRDC);
      read(file_i2c_ADC1, data_ADC1 + i, length);
      read(file_i2c_ADC2, data_ADC2 + i, length);
    }
    
    gettimeofday(&t2, NULL);
    elapsedTime = ((t2.tv_sec * 1000000) + t2.tv_usec)- ((t1.tv_sec * 1000000) + t1.tv_usec);
    printf("Elapsed Time: %lld\n",elapsedTime);

    // print data
    for(int i=0;i<16;i++){
      data_ADC1[i] = ((data_ADC1[i] & MASK_UPPER_BYTE)>>12) | ((data_ADC1[i] & MASK_LOWER_BYTE)<<4);
      data_ADC2[i] = ((data_ADC2[i] & MASK_UPPER_BYTE)>>12) | ((data_ADC2[i] & MASK_LOWER_BYTE)<<4);
      printf("Value %u ADC1: %u ADC2: %u\n",i+1,data_ADC1[i],data_ADC2[i]);
    }
    printf("No Error\n END OF FILE!\n");
  }
}
