#include <stdio.h>
#include <linux/i2c-dev.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <bc2835.h>

#define MASK_12_BIT 0x0FFF
#define ADC1 0x08
#define ADC2 0x09
#define CH0 0x80
#define CH1 0xC0
#define NUM_PT 1024

int main(void){
  // variables
  int file_i2c_ADC1, file_i2c_ADC2, length = 2;
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


  if(ioctl(file_i2c_ADC1, I2C_SLAVE, ADC1) < 0){
    printf("Failed to acquire bus accss and/or talk to ADC1.\n");
  }

  if(ioctl(file_i2c_ADC2, I2C_SLAVE, ADC2) < 0){
    printf("Failed to acquire bus accss and/or talk to ADC2.\n");
  }
  
  // write config
  data [0] = CH0;
  if((write(file_i2c_ADC1, data, 1) != 1) || (write(file_i2c_ADC2, data, 1) != 1)){
  printf("Failed to write to the i2c Bus.\n");
  }

  // send test broadcast

  // read bytes
  gettimeofday(&t1, NULL);
  for(int i=0;i<NUM_PT;i++){
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

  // print data
  for(int i=0;i<16;i++){
    data_ADC1[i] = (data_ADC1[i]>>4) & MASK_12_BIT;
    data_ADC2[i] = (data_ADC2[i]>>4) & MASK_12_BIT;
    printf("Value %u ADC1: %u ADC2: %u\n",i+1,data_ADC1[i],data_ADC2[i]);
  }
  printf("No Error\n END OF FILE!\n");
}
