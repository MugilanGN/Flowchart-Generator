import re,os,math
from PIL import Image, ImageDraw, ImageFont

def read():

    #get raw lines out of txt
    
    converter = os.path.realpath(__file__)
    self_path = re.compile(r'(.+)testing5.py')
    text_path = re.search(self_path,converter).group(1) + "enter.txt"
    text_file = open(text_path,"r")
    lines = text_file.readlines()
    text_file.close()

    #remove the \n's from the lines individually
    lines.insert(0, "START")
    
    for i in range(0,len(lines)):
        if lines[i][-1] == '\n':
            lines[i] = lines[i][:-1]

    #removes indents
    
    indent_filter = re.compile(r'^\s*(.*)$')
    for i in range(0,len(lines)):
        lines[i] = re.search(indent_filter,lines[i]).group(1)

    lines.append("STOP")
    

    return lines

def translation(lines,font_data):
    
    input_re = re.compile(r'^INPUT\s(.+)')
    output_re = re.compile(r'^OUTPUT\s(.+)')

    if_re = re.compile(r'^IF\s(.+)\sTHEN$')
    else_re = re.compile(r'^ELSE$')
    endif_re = re.compile(r'^ENDIF$')

    chart_code = []

    amount_per_branch = {}
    beginning_of_split = {}

    branch_width = {}
    layer_height = {}

    #font_path = r"C:/Windows/Fonts/Arial.ttf"
    #font_size = 20

    font_path = font_data['path']
    font_size = font_data['size']
    font = ImageFont.truetype(font_path, font_size)

    img = Image.new('RGB', (10, 10), color = 'white')
    draw = ImageDraw.Draw(img)
    
    x = [1]
    y = [1]
    
    for i in range(0,len(lines)):
        line = lines[i]
        
        if x[-1] not in amount_per_branch:
            amount_per_branch[x[-1]] = 0
            beginning_of_split[x[-1]] = 0
            branch_width[x[-1]] = 0

        if y[-1] not in layer_height:
            layer_height[y[-1]] = draw.textsize("a",font=font)[1] + font_size

        if line == "START" or line == "STOP":
            
            if line == "STOP":
                chart_code.append({"type":"Terminator","content":line,"position":[x[-1],y[-1]],"role":'t'})
            else:
                chart_code.append({"type":"Terminator","content":line,"position":[x[-1],y[-1]],"role":'n'})
                
            if draw.textsize(line,font=font)[0] + font_size * 2 > branch_width[x[-1]]:
                branch_width[x[-1]] = draw.textsize(line,font=font)[0] + font_size * 2

            if draw.textsize(line,font=font)[1] + font_size + 2*font_size > layer_height[y[-1]]:
                layer_height[y[-1]] = draw.textsize(line,font=font)[1] + 2*font_size
                
            amount_per_branch[x[-1]] += 1
            y[-1] +=1
        
        elif re.search(input_re,line):
            chart_code.append({"type":"IO","content":line,"position":[x[-1],y[-1]],"role":'n'})

            if draw.textsize(line,font=font)[0] + font_size * 4 > branch_width[x[-1]]:
                branch_width[x[-1]] = draw.textsize(line,font=font)[0] + font_size * 4

            if draw.textsize(line,font=font)[1] + font_size > layer_height[y[-1]]:
                layer_height[y[-1]] = draw.textsize(line,font=font)[1] + font_size
                
            amount_per_branch[x[-1]] += 1
            y[-1] +=1
            
        elif re.search(output_re,line):             
            chart_code.append({"type":"IO","content":line,"position":[x[-1],y[-1]],"role":'n'})

            if draw.textsize(line,font=font)[0] + font_size * 4> branch_width[x[-1]]:
                branch_width[x[-1]] = draw.textsize(line,font=font)[0] + font_size * 4

            if draw.textsize(line,font=font)[1] + font_size > layer_height[y[-1]]:
                layer_height[y[-1]] = draw.textsize(line,font=font)[1] + font_size
                
            amount_per_branch[x[-1]] += 1
            y[-1] +=1

        elif re.search(if_re,line):
            chart_code.append({"type":"Decision","content":re.search(if_re,line).group(1),"position":[x[-1],y[-1]],"role":'o'})

            if len(line) > len("IF")+1:    
                width = 3/2*draw.textsize(line,font=font)[0]
                height = 5*draw.textsize(line,font=font)[1] 
            else:
                width = 5*font_size
                height = 5*font_size

            if width > branch_width[x[-1]]:
               branch_width[x[-1]] = width

            if height > layer_height[y[-1]]:
                layer_height[y[-1]] = height
            
            amount_per_branch[x[-1]] += 1

            beginning_of_split[x[-1]] = y[-1]
            
            x.append(2*x[-1])
            y.append(y[-1]+1)

        elif re.search(else_re,line):
            if x[-1] % 2 == 0:
                x[-1] += 1
                y[-1] = y[-2] + 1
            else:
                x = x[:-1]
                y = y[:-1]

        elif re.search(endif_re,line):
            next_line = lines[i+1]
            
            if amount_per_branch[x[-1]-1] > amount_per_branch[x[-1]]:
                amount_per_branch[x[-2]] += amount_per_branch[x[-1]-1]
                y[-2] = amount_per_branch[x[-1]-1] + beginning_of_split[x[-2]] + 1
            else:
                amount_per_branch[x[-2]] += amount_per_branch[x[-1]]
                y[-2] = amount_per_branch[x[-1]] + beginning_of_split[x[-2]] + 1
                
            amount_per_branch[x[-1]] = 0
            amount_per_branch[x[-1]-1] = 0
                
            y = y[:-1]
            x = x[:-1]

            chart_code.append({"type":"Connector","content":"c","position":[x[-1],y[-1]],"role":'c'})
            
            amount_per_branch[x[-1]] += 1
            y[-1] += 1

            
        else:   
            chart_code.append({"type":"Process","content":line,"position":[x[-1],y[-1]],"role":'n'})

            if draw.textsize(line,font=font)[0] + font_size * 2 > branch_width[x[-1]]:
                branch_width[x[-1]] = draw.textsize(line,font=font)[0] + font_size * 2

            if draw.textsize(line,font=font)[1] + font_size > layer_height[y[-1]]:
                layer_height[y[-1]] = draw.textsize(line,font=font)[1] + font_size
                
            amount_per_branch[x[-1]] += 1
            y[-1] +=1

    del draw,img

    max_branches = max(amount_per_branch)
            
    count = 0
    
    while max_branches != 1:
        if max_branches % 2 == 0:
            max_branches /= 2
        else:
            max_branches = (max_branches - 1) / 2
        count += 1
    
    max_branch = 2 ** (count+1) - 1
    
    max_y = amount_per_branch[1]
    
    return chart_code,max_branch,max_y,layer_height,branch_width

