//
// Created by Piotr Sperka on 23.01.2021.
//

#include "bootloader.h"

typedef void (*pFunction)(void);

uint8_t UserApplicationExists() {
    uint32_t bootloaderMspValue = *(uint32_t *) (FLASH_BASE);
    uint32_t appMspValue = *(uint32_t *) (APP_ADDRESS);

    return appMspValue == bootloaderMspValue ? 1 : 0;
}

uint8_t EraseUserApplication() {
    HAL_StatusTypeDef success = HAL_ERROR;
    uint32_t errorSector = 0;

    if (HAL_FLASH_Unlock() == HAL_OK) {
        FLASH_EraseInitTypeDef eraseInit = {0};
        eraseInit.NbSectors = 2;
        eraseInit.Sector = FLASH_SECTOR_4;
        eraseInit.VoltageRange = FLASH_VOLTAGE_RANGE_3; // Device operating range: 2.7V to 3.6V
        eraseInit.TypeErase = FLASH_TYPEERASE_SECTORS;

        success = HAL_FLASHEx_Erase(&eraseInit, &errorSector);

        HAL_FLASH_Lock();
    }

    return success == HAL_OK ? 1 : 0;
}

uint8_t WriteUserApplication(uint32_t *data, uint32_t dataSize, uint32_t offset) {
    if (HAL_FLASH_Unlock() == HAL_OK) {
        for (int i = 0; i < dataSize; i++) {
            HAL_StatusTypeDef success = HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, APP_ADDRESS + offset, data[i]);

            if (success != HAL_OK) {
                HAL_FLASH_Lock();
                return 0;
            }
        }

        HAL_FLASH_Lock();
    } else {
        return 0;
    }

    return 1;
}

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
