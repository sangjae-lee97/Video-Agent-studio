"""Composite the approved chart into the three F09 camera setups and reprint the consultation sheet from the original take."""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from scipy import ndimage

from render_opening import HERE, FFMPEG, font

SOURCE = HERE / 'media/flow/F09-874d16d5-1080p.mp4'
OUTPUT = HERE / 'renders/F09-consultation-original-reprint-1080p.mp4'
CHART = Image.open(HERE / 'renders/F09-start-85.708.png').convert('RGB')
# Inner display edges, measured on a 480-wide proxy during the first pullback.
PULLBACK = np.array([
    (0,0,0,480,270), (19,0,0,480,270), (23,-4,0,484,298),
    (27,-6,6,475,294),(30,4,10,464,287),(34,20,18,450,277),
    (38,36,25,435,269),(42,51,32,420,258),(46,64,38,408,250),
    (50,74,43,398,242),(54,84,47,388,234)
])

def screen(im, plate, corners, blur):
    # Fit the real display plane, including perspective, with a feather at its bezel.
    dest = np.array(corners, dtype=float) * 4
    low = np.maximum(0,np.floor(dest.min(axis=0)-3)).astype(int)
    high = np.minimum(im.size,np.ceil(dest.max(axis=0)+3)).astype(int)
    local = dest-low
    size = tuple(high-low)
    # Downsample before projection so the small monitor behaves like a photographed display.
    pw = min(1920, max(32, round(np.linalg.norm(dest[1]-dest[0]))))
    art = plate.resize((pw,round(pw*9/16)),Image.Resampling.LANCZOS)
    w,h=art.size
    matrix=[]; rhs=[]
    for (x,y),(u,v) in zip(local,[(0,0),(w,0),(w,h),(0,h)]):
        matrix.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]])
        rhs.extend([u,v])
    coeff=np.linalg.solve(matrix,rhs)
    tile=art.transform(size, Image.Transform.PERSPECTIVE, coeff, Image.Resampling.BICUBIC,fillcolor=(27,31,34))
    mask=Image.new('L',size)
    ImageDraw.Draw(mask).polygon([tuple(pt) for pt in local],fill=255)
    if blur:
        tile=tile.filter(ImageFilter.GaussianBlur(blur))
        mask=mask.filter(ImageFilter.GaussianBlur(blur))
    im.paste(tile,tuple(low),mask)

def print_sheet(im):
    # Reprint the complete two-column body from a clean camera sample of this
    # sheet. Only the source illumination and foreground hand enter the print.
    src=np.asarray(im)
    top=src[457:527, :, 1].astype(float)
    def edge_at(x):
        profile=top[:,x-10:x+11].mean(axis=1)
        return 458+np.argmax(np.diff(profile))
    left,right=edge_at(597),edge_at(1280)
    box=(538,468,1408,1080)
    ox,oy=box[:2]
    y,x=np.mgrid[box[1]:box[3],box[0]:box[2]]
    edge=left+(right-left)*(x-597)/683
    # Coordinates on the paper, following its tilt and widening towards camera.
    v=(y-edge)/583
    u=(x-(539+23*v))/(775+44*v)
    inside=np.minimum.reduce([u*775,(1-u)*775,v*583,(1-v)*583])
    cut=np.clip((inside-9)/29,0,1)
    # The source headings and both outer margins are intact in the original.
    # Meet the original printing within unprinted paper at either end.
    cut*=np.clip((y-edge-176)/20,0,1)*np.clip((edge+530-y)/21,0,1)

    rgb=src[oy:box[3],ox:box[2]].astype(np.float32)
    # Record the clean margin above the headings, including its natural grain.
    sx=(579+np.clip(u,0,1)*710).astype(int)
    sy=(left+(right-left)*(sx-597)/683+18+
        (1-np.abs((y%56)/28-1))*22).astype(int)
    stock=src[sy,sx].astype(np.float32)
    # A coarse light field transfers only the soft cast shadow. The source
    # printing is too small to enter this grid, and never supplies paper texture.
    small=np.asarray(Image.fromarray(np.uint8(rgb)).resize((98,48),Image.Resampling.BOX))
    light=ndimage.percentile_filter(small[:,:,1],82,size=(5,5))
    light=ndimage.gaussian_filter(light.astype(float),1.6)
    tone=np.clip((light+1)/201,0.25,1)
    # Sample shadow only near the clinician's moving hand. Outside that area
    # the clean stock itself supplies the full surface, including its grain.
    chroma=small[:,:,0].astype(float)-small[:,:,1]
    hand=(chroma>16) & (np.arange(small.shape[1])[None,:]>37)
    shadow=ndimage.maximum_filter(hand.astype(float),size=(15,11))
    shadow=ndimage.shift(shadow,(4,0),order=1,mode='nearest')
    shadow=ndimage.gaussian_filter(shadow,2.3)
    tone=1+(tone-1)*shadow
    gain=np.asarray(Image.fromarray(tone.astype(np.float32)).resize(
        (box[2]-ox,box[3]-oy),Image.Resampling.BICUBIC))
    # Fit the unprinted margins of the actual page (not its printed rows).
    # This recovers the broad lighting gradient down to the bottom edge.
    us,vs=u[::8,::8],v[::8,::8]
    margin=(((us>.026)&(us<.065))|((us>.947)&(us<.97))|
            ((vs>.903)&(vs<.927))|((vs>.305)&(vs<.326)))
    margin&=(us>.025)&(us<.97)&(vs>.3)&(vs<.93)
    obs=rgb[::8,::8]
    margin&=(obs[:,:,1]>175)&(abs(obs[:,:,0]-obs[:,:,1])<12)
    pu,pv=us[margin],vs[margin]
    design=np.column_stack([np.ones_like(pu),pu,pv,pu*pv,pu**2,pv**2])
    colors=obs[margin]
    coef=np.linalg.lstsq(design,colors,rcond=None)[0]
    good=np.abs(colors-design@coef).max(axis=1)<7
    if good.sum()>20:
        coef=np.linalg.lstsq(design[good],colors[good],rcond=None)[0]
    shade=(coef[0]+u[:,:,None]*coef[1]+v[:,:,None]*coef[2]
           +(u*v)[:,:,None]*coef[3]+(u*u)[:,:,None]*coef[4]+(v*v)[:,:,None]*coef[5])
    grain=stock-ndimage.gaussian_filter(stock,(4,4,0))
    material=(shade+grain)*gain[:,:,None]
    # All rules and type are printed together, in the coordinate space of the page.
    tx=np.clip(u*(PRINT.width-1),0,PRINT.width-1)
    ty=np.clip(v*(PRINT.height-1),0,PRINT.height-1)
    ink=ndimage.map_coordinates(PRINT_ARRAY,[ty,tx],order=1,mode='nearest')/255
    material*=1-.79*ink[:,:,None]
    # Chroma separates the warm fingers from paper. Preserve the blue shirt
    # at lower left, whose edge crosses the page during the consultation.
    redness=rgb[:,:,0]-rgb[:,:,1]
    fingers=np.clip((redness-13)/9,0,1)
    fingers=ndimage.gaussian_filter(ndimage.median_filter(fingers,size=3),1.1)
    shirt=np.clip((rgb[:,:,2]-rgb[:,:,0]-7)/8,0,1)*(x<670)
    opacity=cut*(1-np.maximum(fingers,shirt))
    # At a motion-blurred fingertip the original print can bleed into skin.
    # Use nearby foreground colour just along the soft matte transition.
    edge_pixels=(fingers>.04)&(fingers<.96)&(cut>.9)&(x>820)
    if edge_pixels.any():
        iy,ix=ndimage.distance_transform_edt(fingers<.97,return_distances=False,return_indices=True)
        ey,ex=np.nonzero(edge_pixels)
        rgb[ey,ex]=rgb[iy[ey,ex],ix[ey,ex]]
    region=rgb+(material-rgb)*opacity[:,:,None]
    im.paste(Image.fromarray(np.uint8(np.clip(region,0,255))),box)


