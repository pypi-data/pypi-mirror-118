from PIL import Image, ImageDraw, ImageFont

def color_text(text):
    text=text.replace('\n',' ')
    text=text.replace('</i>','')
    text=text.replace('<i>','')

    TagDict={
    'blue{':'#00a2ff', 
    'Navy{':'#000dff', 
    'Cyan{':'#61f7ff',
    'pink{':'#ff00d4',
    'yellow{':'#ffee00',
    'green{':'#11f227',
    'orange{':'#ff9100',
    'red{':'#ff0000',
    'purple{':'#bf00ff',
    'brown{':'#A0522D',
    'gray{':'#a6a4a4',
    } 

    # # # normalize Text 
    text=text.replace(' {','{').replace('{ ','{').replace(' }','}').replace('{end}','}')
    for key in TagDict:
        text=text.replace(key,' '+ key +' ')

    text=text.replace('}',' } ').replace('.',' . ').replace(',',' , ').replace('!',' ! ').replace(':',' : ')
    
    colorList=[]
    colorofword='#ffffff'
    for word in text.split():
        if word in TagDict:
            colorofword=TagDict[word]
        elif word == '}':
            colorofword='#ffffff'
        elif word not in {'.',',','!',':'}:
            colorList.append(colorofword)

    for key in TagDict:
        text=text.replace(key,'')

    text=text.replace('}','').replace('  ',' ').replace('  ',' ').replace(' . ','. ')\
                             .replace(' , ',', ').replace(' ! ','! ').replace(' : ',': ')
       

    List=(text,colorList)
    return List

def Text_to_png(coloredText,outputfilename):
    
    txt,colorList=coloredText
    if len(colorList) != len(txt.split()):
        raise ValueError('the length of \'colorList\' and the number of words in \'txt\' must be equal.')
    W_image,H_image=(1227,500)
    img = Image.new('RGBA', (W_image,H_image), color = (0,0,0,0))
    fnt = ImageFont.truetype('source\\seguibl.ttf', 80)
    stroke_w=2
    d = ImageDraw.Draw(img)
    words=txt.split()


    Length_List=[]
    counter=0
    sentence=''
    Margin=d.textsize('wordsss',font=fnt,stroke_width=stroke_w)[0]
    for word in reversed(words):
        counter+=1
        sentence_previous=sentence
        sentence+=word+' '
        L_previous=d.textsize(sentence_previous,font=fnt,stroke_width=stroke_w)[0]
        L=d.textsize(sentence,font=fnt,stroke_width=stroke_w)[0]
        if L>=W_image-Margin :
            if L<=W_image :
                Length_List.append((counter,L))
                counter=0
                sentence=''
            else:
                Length_List.append((counter-1,L_previous))
                counter=1
                sentence=word+' ' 
                L=d.textsize(sentence,font=fnt,stroke_width=stroke_w)[0]  
    if counter!= 0:        
        Length_List.append((counter,L))
    Length_List.reverse()
    newline_pos=Cumulative([i[0] for i in Length_List])
    newline_pos.pop()

    x=0
    counter=0
    line_counter=0
    line_height=d.textsize('wordsss'+' ',font=fnt,stroke_width=stroke_w)[1]
    y_margin=int(line_height/2)
    x_start=int((W_image-Length_List[line_counter][1])/2)
    y_start=img.height-len(Length_List)*line_height

    for word in words:
        counter+=1 
        word_size=d.textsize(word+' ',font=fnt,stroke_width=stroke_w)
        d.text((x_start+x,y_start-y_margin+(line_counter)*line_height), word, font=fnt, fill=colorList[counter-1],stroke_width=stroke_w, stroke_fill='black')
        x+=word_size[0]
        if (counter in newline_pos):
            line_counter+=1
            x_start=int((W_image-Length_List[line_counter][1])/2)
            x=0
            
    img.save(outputfilename)

def Cumulative(lists): 
    cu_list = [] 
    length = len(lists) 
    cu_list = [sum(lists[0:x:1]) for x in range(0, length+1)] 
    return cu_list[1:]

