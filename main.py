from video import read_video, save_video
from tracker import Tracker

def main():
    video_frames = read_video('videos/teste2.mp4')

    tracker = Tracker("models/best-yolo8.pt")

    tracks = tracker.get_object_tracks(video_frames, read_from_stub=False, stub_path='stub/track_stubs.pkl')

    output_frames = tracker.draw_annotations(video_frames, tracks)

    save_video(output_frames, 'videos_saida/output.avi')

if __name__ == '__main__':
    main()