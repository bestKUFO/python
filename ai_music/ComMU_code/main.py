import subprocess
from django.shortcuts import render
import torch


def generate_music(request):
    # connect generate.py
    generate_py_path = 'generate.py'

    track_roles = ['main_melody', 'sub_melody', 'accompaniment', 'bass', 'pad', 'riff']
    chord_progression = "Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G"

    num_measures = 4

    for track_role in track_roles:
        command = f"python {generate_py_path} \
            --checkpoint_dir checkpoint_best.pt \
            --output_dir music_output \
            --bpm 130 \
            --audio_key amajor \
            --time_signature 4/4 \
            --pitch_range mid_low \
            --num_measures {num_measures} \
            --inst string_cello \
            --genre cinematic \
            --min_velocity 2 \
            --max_velocity 127 \
            --track_role {track_role} \
            --rhythm standard \
            --chord_progression {chord_progression} \
            --num_generate 1"

        subprocess.call(command, shell=True)

    return render(request, 'music.html')

# def generate_music(request, response):
#     # generate.py 파일 경로
#     generate_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ComMU_code', 'generate.py')
#
#     # 파라미터 값 지정
#     track_roles = ['main_melody', 'sub_melody', 'accompaniment', 'bass', 'pad', 'riff']
#     chord_progression = response
#     bpm = "72"
#     audio_key = "amajor"
#     time_signature = "4/4"
#     pitch_range = "mid_low"
#     num_measures = 4
#     inst = "string_cello"
#     genre = "cinematic"
#
#     for track_role in track_roles:
#         command = f"python {generate_py_path} \
#             --checkpoint_dir ai_music/ComMU_code/checkpoint_best.pt \
#             --output_dir ai_music/ComMU_code/music_output \
#             --bpm {bpm} \
#             --audio_key {audio_key} \
#             --time_signature {time_signature} \
#             --pitch_range {pitch_range} \
#             --num_measures {num_measures} \
#             --inst {inst} \
#             --genre {genre} \
#             --min_velocity 2 \
#             --max_velocity 127 \
#             --track_role {track_role} \
#             --rhythm standard \
#             --chord_progression {chord_progression} \
#             --num_generate 1"
#
#         subprocess.call(command, shell=True)
#
#     combine_midi(request)  # combine_midi 함수 호출