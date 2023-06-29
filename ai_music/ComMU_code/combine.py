import os
from mido import MidiFile, MidiTrack
from pydub import AudioSegment
import subprocess
import platform


class MidiCombine:
    def __init__(self):
        self.base_folder = 'ai_music/ComMU_code/music_output'
        self.output_dir = os.path.abspath('ai_music/ComMU_code/result/midi_files')
        self.folder_names = ['riff_string_cello_mid_low', 'pad_string_cello_mid_low', 'bass_string_cello_mid_low',
                             'accompaniment_string_cello_mid_low', 'main_melody_string_cello_mid_low',
                             'sub_melody_string_cello_mid_low']
        self.file_extension = '.mid'
        self.sound_font = 'ai_music/static/FluidR3_GM.sf2'

    def combine_midi_files(self):
        combined_tracks = []
        combined_midi_file = os.path.join(self.output_dir, 'combined.mid')

        # 디렉토리 생성 코드 추가
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # midi파일 합치기
        for folder_name in self.folder_names:
            folder_path = os.path.join(self.base_folder, folder_name)
            combined_track = MidiTrack()
            file_prefix = f'{folder_name}_'
            file_count = 0
            while True:
                file_name = file_prefix + f'{file_count:03}' + self.file_extension
                file_path = os.path.join(folder_path, file_name)
                if not os.path.exists(file_path):
                    break
                midi = MidiFile(file_path)
                for i, track in enumerate(midi.tracks):
                    if i != 0:
                        for msg in track:
                            combined_track.append(msg)
                file_count += 1
            combined_tracks.append(combined_track)

        combined_midi = MidiFile(ticks_per_beat=480)
        combined_midi.tracks.extend(combined_tracks)
        combined_midi.save(combined_midi_file)
        return combined_midi_file
