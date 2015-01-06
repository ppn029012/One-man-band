import pygame
import pygame as pg
import pygame.mixer as pm
import numpy as np
from numpy import mean,cov,double,cumsum,dot,linalg,array,rank
import alsaaudio, time, audioop, wave



def getrectrange(rectshape):
        x = np.array(rectshape)
        h_max = np.max(x[:, 0])
        h_min = np.min(x[:, 0])
        v_max = np.max(x[:, 1])
        v_min = np.min(x[:, 1])
        width = h_max - h_min
        height = v_max - v_min
        
        return [h_min, v_min, width, height]

    
def getobjtype(shapeobj):
        # shapeobj is a list: 
        # [[1,2],
        #  [2,2],
        #  [2,3]]
        x = np.array(shapeobj)
        first = x[1, :]
        last = x[len(shapeobj)-1, :]
        direction = last-first
        proj_dir = array([-direction[1],direction[0]])
        proj_dir = proj_dir/np.sqrt(direction[1]*direction[1] + direction[0]*direction[0])
        xproj = np.dot(x, proj_dir)
        xvar = np.var(xproj)/len(shapeobj)
        
        if xvar > 0.3:
                x_pre = x[2:len(shapeobj)-1, :]
                x_hou = x[1:len(shapeobj)-2, :]
                x_diff = x_pre-x_hou
                x_diff = x_diff*x_diff
                x_diff = x_diff[:, 0] + x_diff[:, 1]
                print 'max:'
                print x_diff.max()
                
                if x_diff.max() < 230:
                        return 0 # circle
                else:
                        return 2 # rect
        else:
                return 1        # 1 is line
        


def iscross(a1, b1, a2, b2, x1, y1, x2, y2):

        if x1==x2:
                l1 = (b1- b2)*x1/(a1-a2) + (a1*b2 - a2*b1)/(a1-a2) - y1
                l2 = (b1- b2)*x2/(a1-a2) + (a1*b2 - a2*b1)/(a1-a2) - y2
                if l1==0 and l2 == 0:
                        return True
                else:  
                        return False
        else:
               r1 = (y1- y2)*a1/(x1-x2) + (x1*y2 - x2*y1)/(x1-x2) - b1
               r2 = (y1- y2)*a2/(x1-x2) + (x1*y2 - x2*y1)/(x1-x2) - b2
        
               l1 = (b1- b2)*x1/(a1-a2) + (a1*b2 - a2*b1)/(a1-a2) - y1        
               l2 = (b1- b2)*x2/(a1-a2) + (a1*b2 - a2*b1)/(a1-a2) - y2
        
               if (r1*r2)<0 and (l1*l2)<0:
                       return True
               else:
                       return False



# screen = pygame.display.set_mode((600,400))
pygame.init()
screen = pygame.display.set_mode((1000,800))
running = 1
orgx = orgy = 0
nextx = nexty = 0
isdrawing = 0
isplaying = 0
lastcross = -1

#It is related to record the points
objs = []
tmp_obj = []
lines = []
rects = []

#=========================================
# PART:music related
#=========================================
b4 = pygame.mixer.Sound('b4.wav')
e3 = pygame.mixer.Sound('e3.wav')
c3 = pygame.mixer.Sound('c3.wav')
g3 = pygame.mixer.Sound('g3.wav')
c4 =  pygame.mixer.Sound('c4.wav')
ga3 = pygame.mixer.Sound('ga3.wav')
e4 =  pygame.mixer.Sound('e4.wav')
fg3 =  pygame.mixer.Sound('fg3.wav')
ab4 =  pygame.mixer.Sound('ab4.wav')
cd4 =  pygame.mixer.Sound('cd4.wav')
fg4 =  pygame.mixer.Sound('fg4.wav')
de4 =  pygame.mixer.Sound('de4.wav')
ga4 =  pygame.mixer.Sound('ga4.wav')
beat = pygame.mixer.Sound('beat.wav')
hihat = pygame.mixer.Sound('hihat.wav')
snare = pygame.mixer.Sound('snare.wav')

ga3b  = pygame.mixer.Sound('ga3b.wav')
fg3b  = pygame.mixer.Sound('fg3b.wav')
c3b   = pygame.mixer.Sound('c3b.wav')
e3b   = pygame.mixer.Sound('e3b.wav')

SHORT_NORMALIZE = (1.0/32768.0) 
INPUT_BLOCK_TIME = 0.05
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME


inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(1)
inp.setrate(22050)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(800)
maxval = 0

playlist = []
rythm = 0
rythm_threshold = 400

rythm_changer = 0
rythm_records = []

screen.fill((255, 255, 255))

