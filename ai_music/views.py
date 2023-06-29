from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from .ComMU_code.combine import MidiCombine
from django.urls import reverse
# import subprocess
# import torch
import os
from django.http import JsonResponse
from django.core.files import File
from .models import Music
# from .call_gpt import get_completion
# import re

import shutil
from midi2audio import FluidSynth
from django.http import FileResponse


def home(request):
    return render(request, 'main/main.html')


def music(request):
    return render(request, 'main/music.html')


def alarm(request):
    return render(request, 'main/alarm.html')


# GPT 호출
def call_gpt(request):
    sleep_factor = ['수면 잠복기', '수면 시간', '컨디션', '스트레스', '수면의 효율']
    prediction = 1
    prompt = f"""
    <user>: 당신은 수면 치료사입니다. \
    당신의 작업은 일관된 스타일로 답변하는 것입니다.\
    다음의 수면 점수를 받은 사람에게 좋은 수면의 질을 개선할 수 있는 음악 중 어떤 분위기의 수면 유도 음악을 들으면 좋을지 추천해주세요.\
    수면의 질을 예측한 점수는 1-5점 척도입니다.\
    1점이 가장 숙면을 취하지 못한 사람의 점수이며, 점수가 높아질수록 좋은 수면을 취한 것입니다.\
    수면의 질을 예측한 알고리즘은 다음과 같습니다.\

    먼저 수면 데이터에서 다음의 12개의 요인 중 ['수면 시간', '수면 잠복기', '수면의 효율', '취침 중 자다 깬 횟수','렘 수면','스트레스', '감정 상태', '수면 문제', '컨디션', '카페인 섭취량', '알코올 섭취량', '보행수'] user별로 각자에게 가장 영향을 많이 미치는 요인이 무엇인지 랜덤포레스트 알고리즘을 활용하여 도출합니다.
    예를 들어, user1에게 가장 영향을 미치는 수면 요인은 ['수면 잠복기', '수면 시간', '컨디션']입니다.
    따라서 수면의 질에 수면 잠복기가 가장 영향을 많이 미치고 있습니다.
    이 요인들을 LSTM알고리즘에 넣어 도출한 수면의 질 예측 점수는 1-5점 중에서 도출됩니다.
    user1의 경우, 예측 점수는 1점입니다.

    수면에 영향을 미치는 요인과 수면의 질 예측 점수를 고려하여 수면의 질을 높여주는 음악의 분위기를 추천해주세요.

    <sleep therapist>:
    user1에게 맞는 음악의 분위기를 추천드리겠습니다.
    수면에 영향을 미치는 요인은 ['수면 잠복기', '수면 시간', '컨디션']입니다.
    수면의 질 예측 점수는 1점입니다.

    수면의 질을 높여주는 음악으로는 다음과 같은 분위기의 음악을 추천해드릴 수 있습니다:
    "
    연주곡이나 소리 효과가 포함된 피아노 음악
    자연 소리나 새소리, 바다 파도 소리 등의 힐링 음악
    주파수 조정 음악이나 딥 슬립 및 명상을 위한 음악
    심호흡과 같은 안정화 기법을 위한 음악
    "

    <user>: 당신은 수면 치료사입니다.
    다음의 수면 점수를 받은 사람에게 좋은 수면의 질을 개선할 수 있는 음악 중 어떤 분위기의 수면 유도 음악을 들으면 좋을지 추천해주세요.
    수면의 질을 예측한 점수는 1-5점 척도입니다.
    1점이 가장 숙면을 취하지 못한 사람의 점수이며, 점수가 높아질수록 좋은 수면을 취한 것입니다.
    수면의 질을 예측한 알고리즘은 다음과 같습니다.

    먼저 수면 데이터에서 다음의 12개의 요인 중 ['수면 시간', '수면 잠복기', '수면의 효율', '취침 중 자다 깬 횟수','렘 수면','스트레스', '감정 상태', '수면 문제', '컨디션', '카페인 섭취량', '알코올 섭취량', '보행수'] user별로 각자에게 가장 영향을 많이 미치는 요인이 무엇인지 랜덤포레스트 알고리즘을 활용하여 도출합니다.
    user에게 가장 영향을 미치는 수면 요인은 {sleep_factor} 입니다.
    따라서 수면의 질에 수면 잠복기가 가장 영향을 많이 미치고 있습니다.
    이 요인들을 LSTM알고리즘에 넣어 도출한 수면의 질 예측 점수는 1-5점 중에서 도출됩니다.
    user의 경우, 예측 점수는 {prediction}점입니다.

    수면에 영향을 미치는 요인과 수면의 질 예측 점수를 고려하여 수면의 질을 높여주는 음악의 분위기를 추천해주세요.

    <sleep therapist>:
    user에게 맞는 음악의 분위기를 추천드리겠습니다.
    수면에 영향을 미치는 요인은 {sleep_factor}입니다.
    수면의 질 예측 점수는 {prediction}점입니다.

    수면의 질을 높여주는 음악으로는 다음과 같은 분위기의 음악을 추천해드릴 수 있습니다:
    "
    연주곡이나 소리 효과가 포함된 피아노 음악
    자연 소리나 새소리, 바다 파도 소리 등의 힐링 음악
    주파수 조정 음악이나 딥 슬립 및 명상을 위한 음악
    심호흡과 같은 안정화 기법을 위한 음악
    "

    마지막 <user>질문의 <sleep therapist>의 답변만 작성해주세요.

    """
    response = get_completion(prompt)

    response = "<sleep therapist>: \nuser에게 맞는 음악의 분위기를 추천드리겠습니다. \n수면에 영향을 미치는 요인은 ['수면 잠복기', '수면 시간', '컨디션', '스트레스', '수면의 효율']입니다. \n수면의 질 예측 점수는 1점입니다.\n\n수면의 질을 높여주는 음악으로는 다음과 같은 분위기의 음악을 추천해드릴 수 있습니다:\n\"\n연주곡이나 소리 효과가 포함된 피아노 음악\n자연 소리나 새소리, 바다 파도 소리 등의 힐링 음악\n주파수 조정 음악이나 딥 슬립 및 명상을 위한 음악\n심호흡과 같은 안정화 기법을 위한 음악\n\""

    pattern = r"(연주곡이나 소리 효과가 포함된 피아노 음악\n자연 소리나 새소리, 바다 파도 소리 등의 힐링 음악\n주파수 조정 음악이나 딥 슬립 및 명상을 위한 음악\n심호흡과 같은 안정화 기법을 위한 음악)"
    extracted_text = re.findall(pattern, response, re.MULTILINE)

    if extracted_text:
        recommended_music = extracted_text[0]
    else:
        print("해당 내용을 찾을 수 없습니다.")

    prompt = f"""
    당신은 수면 작곡가입니다.


    <user>: 저를 위해 수면 유도 음악 플레이리스트를 만들어주세요.\
    다음과 같은 분위기의 음악 코드를 작성해주세요.\
    연주곡이나 소리 효과가 포함된 피아노 음악
    자연 소리나 새소리, 바다 파도 소리 등의 힐링 음악

    음악 코드 예시는 다음과 같습니다.\
    G Major Chord (G, B, D) \
    D Major Chord (D, F#, A)\
    A Major Chord (A, C#, E)\
    E Major Chord (E, G#, B)\
    F Major Chord (F, A, C) \
    Bb Major Chord (Bb, D, F)

    답변은 이렇게 4개의 코드로만 작성해주세요.\
    "C-E-G-C"

    <composer>: "C-E-G-C"

    <user>: 저를 위해 수면 유도 음악 플레이리스트를 만들어주세요.\
    {recommended_music}와 같은 분위기의 음악 코드를 작성해주세요.\
    답변은 이렇게 4개 단위의 코드로만 작성해주세요.\
    "Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G"


    <composer>: "Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G-Am-F-C-G"

    마지막 <user>질문의 <composer>의 답변만 작성해주세요.

    """

    response = get_completion(prompt)

    response_list = re.findall(r'"([^"]+)"', response)
    if response_list:
        response_str = response_list[0]
    else:
        response_str = ""
    response = response_str
    generate_music(request, response)  # generate_music 함수 호출
    return JsonResponse({'status': 'success'})


