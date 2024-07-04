cat ../../../../scenes.py | grep 'class ' | cut -f2- -d ' ' | cut -f 1 -d '(' | sed "s/^/file '/" | sed "s/$/.mp4'/" > scenes-names.txt
sed -i '$ d' scenes-names.txt
sed -i '$ d' scenes-names.txt
sed -i '$ d' scenes-names.txt
echo "file '/home/thomasmong/Videos/demo/final-demo.mp4'" >> scenes-names.txt
echo "file 'CommentLP.mp4'" >> scenes-names.txt
#echo "file '/home/thomasmong/Videos/demo-MM/final-demo-MM.mp4'" >> scenes-names.txt
#echo "file 'CommentMM.mp4'" >> scenes-names.txt
echo "file 'Credits.mp4'" >> scenes-names.txt
# Concat files
ffmpeg -y -f concat -safe 0 -i scenes-names.txt -c copy output_scenes.mp4
# Get video duration
dur=$(ffprobe -i output_scenes.mp4 -show_format -v quiet | sed -n 's/duration=//p')
start_time_fo=$((${dur%.*}-2))
echo $dur
echo $start_time_fo
# Fade in/out audio
ffmpeg -y -i ../../../sound/reflected-light-147979.mp3 -af "afade=d=2,afade=t=out:st=$start_time_fo:d=2" audio.mp3

# Add audio
ffmpeg -y -i output_scenes.mp4 -i audio.mp3 -c:v copy -map 0:v -map 1:a -shortest -y output.mp4
