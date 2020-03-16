import random
import math
from PIL import Image, ImageDraw

'''
made by HEO
'''
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


##Represent Bounding Box
class Box:
    def __init__(self, cl, center_x, center_y, width, height):
        self.cl =cl
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        ## parameter is written as ratio
        ## conversion to Pixel
        self.cv_center_x = center_x * 640
        self.cv_center_y = center_y * 480
        self.cv_width = width * 640
        self.cv_height = height * 640

    ##return starting point of bounding box
    def first_point(self):
        fp = Point(self.center_x - self.width/2, self.center_y - self.height/2)

        return fp

    def last_point(self):
        fp = Point(self.center_x + self.width/2, self.center_y + self.height/2)

        return fp

    def textfile_string(self):
        text = str(self.cl) + " " + str(self.center_x) + " " + str(self.center_y) + " " + str(self.width) + " " + str(self.height) + "\n"
        return text
'''
made by HEO
'''


class Merger():
    def __init__(self, merge_image_set, merge_text_set):
        self.merge_set_num = [] ## number of merged image in list
        self.merge_set_box = [] ## box of merged image
        self.merge_number = 0 ## the number of merged item
        self.layer = [] ## the number of item per layer(max layer number = 3)
        
        ## Merge parameter
        self.v_overlap = 0
        self.h_overlap = 0
        self.param_info = (0, 0, 0) ## (v_overlap, h_overlap, merge_number)

        self._merge_image_set = merge_image_set
        self._merge_text_set = merge_text_set
        
        ## norm_size of the class {'key' : (width, height)}
        self.norm_size = {}


    ## set the parameter    
    def do_param_set(self):
        self.merge_number = random.randint(3,9)
        self.v_overlap = float(random.randint(1, 5)/10) ##(0.1~0.9)
        self.h_overlap = float(random.randint(1, 5)/10) ##(0.1~0.9)
        self.param_info = (self.v_overlap, self.h_overlap, self.merge_number)

        ## decide merge_set_num
        newnum = random.randrange(len(self._merge_image_set))
        for i in range(self.merge_number):
            while newnum in self.merge_set_num:
                newnum = random.randrange(len(self._merge_image_set))
            self.merge_set_num.append(newnum)

        ## set the layer
        div1 = random.randint(1, self.merge_number - 2)
        div2 = random.randint(1, self.merge_number - div1)
        self.layer.append(div1)
        self.layer.append(div2)
        self.layer.append(self.merge_number - div1 - div2)

        ## save norm_size information
        norm_list_file = open("/home/wonjae/Desktop/GP/project/Mergetest/image/norm_size.txt", 'r')
        norm_read = norm_list_file.readline()
        while not(norm_read == ""):
            norm_line = norm_read.split()
            self.norm_size[int(norm_line[1])] = (float(norm_line[2]), float(norm_line[3]))
            norm_read = norm_list_file.readline()

    def param_reset(self):
        self.merge_set_num = [] ## number of merged image in list
        self.merge_set_box = [] ## box of merged image
        self.merge_number = 0 ## the number of merged item
        self.layer = [] ## the number of item per layer(max layer number = 3)
        
        ## Merge parameter
        self.v_overlap = 0
        self.h_overlap = 0
        self.param_info = (0, 0, 0) ## (v_overlap, h_overlap, merge_number)
        
        self.norm_size = {}

    def image_resize(self, foreground, fg_box):
        '''
        Resize the image by the norm_size of the class.
        '''
        target_size = self.norm_size[fg_box.cl]
##        target_size *= randomrate(0.9~1.1)
        width_resize_rate = target_size[0]/fg_box.width
        height_resize_rate = target_size[1]/fg_box.height

        foreground = foreground.resize((int(640*width_resize_rate),int(480*height_resize_rate)))
        fg_box.width *= width_resize_rate
        fg_box.height *= height_resize_rate
        fg_box.center_x *= width_resize_rate
        fg_box.center_y *= height_resize_rate
        
        return foreground, fg_box

    '''
    made by HEO
    '''
    def find_point(self, index):
        ##finding line_num and line_index(e.g. layer[line_num] line_order-th bounding box
        ##line_index = 0 1 2...  (line_num = 0)
        ##             0 1 2...  (line_num = 1)
        ##             0 1 2...  (line_num = 2)
        ##index-th image (e.g. index-th image is layer[line_num] line_order-th)

        index_1line = self.layer[0] ## index of layer[1] 0th image

        if index < self.layer[0]:
            line_num = 0
            line_index = index
        elif index < self.layer[0]+self.layer[1]:
            line_num = 1
            line_index = index - self.layer[0]
        else:
            line_num = 2
            line_index = index - self.layer[0] - self.layer[1]

        ##Finding Point
        if line_index == 0:
            if line_num == 0:
                return Point(0,0)
            elif line_num == 1:
                ## wonjae fix if layer[0] == 0  Need to be fixed 
                if self.merge_set_box == []:
                    return Point(0,0)
                return Point(self.merge_set_box[0].last_point().x-self.v_overlap*self.merge_set_box[0].width,
                             self.merge_set_box[0].last_point().y-self.h_overlap*self.merge_set_box[0].height)
            else:
                ## wonjae fix if layer[0] == 0 and layer[1] == 0
                if self.merge_set_box == []:
                    self.h_overlap = 0
                    return Point(0,0)
                return Point(self.merge_set_box[index_1line].last_point().x - self.v_overlap * self.merge_set_box[index_1line].width,
                             self.merge_set_box[index_1line].last_point().y - self.h_overlap * self.merge_set_box[index_1line].height)
        else:
            return Point(self.merge_set_box[index-1].last_point().x - self.v_overlap * self.merge_set_box[index-1].width, self.merge_set_box[index-1].first_point().y)
    
    '''
    made by HEO
    '''


    ## merge two image
    def do_merge(self, background, foreground, fg_box, int_target_point):
        paste_point = (int((-1*fg_box.first_point().x)*640) + int_target_point.x , int((-1*fg_box.first_point().y)*480) + int_target_point.y) 
        background.paste(foreground, paste_point, foreground)
        return background

