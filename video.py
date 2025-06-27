import cv2

def read_video(path):
    capture = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        frames.append(frame)
        print("oi\n")
    return frames

def save_video(output_frames, output_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 24, (output_frames[0].shape[1], output_frames[0].shape[0]))
    for frame in output_frames:
        out.write(frame)
    out.release()
