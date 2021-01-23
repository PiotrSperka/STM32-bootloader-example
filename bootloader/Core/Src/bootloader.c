//
// Created by Piotr Sperka on 23.01.2021.
//

#include "bootloader.h"

typedef void (*pFunction)(void);

void JumpToAddress(uint32_t addr) {
    uint32_t JumpAddress = *(uint32_t *) (addr + 4);
    pFunction Jump = (pFunction) JumpAddress;

    HAL_RCC_DeInit();
    HAL_DeInit();
    SysTick->CTRL = 0;
    SysTick->LOAD = 0;
    SysTick->VAL = 0;

    SCB->VTOR = addr;
    __set_MSP(*(uint32_t *) addr);

    Jump();
}

void JumpToApplication() {
    JumpToAddress(APP_ADDRESS);
}
