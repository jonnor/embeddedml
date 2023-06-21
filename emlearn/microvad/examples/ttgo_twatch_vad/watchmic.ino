/**
 *  Voice Activity Detection for TTGO TWATCH 2020 V3
 *  
 *  Based on example code from 
 *  https://github.com/Xinyuan-LilyGO/TTGO_TWatch_Library/tree/master/examples/BasicUnit/TwatcV3Special/Microphone
 */



/* Build libfvad directly into the binary. Must put  */

extern "C" {
#include "libfvad/src/fvad.c"
#include "libfvad/src/vad/vad_core.c"
#include "libfvad/src/vad/vad_filterbank.c"
#include "libfvad/src/vad/vad_gmm.c"
#include "libfvad/src/vad/vad_sp.c"
#include "libfvad/src/signal_processing/spl_inl.c"
#include "libfvad/src/signal_processing/energy.c"
#include "libfvad/src/signal_processing/get_scaling_square.c"
#include "libfvad/src/signal_processing/division_operations.c"
#include "libfvad/src/signal_processing/resample_fractional.c"
#include "libfvad/src/signal_processing/resample_by_2_internal.c"
#include "libfvad/src/signal_processing/resample_48khz.c"
}

 
#include "config.h"
#include <driver/i2s.h>

// FIXME: make audio work at 16khz. VAD is currently not reacting in that case
#define AUDIO_SAMPLERATE 48000 
#define VAD_FRAME_SAMPLES 480 // must be 10/20/30ms
#define BUFFER_SIZE (2*VAD_FRAME_SAMPLES)

int16_t vad_buffer[VAD_FRAME_SAMPLES];

int vad_set_mode_status = -11;
int vad_set_samplerate_status = -11;

// TWATCH 2020 V3 PDM microphone pin
#define MIC_DATA            2
#define MIC_CLOCK           0

uint8_t buffer[BUFFER_SIZE] = {0};

TTGOClass           *ttgo = nullptr;
lv_obj_t            *chart = nullptr;
lv_chart_series_t   *ser1 = nullptr;

Fvad vad;



void setup()
{
    Serial.begin(115200);

    ttgo = TTGOClass::getWatch();

    ttgo->begin();

    ttgo->openBL();

    ttgo->lvgl_begin();

    lv_obj_t *text = lv_label_create(lv_scr_act(), NULL);
    lv_label_set_text(text, "PDM Microphone Test");
    lv_obj_align(text, NULL, LV_ALIGN_IN_TOP_MID, 0, 20);

    chart = lv_chart_create(lv_scr_act(), NULL);
    lv_obj_set_size(chart, 200, 150);
    lv_obj_align(chart, NULL, LV_ALIGN_CENTER, 0, 0);
    lv_chart_set_type(chart,  LV_CHART_TYPE_LINE);   /*Show lines and points too*/
    lv_chart_set_range(chart, 0, 800);

    ser1 = lv_chart_add_series(chart, LV_COLOR_RED);

    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_PDM),
        .sample_rate =  AUDIO_SAMPLERATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
        .communication_format = (i2s_comm_format_t)(I2S_COMM_FORMAT_I2S | I2S_COMM_FORMAT_I2S_MSB),
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 2,
        .dma_buf_len = 128,
    };

    i2s_pin_config_t i2s_cfg;
    i2s_cfg.bck_io_num   = I2S_PIN_NO_CHANGE;
    i2s_cfg.ws_io_num    = MIC_CLOCK;
    i2s_cfg.data_out_num = I2S_PIN_NO_CHANGE;
    i2s_cfg.data_in_num  = MIC_DATA;

    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &i2s_cfg);
    i2s_set_clk(I2S_NUM_0, AUDIO_SAMPLERATE, I2S_BITS_PER_SAMPLE_16BIT, I2S_CHANNEL_MONO);

    // https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2s.html#pdm-rx-usage
    // i2s_pdm_rx_clk_config_t, i2s_pdm_rx_clk_config_t, mclk_multiple
    // https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2s.html#_CPPv419i2s_mclk_multiple_t
    // dn_sample_mode

    // Setup VAD
    fvad_reset(&vad);
    const int VAD_MODE = 3;
    vad_set_mode_status = fvad_set_mode(&vad, VAD_MODE);
    vad_set_samplerate_status = fvad_set_sample_rate(&vad, AUDIO_SAMPLERATE);
}

void loop()
{
    static uint32_t j = 0;
  
    
    j = j + 1;

    // Wait for audio input
    size_t read_len = 0;
    i2s_read(I2S_NUM_0, (char *) buffer, BUFFER_SIZE, &read_len, portMAX_DELAY);


    // Process the audio
    const int16_t process_start = micros();
    
    for (int i = 0; i < BUFFER_SIZE / 2 ; i++) {

        const uint8_t val1 = buffer[i * 2];
        const uint8_t val2 = buffer[i * 2 + 1] ;
        const int16_t val16 = val1 + val2 *  256;

        
        vad_buffer[i] = val16;

    }
    const int result = fvad_process(&vad, vad_buffer, VAD_FRAME_SAMPLES);
    const int16_t process_end = micros();


    // Log a bit
    Serial.print("frame ");
    Serial.print(" time.ms=");
    Serial.print(millis());
    Serial.print(" read=");
    Serial.print(read_len);
    Serial.print(" result=");
    Serial.print(result);
    Serial.print(" processing.ms=");
    Serial.print((process_end-process_start)/1000.0);

    Serial.print(" set_mode=");
    Serial.print(vad_set_mode_status);
    Serial.print(" set_samplerate=");
    Serial.print(vad_set_samplerate_status);
   
    Serial.println();


    // Update the screen
    if (j % 2 == 0 && j > 0) {
        lv_chart_set_next(chart, ser1, (100.0f)+(result*200.0f));
    }    
    lv_task_handler();
    delay(5);
}
