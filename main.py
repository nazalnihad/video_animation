import cv2
# Edit this function to apply a different effect


def apply_watercolor_effect(frame, resize_factor=0.35, sigma_s=3, iterations=[(3, 10, 5), (3, 20, 10), (5, 30, 10)]):
    # Resize the frame
    frame_resized = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)

    # Remove impurities from the frame
    frame_cleared = frame_resized.copy()
    for _ in range(3):
        frame_cleared = cv2.medianBlur(frame_cleared, 3)
    frame_cleared = cv2.edgePreservingFilter(frame_cleared, sigma_s=sigma_s)

    # Bilateral Image Filtering
    frame_filtered = frame_cleared.copy()
    for it in iterations:
        frame_filtered = cv2.bilateralFilter(frame_filtered, *it)

    # Sharpen the frame
    gaussian_mask = cv2.GaussianBlur(frame_filtered, (7, 7), 2)
    frame_sharp = cv2.addWeighted(frame_filtered, 1.5, gaussian_mask, -0.5, 0)
    frame_sharp = cv2.addWeighted(frame_sharp, 1.4, gaussian_mask, -0.2, 10)

    return frame_sharp


def extract_frames(video_path):
    # Open the video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Cannot open the video.")
        return None

    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Append the frame to the list
        frames.append(frame)

    # Get the frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Release resources
    cap.release()

    return frames, frame_width, frame_height


def edit_and_combine(frames, output_video_path, output_frame_width, output_frame_height, output_frame_rate):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, output_frame_rate,
                          (output_frame_width, output_frame_height))

    for frame in frames:
        # Apply the watercolor effect to each frame
        watercolored_frame = apply_watercolor_effect(frame)

        # Resize the watercolored frame to the desired output size
        watercolored_frame = cv2.resize(
            watercolored_frame, (output_frame_width, output_frame_height))

        # Write the frame to the output video
        out.write(watercolored_frame)

    # Release the VideoWriter
    out.release()


if __name__ == "__main__":
    input_video = input("Enter input video path : ")
    output_video = input("Enter output video path : ")

    # Extract frames from the input video
    frames, frame_width, frame_height = extract_frames(input_video)

    # Define the output frame dimensions and frame rate
    output_frame_width = frame_width
    output_frame_height = frame_height
    output_frame_rate = 30

    # Edit and combine frames to create the output video
    edit_and_combine(frames, output_video, output_frame_width,
                     output_frame_height, output_frame_rate)
    print("Done")