## 합친 이미지가 파일 전체 길이보다 길어질 때 고려해야함!! ##
    def real_merge(self, num):
        '''
        Create a randomly merged image file. Parameter 'num' is index of image file to be created. It will be on filename
        '''
        
        ## NEED TO CHANGE HERE!!!!!!!!!!!!!!!!!!!!##########################
        input_file_path = "/home/wonjae/Desktop/GP/project/Mergetest/image/"
        output_file_path = "/home/wonjae/Desktop/GP/project/Mergetest/merge_test_out/"
        ## NEED TO CHANGE HERE!!!!!!!!!!!!!!!!!!!!##########################
       
        for run in range(num):
            ## parameter setting
            self.do_param_set()
            out_filename = "merged_0" + str(run) + "_num:" + str(self.merge_number) + "_V:" + str(self.v_overlap) + "_H:" + str(self.h_overlap)
            
            ## background image (black)
            background = Image.new("RGBA", (640, 480), (0, 0, 0))
            
            ## for Debug
            ## print(self._merge_image_set)

            for idx in self.merge_set_num:
                input_image = Image.open(self._merge_image_set[idx]).convert("RGBA") ## open foreground image
##                print(self._merge_image_set[0])
                input_text = open(self._merge_text_set[idx]) ## open foreground image text file
                
                ## read text file
                fg_readline = input_text.readline()
                fg_info = fg_readline.split()

                ## make foreground box
                fg_box = Box(int(fg_info[0]), float(fg_info[1]), float(fg_info[2]), float(fg_info[3]), float(fg_info[4])) 
                input_image, fg_box = self.image_resize(input_image, fg_box)

                ## number of merged image before
                num_done_image = len(self.merge_set_box)
                
                ## merge image file
                target_point = self.find_point(num_done_image)
                int_target_point = Point(int(target_point.x*640), int(target_point.y*480))
                self.do_merge(background, input_image, fg_box, int_target_point)
                
                ## Append fixed foreground box info
                fixed_fg_box = Box(fg_box.cl, float(int_target_point.x)/640 + fg_box.width/2, float(int_target_point.y)/480 + fg_box.height/2, fg_box.width, fg_box.height)
                self.merge_set_box.append(fixed_fg_box)
                
                ## Draw Bounding Box
                background1 = ImageDraw.Draw(background)
                background1.rectangle([fixed_fg_box.first_point().x*640, fixed_fg_box.first_point().y*480, fixed_fg_box.last_point().x*640, fixed_fg_box.last_point().y*480], outline = "green")
                
                ## close image and text file
                input_image.close()
                input_text.close()
                
            
            ## save image file
            background.save(output_file_path + out_filename + ".png", format = "png")
            background = background.transpose(Image.FLIP_LEFT_RIGHT)
            background.save(output_file_path + out_filename + "_flip.png")

            ## save txt file 
            out_file = open(output_file_path + out_filename + ".txt" , 'w')
            for i in range(len(self.merge_set_box)):
                out_file.write(self.merge_set_box[i].textfile_string())
            out_file.close()
            
            ## reset merge_set_box for next merge
            self.param_reset()
            background.close()






##test


### Need to change here!!!!!!!!!!!!!#########################################
input_file_path = "/home/wonjae/Desktop/GP/project/Mergetest/image/"
### Need to change here!!!!!!!!!!!!!#########################################



image_list = []
text_list = []
image_file = open(input_file_path + 'target.txt', 'r')
text_file = open(input_file_path + 'target2.txt', 'r')
while True:
    line = image_file.readline()
    if line == "":
        break
    image_list.append(line[:-1]) ## read except '\n'
while True:
    line2 = text_file.readline()
    if line2 == "":
        break
    text_list.append(line2[:-1]) ## read exceipt '\n'
image_file.close()
text_file.close()

test = Merger(image_list, text_list)
test.real_merge(10)
