import numpy as np
import sounddevice as sd
from moviepy.editor import AudioFileClip, ColorClip
from scipy.io.wavfile import write

def create_wave_sound(duration=5, sample_rate=44100):
    # 시간 배열 생성
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 기본 주파수와 변조 주파수 설정
    base_frequency = 2  # 파도의 기본 주파수 (Hz)
    modulation_frequency = 0.5  # 변조 주파수 (Hz)

    # 파도 소리 생성
    wave = 0.5 * np.sin(2 * np.pi * base_frequency * t) * np.sin(2 * np.pi * modulation_frequency * t)

    # 약간의 노이즈 추가 (자연스러운 느낌을 위해)
    noise = np.random.normal(0, 0.02, wave.shape)  # 평균 0, 표준편차 0.02인 노이즈
    combined_wave = wave + noise

    return combined_wave

# 소리 생성
wave_sound = create_wave_sound()

# 소리 재생
sd.play(wave_sound, samplerate=44100)
sd.wait()  # 소리가 재생될 때까지 대기

# WAV 파일로 저장
wav_file_path = 'wave_sound.wav'
# scipy를 사용하여 WAV 파일로 저장
write(wav_file_path, 44100, wave_sound.astype(np.float32))

# WAV 파일을 MP4로 변환
audio_clip = AudioFileClip(wav_file_path)
video_file_path = 'wave_sound.mp4'

# 비디오 클립 생성
# 여기서는 5초 동안의 단색 비디오를 생성
video_clip = ColorClip(size=(640, 480), color=(0, 0, 255), duration=audio_clip.duration)

# fps 설정
video_clip.fps = 24  # 초당 24 프레임

# 오디오 추가
video_with_audio = video_clip.set_audio(audio_clip)

# 비디오 파일로 저장
video_with_audio.write_videofile(video_file_path, codec='libx264', audio_codec='aac')

print(f"MP4 파일로 변환 완료: {video_file_path}")
