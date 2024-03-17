import ffmpeg
from flask import Flask, send_file

app = Flask(__name__)

class VideoJoiner:
    def __init__(self, new_generated_video,count:int,isFirst:bool):
        #isFirst is a boolean that checks if the video is the first video in the merging queue
        #if first, then the input1 is the new_generated_video
        #isFirst is handled from the video_generator code
        #it should pass True in the first iteration, and False in the rest

        #input1 is used for new generated videos that are sent to this function
        #input2 is used for the already merged video
        if isFirst:
            self.input2 = new_generated_video
            return
        else:
            self.input1 = new_generated_video
        self.count = count

    def video_merger(self):

        #API control
        #if all the prompts are done, run the flask app
        if self.count == 0:
            app.run(debug=True)
        #helper function API
        @app.route('/get_video')
        def get_video(video):
            # Return the video file
            return send_file(video, as_attachment=True)
        
        # Separate audio and video streams for input1
        video1 = ffmpeg.input(self.input1).video
        audio1 = ffmpeg.input(self.input1).audio

        # Separate audio and video streams for input2
        video2 = ffmpeg.input(self.input2).video
        audio2 = ffmpeg.input(self.input2).audio

        # Concatenate video streams and output to a temporary file
        merged_video = ffmpeg.concat(video1, video2, v=1).output('temp_video.mp4')
        ffmpeg.run(merged_video)

        # Concatenate audio streams and output to a temporary file
        merged_audio = ffmpeg.concat(audio1, audio2, a=1).output('temp_audio.mp3')
        ffmpeg.run(merged_audio)

        # Combine the merged video and audio streams
        final_output = ffmpeg.input('temp_video.mp4').output('temp_audio.mp3', 'final_output.mp4')
        ffmpeg.run(final_output)
        self.count -=1 

        # Return the path to the final output file
        return final_output