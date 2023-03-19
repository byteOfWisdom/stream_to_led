cmake_minimum_required(VERSION 3.25)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(stream_to_led)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

add_compile_options(-O3)

add_executable(stream_to_led)

pico_generate_pio_header(stream_to_led ${CMAKE_CURRENT_LIST_DIR}/src/led.pio)

target_sources(stream_to_led PRIVATE src/main.c)

target_include_directories(stream_to_led PRIVATE ${CMAKE_CURRENT_LIST_DIR} )

#target_link_libraries(stream_to_led PRIVATE pico_stdlib hardware_pio pico_cyw43_arch_lwip_threadsafe_background)
target_link_libraries(stream_to_led PRIVATE pico_stdlib hardware_pio pico_cyw43_arch_lwip_poll)
# rest of your project

pico_enable_stdio_usb(stream_to_led 1) # for the serial printing to the usb port

pico_add_extra_outputs(stream_to_led)