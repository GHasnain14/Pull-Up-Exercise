import cv2
from matplotlib import image
import mediapipe as mp
import numpy as np
import PoseModule as pm
from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import filedialog
count=0
root =Tk()
root.configure(bg="#000000")
root.state("zoomed")
# ---------------------------------------------------------------------------------------------------------------------------------
video_frame = Frame(root,height=580,width=720,bg="#000000")
video_labal = Label(root,height=580,width=720,bg="#000000")
video_frame.place(x=15,y=30)
video_labal.place(x=15,y=30)
video_path = 0
# ************************************************Path Select Function*****************************************************************
def path_select():
    global video_path,cap
    video_path = filedialog.askopenfilename()
    cap = cv2.VideoCapture(video_path)
    reset()
    text = Label(root,text="Recorded Video  ",bg="purple",fg="#ffffff",font=("Times New Roman",20))
    text.place(x=280,y=10)


# -----------------------------------Live Feed--------------------------------------------------------------------------
def video_live():
    global video_path,cap
    video_path = 0
    cap = cv2.VideoCapture(video_path)
    reset()
    text = Label(root,text="Live Video Feed",bg="purple",fg="#ffffff",font=("Times New Roman",20))
    text.place(x=280,y=10)
#---------------------------------------------Reset Function --------------------------------------------------------------------------
def reset():
    global count
    count=0


#---------------------------------------------Live Button --------------------------------------------------------------------------

live_btn_img = cv2.imread("live.png")
live_btn_img=cv2.resize(live_btn_img,(130,50))
live_btn_img = cv2.cvtColor(live_btn_img, cv2.COLOR_BGR2RGB)
live_btn_img = ImageTk.PhotoImage(Image.fromarray(live_btn_img), Image.ANTIALIAS)
live_btn = Button(root, height = 50, width=130, image=live_btn_img, fg="#DBDBDB", bg="purple", command=lambda:video_live())
live_btn.place(x=1200,y=20)

text = Label(root,text="  For Live Video",bg="purple",fg="#ffffff",font=("Times New Roman",20))
text.place(x=1000,y=30)
# --------------------------------------------Browse Button-----------------------------------------------------------------------------
browse_btn_img = cv2.imread("browse.png")
browse_btn_img=cv2.resize(browse_btn_img,(130,50))
browse_btn_img = cv2.cvtColor(browse_btn_img, cv2.COLOR_BGR2RGB)
browse_btn_img = ImageTk.PhotoImage(Image.fromarray(browse_btn_img), Image.ANTIALIAS)
browse_btn = Button(root, height = 50, width=130,image=browse_btn_img, fg="#3a3b3c", bg="purple", command=lambda:path_select())
browse_btn.place(x=1200,y=80)
text = Label(root,text="To Browse Video",bg="purple",fg="#ffffff",font=("Times New Roman",20))
text.place(x=1000,y=90)
#---------------------------------------------Count Label --------------------------------------------------------------------------
reset_ = Label(root,text='COUNT', fg="#DBDBDB", bg="purple",font=("Times New Roman",20))
reset_.place(x=1100,y=250)
#---------------------------------------------Reset Button --------------------------------------------------------------------------
reset_btn = Button(root, height = 2, width=4,text='Reset', fg="#DBDBDB", bg="purple",font=("Times New Roman",10), command=lambda:reset())
reset_btn.place(x=1200,y=350)
#---------------------------------------------Accuracy  Label --------------------------------------------------------------------------
Pull_down= Label(root,text='Down', fg="#DBDBDB", bg="purple",font=("Times New Roman",15))
Pull_down.place(x=850,y=550)
Pull_up= Label(root,text='Up', fg="#DBDBDB", bg="purple",font=("Times New Roman",15))
Pull_up.place(x=850,y=90)
#---------------------------------------------title page label --------------------------------------------------------------------------
Name_part= Label(root,text='2020-MC-42', fg="#DBDBDB", bg="black",font=("Times New Roman",15))
Name_part.place(x=1200,y=680)
Name_part_1= Label(root,text='2020-MC-57', fg="#DBDBDB", bg="black",font=("Times New Roman",15))
Name_part_1.place(x=1200,y=700)

#---------------------------------------------Pull up counter label --------------------------------------------------------------------------
text = Label(root,text="  Pull Up Counter ",bg="purple",fg="#ffffff",font=("Times New Roman",40))
text.place(x=150,y=640)

# ----------------------------------------------------------
browse_btn_img_logo = cv2.imread("Logo.png")
browse_btn_img_logo=cv2.resize(browse_btn_img_logo,(130,160))
browse_btn_img_logo = cv2.cvtColor(browse_btn_img_logo, cv2.COLOR_BGR2RGB)
browse_btn_img_logo = ImageTk.PhotoImage(Image.fromarray(browse_btn_img_logo), Image.ANTIALIAS)
browse_btn = Label(root,image=browse_btn_img_logo, fg="#3a3b3c", bg="#000000")
browse_btn.place(x=550,y=570)

browse_btn = Label(root,image=browse_btn_img_logo, fg="#3a3b3c", bg="#000000")
browse_btn.place(x=40,y=570)

#================================================================================================================================

cap = cv2.VideoCapture(video_path)
detector = pm.poseDetector()
direction = 0
count=0
form = 0
loop=0
#---------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------Main Loop --------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
while True:
    success, img = cap.read() #640 x 480
    if success:
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            elbow_left = detector.findAngle(img, 11, 13, 15)
            elbow_right = detector.findAngle(img, 12, 14, 16)
            
            #Percentage of success of pushup
            per = np.interp(elbow_left, (45, 160), (0, 100)) 
           
            if elbow_left > 160 and elbow_right >160:
                form = 1
            #Check for full range of motion for the pushup
            if form == 1: 
                if per ==100:
                    if elbow_left > 160 and elbow_right > 160:
                        ##up
                        if direction == 1:
                            count += 0.5
                            direction = 0
                if per == 0:
                    if elbow_left <= 45 and elbow_right <= 45:
                        ##down
                        if direction == 0:
                            count += 0.5
                            direction = 1
            
            if form == 1:
                pb = ttk.Progressbar(root,orient="vertical",mode="determinate",length=500)    
                pb["value"] = 100-per
                pb.place(x=800,y=80)
                # Counter button display
                counter=Label(root,text=f"{int(count)}",fg="#ffffff",bg="purple",font=("Times New Roman",35))
                counter.place(x=1200,y=250)

        cv2.resize(img,(720,580))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img),Image.ANTIALIAS)
        video_labal["image"]=img
        
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    root.update()