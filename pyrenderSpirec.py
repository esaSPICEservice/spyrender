import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt
import spiceypy as cspice
import json
import PIL.Image


def generateImage(mesh, yfov, ar, pxlines, pxsamples, rcam, qcam, rsun, lightfactor=10, imname='sim_image.png', plot=True, save=False):

   #
   # load model target
   #
   nm = pyrender.Node(mesh=mesh)
   scene = pyrender.Scene(bg_color=0)
   scene.add_node(nm)

   #
   # camera position
   #
   camera = pyrender.PerspectiveCamera(yfov=yfov, aspectRatio=ar)
   nc = pyrender.Node(camera=camera,
                      translation=[rcam[0], rcam[1], rcam[2]],
                      rotation=[-qcam[1], -qcam[2], -qcam[3], qcam[0]])
   scene.add_node(nc)

   #
   # directional light
   #
   light = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=lightfactor)
   zsun = rsun/np.linalg.norm(rsun)
   xsun = np.array([0, 0, 1]) - np.dot(np.array([0, 0, 1]), zsun) * zsun
   xsun = xsun/np.linalg.norm(xsun)
   ysun = np.cross(zsun, xsun)
   Msun = np.array([[xsun[0], ysun[0], zsun[0]],
                    [xsun[1], ysun[1], zsun[1]],
                    [xsun[2], ysun[2], zsun[2]]])
   qsun = cspice.m2q(np.linalg.inv(Msun))
   nl = pyrender.Node(light=light, rotation=[-qsun[1], -qsun[2], -qsun[3], qsun[0]])
   scene.add_node(nl)

   #
   # render scene
   #
   # pyrender.Viewer(scene, shadows=True)
   flags = pyrender.RenderFlags.SHADOWS_DIRECTIONAL
   r = pyrender.OffscreenRenderer(pxlines, pxsamples)
   color, depth = r.render(scene, flags=flags)
   plt.figure()
   plt.axis('off')
   plt.imshow(color)
   if save:
      plt.imsave(imname, color)
   if plot == 'True':
      plt.show()
   plt.close()

   return

def spiceGeometry(utc, observer, observerframe, target, targetframe, illumsource):

   et = cspice.utc2et(utc)
   rcam = cspice.spkpos(observer, et, targetframe, 'LT+S', target)[0]
   M = cspice.pxform(targetframe, observerframe, et)
   Maux = cspice.eul2m(np.pi, 0, 0, 1, 2, 3)
   M = cspice.mxm(Maux, M)
   qcam = cspice.m2q(M)
   rsun = cspice.spkpos(illumsource, et, targetframe, 'LT+S', observer)[0]
   rsun = rsun/np.linalg.norm(rsun)

   return rcam, qcam, rsun

def main(config):
   with open(config, 'r') as f:
      config = json.load(f)

   fuze_trimesh = trimesh.load(config['targetobj'])
   if config['texture']:
      imagetext = PIL.Image.open(config['texture'])
      testtext = pyrender.Texture(source=imagetext, source_channels='RGB')
      testmat = pyrender.MetallicRoughnessMaterial(baseColorTexture=testtext)
      mesh = pyrender.Mesh.from_trimesh(fuze_trimesh, smooth=config['smooth'], material=testmat)
   else:
      mesh = pyrender.Mesh.from_trimesh(fuze_trimesh, smooth=config['smooth'])

   mk = config['metakernel']
   path = config['output']
   cspice.furnsh(mk)

   utc0 = config['utc0']
   et0 = cspice.utc2et(utc0)
   utcf = config['utcf']
   etf = cspice.utc2et(utcf)
   et = np.linspace(et0, etf, int(config['tsamples']))

   if config['labelfile'] == 'True':
      lblfile = open(path + "data.lbl", "a+")
      lblfile.write('# id, xsc[km], ysc[km], zsc[km], qxsc[-], qysc[-], qzsc[-], qwsc[-], rxsun[-], rysun[-], rzsun[-]\n')

   n = 0
   for eti in et:
      n = n + 1
      index = int(n + 1e7)
      utc = cspice.et2utc(eti, 'ISOC', 2)
      print(utc)
      rcam, qcam, rsun = spiceGeometry(utc=utc,
                                             observer=config['observer'], observerframe=config['observer_frame'],
                                             target=config['target'], targetframe=config['target_frame'],
                                             illumsource=config['illumsource'])
      imname = path + 'SIM_x' + str(index)[-6:] + '.PNG'
      generateImage(mesh=mesh, yfov=config['yfov'], ar=config['aspectratio'],
                    pxlines=config['pxlines'], pxsamples=config['pxsamples'],
                    rcam=rcam, qcam=qcam, rsun=rsun,
                    lightfactor=config['lightfactor'],
                    plot=(config['plot']), save=config['save'], imname=imname)
      if config['labelfile'] == 'True':
         rcam, qcam, rsun = spiceGeometry(utc=utc,
                                          observer=config['observer'], observerframe=config['observer_frame'],
                                          target=config['target'], targetframe=config['target_frame'],
                                          illumsource=config['illumsource'])
         lblfile.write(str(index)[-6:] + ', ' +
                       str(rcam[0]) + ', ' + str(rcam[1]) + ', ' + str(rcam[2]) + ', ' +
                       str(-qcam[1]) + ', ' + str(-qcam[2]) + ', ' + str(-qcam[3]) + ', ' +
                       str(qcam[0]) + ', ' + str(rsun[0]) + ', ' + str(rsun[1]) + ', ' + str(rsun[2]) + '\n')

   return
main(config='config.json')
