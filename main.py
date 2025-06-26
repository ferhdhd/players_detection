from ultralytics import YOLO
from video import read_video, save_video

def main():
    video_frames = read_video('videos/fut-teste.mp4')

    save_video(video_frames, 'videos_saida/output.avi')

if __name__ == '__main__':
    main()