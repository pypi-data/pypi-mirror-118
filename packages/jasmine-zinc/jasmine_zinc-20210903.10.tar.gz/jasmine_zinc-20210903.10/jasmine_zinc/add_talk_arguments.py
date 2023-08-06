import argparse

def add_talk_arguments_effects(parser: argparse.ArgumentParser):
    parser.add_argument('--effect-volume', type=float, default=1, help='0-2, step 0.01')
    parser.add_argument('--effect-speed', type=float, default=1, help='0.5-4, step 0.01')
    parser.add_argument('--effect-pitch', type=float, default=1, help='0.5-2, step 0.01')
    parser.add_argument('--effect-intonation', type=float, default=1, help='0-2, step 0.01')
    parser.add_argument('--effect-shortpause', type=int, default=150, help='80-500, step 1')
    parser.add_argument('--effect-longpause', type=int, default=370, help='100-2000, step 1')

def add_talk_arguments_emotions(parser: argparse.ArgumentParser):
    parser.add_argument('--emotion-joy', type=float, default=0, help='0-1, step 0.01')
    parser.add_argument('--emotion-anger', type=float, default=0, help='0-1, step 0.01')
    parser.add_argument('--emotion-sadness', type=float, default=0, help='0-1, step 0.01')

def add_talk_arguments(parser: argparse.ArgumentParser):
    add_talk_arguments_effects(parser=parser)
    add_talk_arguments_emotions(parser=parser)
