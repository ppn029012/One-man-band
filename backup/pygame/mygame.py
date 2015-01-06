import pygame
import numpy as np
from numpy import mean,cov,double,cumsum,dot,linalg,array,rank
import alsaaudio, time, audioop

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
        
        if xvar > 0.1:
                x_pre = x[2:len(shapeobj)-1, :]
                x_hou = x[1:len(shapeobj)-2, :]
                x_diff = x_pre-x_hou
                x_diff = x_diff*x_diff
                x_diff = x_diff[:, 0] + x_diff[:, 1]
                print 'max:'
                print x_diff.max()
                
                if x_diff.max() < 500:
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

#music related
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)
maxval = 0



screen.fill((255, 255, 255))

while running:

	# MUSIC related
	l,data = inp.read()
	if l:
		maxval = audioop.max(data, 2)
		nocross = audioop.cross(data, 2)
		print nocross	
    	
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
        elif event.type == pygame.MOUSEMOTION:
                nextx, nexty = event.pos


        if event.type == pygame.MOUSEBUTTONDOWN:
                isdrawing = 1
                tmp_obj = []

        elif event.type == pygame.MOUSEBUTTONUP:
                isdrawing = 0             
                objnum = 4
                
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
                                
                                if lastcross == -1:
                                        lastcross = guitar_str
                                        print "crossing: string:" + str(guitar_str)
                                if guitar_str != lastcross:
                                        lastcross = guitar_str
                                        print "crossing: string:" + str(guitar_str)
                                        
                                break
                        else:
                                lastcross = -1
                        guitar_str = guitar_str + 1
                
        orgx = nextx
        orgy = nexty
	pygame.display.flip()
	time.sleep(.001)
        











