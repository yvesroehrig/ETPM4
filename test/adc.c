#include <stdio.h>
#include <linux/i2c-dev.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>

#define MASK_12_BIT 0x0FFF
#define CH0 0x80
#define CH1 0xC0

int main(void){
  // variables
  int file_i2c, length = 2;
  uint16_t data[16] = {0};
  struct timeval t1, t2;
  long long elapsedTime;

  // open I2C Bus
  char *filename = (char*)"/dev/i2c-1";
  if((file_i2c = open(filename, O_RDWR))<0){
    printf("Failed to open the i2c bus\n");
  }

  int addr = 0x09;
  if(ioctl(file_i2c, I2C_SLAVE, addr) < 0){
    printf("Failed to acquire bus accss and/or talk to slave.\n");
  }
  // write config
  data [0] = CH0;
  if(write(file_i2c, data, 1) != 1){
  printf("Failed to write to the i2c Bus.\n");
  }

  // read bytes
  gettimeofday(&t1, NULL);
  if(read(file_i2c, data, length) != length){
    printf("Failed to read from the i2c bus.\n");
  }
  gettimeofday(&t2, NULL);
  elapsedTime = ((t2.tv_sec * 1000000) + t2.tv_usec)- ((t1.tv_sec * 1000000) + t1.tv_usec);
  printf("Elapsed Time: %lld\n",elapsedTime);

  // print data
  for(int i=0;i<16;i++){
    data[i] = (data[i]>>4) & MASK_12_BIT;
    printf("Value %u : %u\n",i+1,data[i]);
  }
  printf("No Error\n END OF FILE!\n");
}