def drawer(chart_code,max_branch,max_y,layer_height,branch_width,font_data):

    class newNode: 
        def __init__(self, data): 
            self.data = data  
            self.left = self.right = None

    def insertLevelOrder(arr, root, i, n): 
        if i < n: 
            temp = newNode(arr[i])  
            root = temp  
            root.left = insertLevelOrder(arr, root.left, 2 * i + 1, n)  
            root.right = insertLevelOrder(arr, root.right, 2 * i + 2, n) 
        return root 

    def inOrder(root,result): 
        if root != None: 
            inOrder(root.left,result)
            result.append(root.data)
            inOrder(root.right,result) 
  
    def Restructure(arr):
        root = None
        root = insertLevelOrder(arr, root, 0, len(arr))
        result = []
        inOrder(root,result)
        return result
    
    def Terminator(text,position):
        
        width = draw.textsize(text,font=font)[0] + font_size * 2
        height = draw.textsize(text,font=font)[1] + font_size * 2
        
        x = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2 - width/2
        y = combined_heights[position[1]]

        coords = [(x,y),(x+width,y+height)]

        draw.ellipse(coords,fill=None,outline="black")
        draw.text((x+font_size,y+height/2-scale_constant), text, fill='black',font=font)

        return height
        
    def Decision(text,position):
        
        def diamond(coords,width,height):
            draw.line([(coords[0]+width/2,coords[1]),(coords[0]+width,coords[1]+height/2)],fill='black', width=1)
            draw.line([(coords[0]+width/2,coords[1]),(coords[0],coords[1]+height/2)],fill='black', width=1)

            draw.line([(coords[0],coords[1]+height/2),(coords[0]+width/2,coords[1]+height)],fill='black', width=1)
            draw.line([(coords[0]+width,coords[1]+height/2),(coords[0]+width/2,coords[1]+height)],fill='black', width=1)

        if len(text) > len("IF")+1:    
            width = 3/2*draw.textsize(text,font=font)[0]
            height = 5*draw.textsize(text,font=font)[1] 
            text_offset = draw.textsize(text,font=font)[0]/4
            
        else:
            width = 5*font_size
            height = 5*font_size
            text_offset = (width - draw.textsize(text,font=font)[0])/2

        x = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2 - width/2
        y = combined_heights[position[1]]
        
        diamond((x,y),width,height)

        draw.text((x+width/2-scale_constant,y+height/4-scale_constant), "IF", fill='black',font=font)
        draw.text((x+text_offset,y+height/2-scale_constant), text, fill='black',font=font)

        return height,width

    def Process(text,position):
        
        width = draw.textsize(text,font=font)[0] + font_size * 2
        height = draw.textsize(text,font=font)[1] + font_size

        x = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2 - width/2 
        y = combined_heights[position[1]]
        
        coords = [(x,y),(x+width,y+height)]
        
        draw.rectangle(coords,fill=None,outline='black')
        draw.text((x+font_size,y+scale_constant), text, fill='black',font=font)

        return height

    def IO(text,position):
        
        def parallelogram(coords,width,height,offset):
            draw.line([(coords[0],coords[1]+height),(coords[0]+width,coords[1]+height)] ,fill='black', width=1)
            draw.line([(coords[0]+offset,coords[1]),(coords[0]+width+offset,coords[1])] ,fill='black', width=1)

            draw.line([(coords[0]+offset,coords[1]),(coords[0],coords[1]+height)] ,fill='black', width=1)
            draw.line([(coords[0]+width+offset,coords[1]),(coords[0]+width,coords[1]+height)] ,fill='black', width=1)

        width = draw.textsize(text,font=font)[0] + font_size * 2
        height = draw.textsize(text,font=font)[1] + font_size
        offset = font_size

        x = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2 - width/2  - offset/2
        y = combined_heights[position[1]]
        
        parallelogram((x,y),width,height,offset)

        draw.text((x+font_size + offset/2,y+scale_constant), text, fill='black',font=font)

        return height
    
    def Flowline(role,position,height,chart_code,width):

        def arrow(coords, height,direction):
            h = int(height)
            L = int(height)
            if direction == "left":
                draw.line([(coords[0],coords[1]),(coords[0]+L,coords[1]+h)], fill='black', width=1)
                draw.line([(coords[0],coords[1]),(coords[0]+L,coords[1]-h)], fill='black', width=1)

            elif direction == "right":
                draw.line([(coords[0],coords[1]),(coords[0]-L,coords[1]+h)], fill='black', width=1)
                draw.line([(coords[0],coords[1]),(coords[0]-L,coords[1]-h)], fill='black', width=1)

            elif direction == "down":
                draw.line([(coords[0],coords[1]),(coords[0]+L,coords[1]-h)], fill='black', width=1)
                draw.line([(coords[0],coords[1]),(coords[0]-L,coords[1]-h)], fill='black', width=1)

            elif direction == "top":
                draw.line([(coords[0],coords[1]),(coords[0]+L,coords[1]+h)], fill='black', width=1)
                draw.line([(coords[0],coords[1]),(coords[0]-L,coords[1]+h)], fill='black', width=1)
                
        if role == 'n':
            axis = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2

            start = combined_heights[position[1]]+height
            distance = combined_heights[position[1]+1] - start
            
            draw.line([(axis,start),(axis,start+distance)], fill='black', width=1)
            arrow([axis,start+2*distance/3],block_gap/3,"down")

        elif role == 'o':
            if_axis = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2

            start = combined_heights[position[1]]+height/2
            end = combined_heights[position[1]+1]

            even_axis = width_offset + combined_widths[2*position[0]] + branch_width[2*position[0]]/2
            odd_axis = width_offset + combined_widths[2*position[0]+1] + branch_width[2*position[0]+1]/2
            
            draw.line([(if_axis-width/2,start),(even_axis,start)], fill='black', width=1)
            arrow([(if_axis+even_axis)/2 - block_gap/3,start],block_gap/3,"left")
            
            draw.line([(if_axis+width/2,start),(odd_axis,start)], fill='black', width=1)
            arrow([(if_axis+odd_axis)/2 + block_gap/3,start],block_gap/3,"right")

            draw.line([(even_axis,start),(even_axis,end)], fill='black', width=1)
            arrow([even_axis,(start+end)/2 + block_gap/3],block_gap/3,"down")
            
            draw.line([(odd_axis,start),(odd_axis,end)], fill='black', width=1)
            arrow([odd_axis,(start+end)/2 + block_gap/3],block_gap/3,"down")

            draw.text(( (if_axis-width/2 +even_axis)/2 - 2*font_size,start-2*font_size), "yes", fill='black',font=font)
            draw.text(( (if_axis+width/2 +odd_axis)/2 - 2*font_size,start-2*font_size), "no", fill='black',font=font)

        elif role == 'c':
            axis = width_offset + combined_widths[position[0]] + branch_width[position[0]]/2

            start = combined_heights[position[1]]+height/2
            distance = combined_heights[position[1]+1] - start
            
            draw.line([(axis,start),(axis,start+distance)], fill='black', width=1)
            arrow([axis,start+2*distance/3],block_gap/3,"down")
            
            even_branch = [position[0]*2,0]
            odd_branch = [position[0]*2+1,0]
            
            for obj in reversed(chart_code):
                if obj['position'][0] == odd_branch[0] and odd_branch[1] == 0:
                    odd_branch[1] = obj['position'][1]
                elif obj['position'][0] == even_branch[0] and even_branch[1] == 0:
                    even_branch[1] = obj['position'][1]
                if even_branch[1] != 0 and odd_branch[1] != 0:
                    break

            even_axis = width_offset + combined_widths[2*position[0]] + branch_width[2*position[0]]/2
            odd_axis = width_offset + combined_widths[2*position[0]+1] + branch_width[2*position[0]+1]/2

            draw.line([(axis,start),(even_axis,start)], fill='black', width=1)
            arrow([(axis+even_axis)/2 - block_gap/3,start],block_gap/3,"right")
            
            draw.line([(axis,start),(odd_axis,start)], fill='black', width=1)
            arrow([(axis+odd_axis)/2 + block_gap/3,start],block_gap/3,"left")

            start = combined_heights[even_branch[1]+1]
            distance = combined_heights[position[1]]+height/2 - start

            draw.line([(even_axis,start),(even_axis,start+distance)], fill='black', width=1)

            start = combined_heights[odd_branch[1]+1]
            distance = combined_heights[position[1]]+height/2 - start
            
            draw.line([(odd_axis,start),(odd_axis,start+distance)], fill='black', width=1)
            
    font_path = font_data['path']
    font_size = font_data['size']
    font = ImageFont.truetype(font_path, font_size)

    scale_constant = int(font_size/2)
    block_gap = font_size * 3/2
     
    height_offset = 100
    width_offset = 100

    tree_struct = Restructure([i for i in range(1,max_branch+1)])

    combined_widths = {}

    for i in range(0,len(tree_struct)):
        branch = tree_struct[i]
        if i == 0:
            combined_widths[branch] = 0
        else:
            try:
                combined_widths[branch] = combined_widths[tree_struct[i-1]] + branch_width[tree_struct[i-1]]
            except:
                combined_widths[branch] = combined_widths[tree_struct[i-1]]

    combined_heights = {}

    for key in layer_height.keys():
        if key == 1:
            combined_heights[key] = height_offset
        else:
            combined_heights[key] = layer_height[key-1] + combined_heights[key-1] + block_gap

    #print(layer_height,combined_heights)

    img_width = int(combined_widths[list(combined_widths.keys())[-1]] + branch_width[list(branch_width.keys())[-1]] + width_offset*2)
    img_height = int(combined_heights[max_y] + layer_height[max_y] + height_offset)

    img = Image.new('RGB', (img_width, img_height), color = 'white')
    draw = ImageDraw.Draw(img)

    width = 0
    for i in range(0,len(chart_code)):
        block = chart_code[i]
        if block['type'] == 'IO':
            height = IO(block['content'],block['position'])
        elif block['type'] == 'Terminator':
            height = Terminator(block['content'],block['position'])
        elif block['type'] == 'Process':
            height = Process(block['content'],block['position'])
        elif block['type'] == 'Decision':
            height,width = Decision(block['content'],block['position'])
        elif block['type'] == 'Connector':
            #height = Process(block['content'],block['position'])
            height = draw.textsize("c",font=font)[1] + font_size
            
        Flowline(block['role'],block['position'],height,chart_code[0:i],width)
            
    del draw
    
    return img

def main():
    lines = read()

    font_data = {"path":r"C:/Windows/Fonts/Arial.ttf","size":20}
    
    chart_code,max_branch,max_y,layer_height,branch_width = translation(lines,font_data)
    
    #for line in chart_code:
        #print(str(line["position"])+ "  :  " + str(line["role"])+ "  :  " + line['content'])

    flowchart = drawer(chart_code,max_branch,max_y,layer_height,branch_width,font_data)

    flowchart.save('testing3.png')

if __name__ == '__main__':
    main()