while running:

	# MUSIC related
	l,data = inp.read()
        nocross = 0
        
        if len(rects) > 0:
                rythm_changer = rythm_changer + 1
                
                
	if l:
                maxval = audioop.max(data, 2)
                if maxval>30000:
                        nocross = audioop.cross(data, 2)
		
                
                print nocross
                playlist = []
                if nocross <=4:
                        playlist.append(c3)
                        playlist.append(e3)
                        playlist.append(g3)
                        playlist.append(c4)
                        playlist.append(c3b)
                elif nocross > 4 and nocross <8:
                        playlist.append(e3)
                        playlist.append(ga3)
                        playlist.append(b4)
                        playlist.append(e4)    
                        playlist.append(e3b)
                elif nocross >8 and nocross <12:
                        playlist.append(fg3)
                        playlist.append(ab4)
                        playlist.append(cd4)
                        playlist.append(fg4)
                        playlist.append(fg3b)
                elif nocross >8 and nocross <12:                     
                        playlist.append(ga3)
                        playlist.append(c4)
                        playlist.append(de4)
                        playlist.append(ga4)
                        playlist.append(ga3b)
                else:
                        playlist.append(ga3)
                        playlist.append(c4)
                        playlist.append(de4)
                        playlist.append(ga4)
                        playlist.append(ga3b)
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
        elif event.type == pygame.MOUSEMOTION:
                nextx, nexty = event.pos


        if event.type == pygame.MOUSEBUTTONDOWN:
                isdrawing = 1
                tmp_obj = []
                if isplaying:
                        if len(rects) != 0:
                                if nextx>rects[0][0] and nextx<rects[0][0]+rects[0][1] and nexty>rects[0][2] and nexty<rects[0][3]+rects[0][2]:
                                        if len(rythm_records) == 0:
                                                rythm_records.append(0)
                                                rythm_changer = 0
                                        else:
                                                rythm_records.append(rythm_changer)
                                        print rythm_records
                                        if len(rythm_records) == 5:
                                                rythm_diff = rythm_records[1:-1]
                                                rythm_diff = np.array(rythm_diff) - np.array(rythm_records[0:-2])
                                                rythm_threshold = int(np.mean(rythm_diff))

                                                rythm_records = []
                                                rythm_changer = 0
                                                
                                                print 'changing rythm :' + str(rythm_threshold)
                                        print 'clicking!!!!  ' + str(len(rythm_records))

        elif event.type == pygame.MOUSEBUTTONUP:
                isdrawing = 0             
                objnum = 6
                
                if len(objs)< objnum:
                        objs.append(tmp_obj)
                        print 'OBJ num: '+str(len(objs))
                        
                if isplaying==0:
                        # calculate the what the tmp_obj is: line, circle, rect
                        objtype = getobjtype(tmp_obj)

                        if objtype == 1:
                                lines.append([tmp_obj[0][0], tmp_obj[0][1],  tmp_obj[-1][0], tmp_obj[-1][1]]  )
                                print 'drawing a LINE : '
                        elif objtype == 0:
                                print 'drawing a circle'
                        elif objtype == 2:
                                print 'drawing a RECT'
                                rectx, recty, rectwid, rectheight = getrectrange(tmp_obj)
                                rects.append([rectx, recty, rectwid, rectheight])
                                pg.draw.rect(screen, (255,0,0), (rectx, recty, rectwid, rectheight), 1)
                if len(objs) == objnum:
                        isplaying = 1                 
        if orgx==0 and orgy==0:
                orgx = nextx
                orgy = nexty
                
                
        if isdrawing==1 and isplaying==0:
                tmp_obj.append([orgx,orgy])
                pygame.draw.line(screen, (0, 0, 255), (orgx, orgy), (nextx, nexty), 3)
        if isdrawing==1 and isplaying==1:
                guitar_str = 0
                for line in lines:
                        if iscross(line[0],line[1],line[2],line[3],orgx, orgy, nextx,nexty):
                                if guitar_str == 0:
                                        playlist[guitar_str].play()
                                        
                                elif guitar_str ==1:
                                        playlist[guitar_str].play()
                                elif guitar_str ==2:

                                        playlist[guitar_str].play()
                                elif guitar_str ==3:

                                        playlist[guitar_str].play()
                                if lastcross == -1:
                                        lastcross = guitar_str

                                if guitar_str != lastcross:
                                        lastcross = guitar_str

                                break
                        else:
                                lastcross = -1
                        guitar_str = guitar_str + 1
               
        if isplaying ==1:
                
                
                rythm = rythm + 1
                if rythm == int(rythm_threshold):
                        beat.play()
                        hihat.play()
                        
                        playlist[4].play()
                elif rythm >= int(rythm_threshold)*3:
                        snare.play()
                        rythm = 0
                        playlist[4].play()
        
        
                


        orgx = nextx
        orgy = nexty
	pygame.display.flip()
        time.sleep(0.001)
        











