//
// Created by Piotr Sperka on 23.01.2021.
//

#ifndef BOOTLOADER_BOOTLOADER_H
#define BOOTLOADER_BOOTLOADER_H

#include "stm32f2xx_hal.h"

#define APP_ADDRESS (uint32_t)0x08010000

void JumpToApplication();

#endif //BOOTLOADER_BOOTLOADER_H
