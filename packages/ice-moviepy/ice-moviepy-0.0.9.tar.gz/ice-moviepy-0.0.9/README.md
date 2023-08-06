# ice-moviepy [![License: MIT](https://img.shields.io/badge/License-MIT-gree.svg)]


a package for extracting short subtitled clips from movies by subtitle.srt file.

## Installation

Use the package manager [pip] to install ice-moviepy.

```bash
pip install ice-moviepy
```

## Usage
given a movie with a srt file subtitle, cut some parts of subtitle.srt and paste them into another file, such as sub.srt and run the following: 

```python
import ice_moviepy

ice_moviepy.subtitle2video("Video.mkv",'Sub.srt','logo.png')
```
or 

```python
ice_moviepy.subtitle2video("Video.mkv",'Sub.srt')
```
if you don't want to attach a watermark on it.

## editing subtitle 
you can colorize different parts of subtitle. for example you can use red{...}, blue{...}, yellow{...} and so on, to colorize your subtitle.

Place an {end} at the end of the block you want to cut out as a separate clip.

```
9
00:00:48,920 --> 00:00:51,151
There are two
kinds of pain.

10
00:00:51,280 --> 00:00:53,272
The sort of pain
blue{that makes} you strong

11
00:00:53,360 --> 00:00:57,240
red{or useless} yellow{pain}, the purple{sort of}
pain blue{that's} only orange{suffering}. {end}
```

![alt text](example.png)