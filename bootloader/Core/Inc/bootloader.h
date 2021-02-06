//
// Created by Piotr Sperka on 23.01.2021.
//

#ifndef BOOTLOADER_BOOTLOADER_H
#define BOOTLOADER_BOOTLOADER_H

#include "stm32f2xx_hal.h"

#define APP_ADDRESS (uint32_t)0x08010000
#define RAM_START (uint32_t)0x20000000

void JumpToApplication();
uint8_t EraseUserApplication();
uint8_t UserApplicationExists();
uint8_t WriteUserApplication(uint32_t *data, uint32_t dataSize, uint32_t offset);

#endif //BOOTLOADER_BOOTLOADER_H