PRINT=Image.new('L',(790,583))
pen=ImageDraw.Draw(PRINT)
pen.line((51,217,739,217),fill=116,width=2)
pen.line((395,180,395,518),fill=45,width=2)

for center,words in [(218,'1년간 PFA 우세'),(568,'257명 중 뇌졸중 6명')]:
    pen.text((center,361),words,font=font(35,'bold'),anchor='mm',fill=236)
PRINT_ARRAY=np.asarray(PRINT.filter(ImageFilter.GaussianBlur(.9)),dtype=np.float32)


def corrected(im,n):
    if n < 55:
        l,t,r,b=[np.interp(n,PULLBACK[:,0],col) for col in PULLBACK[:,1:].T]
        # The generated display changes aspect during the reveal. Extend its lower
        # margin instead of stretching the graph as the bezel enters the frame.
        h=(r-l)*9/16
        if t+h<b:
            margin=CHART.crop((0,1077,1920,1080)).resize((1920,max(1,round((b-t-h)*1080/h))))
            art=Image.new('RGB',(1920,1080+margin.height))
            art.paste(CHART); art.paste(margin,(0,1080))
        else:
            art=CHART
        screen(im,art,[(l,t),(r,t),(r,b),(l,b)],0 if n<20 else .6)
    elif n<111:
        screen(im,ROOM_CHART,[(148.3,79.5),(315,84.1),(317,194.2),(149.2,198.9)],.85)
    else:
        # The top half of this monitor is above the camera crop.
        screen(im,ROOM_CHART,[(203,-38),(471,-41),(469.3,78.3),(205.5,82)],2.1)
        print_sheet(im)
    return im

ROOM_CHART = ImageEnhance.Contrast(CHART).enhance(.91)

def render():
    cmd=[FFMPEG,'-loglevel','error','-y']
    temp=OUTPUT.with_suffix('.part.mp4')
    with subprocess.Popen(cmd+['-i',str(SOURCE),'-an','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE) as dec, subprocess.Popen(cmd+[
            '-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-vf','scale=out_color_matrix=bt709,format=yuv420p',
            '-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-c:v','libx264','-threads','5','-crf','13','-preset','veryfast',str(temp)],stdin=subprocess.PIPE) as enc:
        with enc.stdin:
            count=0
            while raw:=dec.stdout.read(1920*1080*3):
                im=Image.frombytes('RGB',(1920,1080),raw)
                enc.stdin.write(corrected(im,count).tobytes())
                count+=1
        if dec.wait() or enc.wait() or count!=190:
            raise ValueError(f'F09 encode failed ({count} frames)')
    temp.replace(OUTPUT)

if __name__=='__main__':
    render()
