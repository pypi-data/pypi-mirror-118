from ice_moviepy.editor import *
from ice_moviepy.video.tools.subtitles import SubtitlesClip, ClipItem 
import pysrt 

def produce_clip(Clip,clipitem,outputname,logo_path=None):
    """
    docstring
    """
    
    Clip = Clip.subclip(cvsecs(clipitem.start)-clipitem.risetime_sec,cvsecs(clipitem.end)+clipitem.risetime_sec)  
    generator = lambda txt: TextClip(txt,method='pango', font='Segoe-UI-Bold', fontsize=80, color='white',stroke_color='red', stroke_width=2.5)
    txt_clip = SubtitlesClip(clipitem,generator)    
    txt_clip = txt_clip.set_pos(("bottom"))
    if logo_path==None:
        video = CompositeVideoClip([Clip,txt_clip]) 
    else:
        logo = ImageClip(logo_path).set_duration(Clip.duration).resize(height=110).margin(left=8, top=8, opacity=0).set_pos(("left","top"))
        video = CompositeVideoClip([Clip, logo ,txt_clip]) 
    # Overlay the text clip on the first video clip   
    video.write_videofile(outputname+".mp4",codec='libx264' )

def subtitle2video(clip_name,subtitle_name,logo_path=None):
    clip = VideoFileClip(clip_name)  
    subs = pysrt.open(subtitle_name)
    List_subs_of_clip=[]
    List_of_clips=[]
    for sub in subs:
        if not sub.text.endswith("{end}"):
            List_subs_of_clip.append(sub)
        else:
            List_subs_of_clip.append(sub)
            List_of_clips.append(ClipItem(List_subs_of_clip))
            List_subs_of_clip=[]
    if len(List_subs_of_clip)!=0:
        List_of_clips.append(ClipItem(List_subs_of_clip))
    counter=0
    for clipitem in List_of_clips:
        counter=counter+1
        produce_clip(clip,clipitem,str(counter),logo_path)


