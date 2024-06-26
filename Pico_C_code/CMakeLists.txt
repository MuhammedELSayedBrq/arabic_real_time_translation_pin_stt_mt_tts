cmake_minimum_required(VERSION 3.12)
include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

project(wifi_connect C CXX ASM)
add_subdirectory("${PICO_SDK_PATH}/FreeRTOS/portable/ThirdParty/GCC/RP2040" FREERTOS_KERNEL)
pico_sdk_init()

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_executable(picow_freertos_iperf_server_sys
        picow_freertos_iperf.c
        )
target_compile_definitions(picow_freertos_iperf_server_sys PRIVATE
        WIFI_SSID=\"${WIFI_SSID}\"
        WIFI_PASSWORD=\"${WIFI_PASSWORD}\"
        NO_SYS=0            # don't want NO_SYS (generally this would be in your lwipopts.h)
        )
target_include_directories(picow_freertos_iperf_server_sys PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}
        ${CMAKE_CURRENT_LIST_DIR}/../.. # for our common lwipopts
        )
target_link_libraries(picow_freertos_iperf_server_sys 
        hardware_dma 
        hardware_adc 
        hardware_irq
        pico_cyw43_arch_lwip_sys_freertos
        pico_stdlib
        pico_lwip_iperf
        FreeRTOS-Kernel-Heap4 # FreeRTOS kernel and dynamic heap
        )
pico_enable_stdio_usb(picow_freertos_iperf_server_sys 1)
pico_enable_stdio_uart(picow_freertos_iperf_server_sys 0)
pico_add_extra_outputs(picow_freertos_iperf_server_sys)
