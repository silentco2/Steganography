def encode_video():
    video_name = input('Name of the video you want to encode : ')
    data = [i+pin for i in input("Enter data to be encoded : ").split(' ')]
    if not len(data):
        raise ValueError('Data is empty')
    cap = cv2.VideoCapture(video_name)
    framespersecond = int(cap.get(cv2.CAP_PROP_FPS))
    success, image = cap.read()
    audio = moviepy.editor.VideoFileClip(video_name).audio
    count = 0
    while success:
        if count < len(data):
            image = hide_data(image, bi_converter(data[count]))
        cv2.imwrite(f"{video_name.split('.')[0]}/frame{count}.png", image)
        success, image = cap.read()
        # print('Read a new frame: ', success)
        count += 1
    new_video_name = input('Name of the new encoded video : ')
    images = [f'frame{i}.png' for i in range(len(os.listdir(video_name.split('.')[0])))]
    height, width, layers = cv2.imread(os.path.join(video_name.split('.')[0], images[0])).shape

    video = cv2.VideoWriter(new_video_name, cv2.VideoWriter_fourcc(*'mp4v'), framespersecond, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(video_name.split('.')[0], image)))

    moviepy.editor.VideoFileClip(video_name).set_audio(audio).write_videofile(new_video_name)
    cv2.destroyAllWindows()
    video.release()

def decode_video():
  video_name = input('Name of the video you want to decode : ')
  cap = cv2.VideoCapture(video_name)
  success, image = cap.read()
  text = ''
  count = 0
  while success:
      try:
          text += ' ' + show_data(image)
      except ValueError:
          break
      success, image = cap.read()
      count += 1
  if not len(text):
      raise ValueError('Error the pin was incorrect')
  return text
 
