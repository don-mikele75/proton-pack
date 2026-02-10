
import time
import urandom
import uasyncio as asyncio
from machine import I2S
from machine import Pin
from asyncio import sleep
import struct
import io

class WaveFileHeader:
    @staticmethod
    def from_file(file_source):
        ident = file_source.read(4)
        if ident != b"RIFF":
            raise ValueError(f"Expected RIFF header, got {ident}.")
        file_size = struct.unpack("I",
            file_source.read(4))
        file_type = file_source.read(8)
        if file_type[:7] != b"WAVEfmt":
            raise ValueError(f"Not WAVE type. Got {file_type}")
        fmt = "IHHIIHHHI"
        fmt_size, wave_fmt, channels, sample_rate, byte_rate, block_align, bits_per_sample, extra, data_size = struct.unpack(fmt,
            file_source.read(struct.calcsize(fmt)))

        header = WaveFileHeader()
        header.wave_fmt = wave_fmt
        header.channels = channels
        header.sample_rate = sample_rate
        header.bits_per_sample = bits_per_sample
        header.data_size = data_size
        return header

    def __init__(self):
        self.data_size = 0xFFFF
        self.wave_fmt = 1 # PCM
        self.channels = 1
        self.sample_rate = 44_100
        self.bits_per_sample = 16

class Player:

    ready = False
    task: asyncio.Task = None
    
    BUFFER_LENGTH_IN_BYTES = 50000

    def __init__(self, sck_pin, ws_pin, sd_pin, i2s_id, debug=False):
        self.sck_pin = sck_pin
        self.ws_pin = ws_pin
        self.sd_pin = sd_pin
        self.i2s_id = i2s_id
        self.listeners = list()
        self.ready = True
        self.debug = debug
            
    def start(self, file, callback=None, continuous = False):
        self.stop()
        self.task = asyncio.create_task(self._play(file, callback, continuous))

    def stop(self):
        if not (self.task is None):
            self.task.cancel()
            self.task = None
    
    def is_running(self): 
        return not (self.task is None)
    
    async def _play(self, file, callback=None, continuous = False):
        while not self.ready:
            await asyncio.sleep_ms(10)
        self.ready = False
        try:            
            with open(file, "rb") as wav:
                wav_header = WaveFileHeader.from_file(wav)
                print(f"Start playing WAV File: {file} - {wav_header.bits_per_sample} Bits / {wav_header.sample_rate} Hz / Channels: {wav_header.channels} ...")
                format = I2S.MONO 
                if (wav_header.channels == 2):
                    format = I2S.STEREO

                audio_out = I2S(
                    self.i2s_id,
                    sck = self.sck_pin,
                    ws= self.ws_pin,
                    sd = self.sd_pin,
                    mode = I2S.TX,
                    bits = wav_header.bits_per_sample,
                    format = format,
                    rate = wav_header.sample_rate,
                    ibuf = self.BUFFER_LENGTH_IN_BYTES,
                )

                swriter = asyncio.StreamWriter(audio_out) # type: ignore
                _ = wav.seek(44)  # advance to first byte of Data section in WAV file

                wav_samples = bytearray(10000)
                wav_samples_mv = memoryview(wav_samples)
                while True:
                    num_read = wav.readinto(wav_samples_mv)
                    if num_read == 0:
                        if continuous:
                            print("... looping ...")
                            _ = wav.seek(44)
                        else:
                            break
                    else:
                        if not self.debug:
                            swriter.out_buf = wav_samples_mv[:num_read] # type: ignore
                            await swriter.drain()
                        else:
                            no_of_bytes_s = (wav_header.sample_rate * wav_header.bits_per_sample * wav_header.channels) / 8
                            await asyncio.sleep(num_read / no_of_bytes_s)
                    
        except (asyncio.CancelledError) as e:
            print(f"... cancelled playing WAV file {file}...")
        except (Exception) as e:
            print("!!! Exception Playing WAV File: {} {}\n".format(type(e).__name__, e))
        finally:
            wav.close()
            audio_out.deinit()
            print(f"... finished playing WAV file {file}")
            if not (callback is None):
                await callback()
            self.ready = True

