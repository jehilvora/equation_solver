import cv2
import numpy as np
import pytesseract
from keras.models import model_from_json
import tensorflow as tf

json_file = open('/Users/i506655/Projects/EquationSolver/Handwritten-Equation-Solver/model_final.json', 'r')
loaded_model_json = json_file.read()
print("model read")
json_file.close()
loaded_model = model_from_json(loaded_model_json)
print("model loaded")
# load weights into new model
loaded_model.load_weights("/Users/i506655/Projects/EquationSolver/Handwritten-Equation-Solver/model_final.h5") 
global graph
graph = tf.get_default_graph()

def convertImageToText(imagePath):
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    #kernel = np.ones((3,3),np.uint8)
    # cv2.imshow("wo",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #erosion = cv2.erode(img,kernel,iterations = 3)
    #dilation = cv2.dilate(img,kernel,iterations = 1)
    #img=dilation
    if img is not None:
        #images.append(img)
        img=~img
        ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        ctrs,ret=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w=int(28)
        h=int(28)
        train_data=[]
        #print(len(cnt))
        rects=[]
        for c in cnt :
            x,y,w,h= cv2.boundingRect(c)
            rect=[x,y,w,h]
            rects.append(rect)
        #print(rects)
        bool_rect=[]
        for r in rects:
            l=[]
            for rec in rects:
                flag=0
                if rec!=r:
                    if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
                        flag=1
                    l.append(flag)
                if rec==r:
                    l.append(0)
            bool_rect.append(l)
        #print(bool_rect)
        dump_rect=[]
        for i in range(0,len(cnt)):
            for j in range(0,len(cnt)):
                if bool_rect[i][j]==1:
                    area1=rects[i][2]*rects[i][3]
                    area2=rects[j][2]*rects[j][3]
                    if(area1==min(area1,area2)):
                        dump_rect.append(rects[i])
        #print(len(dump_rect)) 
        final_rect=[i for i in rects if i not in dump_rect]
        #print(final_rect)
        for r in final_rect:
            x=r[0]
            y=r[1]
            w=r[2]
            h=r[3]
            im_crop =thresh[y:y+h+10,x:x+w+10]
            

            im_resize = cv2.resize(im_crop,(28,28))
            # cv2.imshow("work",im_resize)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            im_resize=np.reshape(im_resize,(1,28,28))
            train_data.append(im_resize)

    s=''
    for i in range(len(train_data)):
        train_data[i]=np.array(train_data[i])
        train_data[i]=train_data[i].reshape(1,1,28,28)
        result=""
        with graph.as_default():
            result=loaded_model.predict_classes(train_data[i])
        if(result[0]==10):
            s=s+'-'
        if(result[0]==11):
            s=s+'+'
        if(result[0]==12):
            s=s+'*'
        if(result[0]==0):
            s=s+'0'
        if(result[0]==1):
            s=s+'1'
        if(result[0]==2):
            s=s+'2'
        if(result[0]==3):
            s=s+'3'
        if(result[0]==4):
            s=s+'4'
        if(result[0]==5):
            s=s+'5'
        if(result[0]==6):
            s=s+'6'
        if(result[0]==7):
            s=s+'7'
        if(result[0]==8):
            s=s+'8'
        if(result[0]==9):
            s=s+'9'
    return s