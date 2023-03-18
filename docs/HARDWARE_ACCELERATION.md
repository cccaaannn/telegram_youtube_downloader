## Running ffmpeg with hardware acceleration
---

### Get supported encoders from ffmpeg
```shell
ffmpeg -encoders
```

### Add this line to your `configs/config.yaml` file's `video_options` section
- Replace `h264_nvenc` with your encoder
```yaml
postprocessor_args: ['-c:v', 'h264_nvenc']
```

### It should look like this
```yaml
video_options:
  postprocessor_args: ['-c:v', 'h264_nvenc']
  postprocessors: 
    - key: "FFmpegVideoConvertor"
      preferedformat: "mp4"
```

### Check the example on Google Colab
<a href="https://colab.research.google.com/drive/16dBProJTucW5P0whHgmTdFMkGm9x3T8c?usp=sharing" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