def generate_music(request, response):
    # generate.py 파일 경로
    generate_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ComMU_code', 'generate.py')
    # 파라미터 값 지정
    track_roles = ['main_melody', 'sub_melody', 'accompaniment', 'bass', 'pad', 'riff']
    bpm = "72"
    audio_key = "amajor"
    time_signature = "4/4"
    pitch_range = "mid_low"
    num_measures = 4
    inst = "string_cello"
    genre = "cinematic"

    for track_role in track_roles:
        command = f"python {generate_py_path} \
            --checkpoint_dir ai_music/ComMU_code/checkpoint_best.pt \
            --output_dir ai_music/ComMU_code/music_output \
            --bpm {bpm} \
            --audio_key {audio_key} \
            --time_signature {time_signature} \
            --pitch_range {pitch_range} \
            --num_measures {num_measures} \
            --inst {inst} \
            --genre {genre} \
            --min_velocity 2 \
            --max_velocity 127 \
            --track_role {track_role} \
            --rhythm standard \
            --chord_progression \"{response}\" \
            --num_generate 1"

        subprocess.call(command, shell=True)

    combine_midi(request)  # combine_midi 함수 호출
    return HttpResponseRedirect(reverse('ai_music:music'))


# midi 파일 합치기
def combine_midi(request):
    converter = MidiCombine()
    combined_midi_file = converter.combine_midi_files()

    print("합치기 및 변환이 완료되었습니다. 최종 생성 파일:", combined_midi_file)

    # Music 모델 인스턴스 생성
    music = Music()
    with open(combined_midi_file, 'rb') as file:
        music.midi_file.save('combined.mid', File(file))  # midi_file 필드에 업로드된 파일 저장
    music.save()  # 모델 인스턴스 저장

    return JsonResponse({'midi_url': music.midi_file.url})
