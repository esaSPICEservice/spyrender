import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt
import spiceypy as cspice
import json


'''
   developed and maintained by the
    __   __   __      __   __     __   ___     __   ___  __          __   ___
   /__\ /__` '__\    /__` |__) | /  ` |__     /__` |__  |__) \  / | /  ` |__
   \__, .__/ \__/    .__/ |    | \__, |___    .__/ |___ |  \  \/  | \__, |___

   If you have any questions regarding this file contact the
   ESA SPICE Service (ESS) at ESAC:

           Alfredo Escalante Lopez
           (+34) 91-8131-429
           alfredo.escalante.lopez@ext.esa.int
   
'''

def generateImage(yfov, ar, pxlines, pxsamples, cambody, targets, rsun, lightfactor=10, imname='sim_image.png', plot=True, save=False):

   #
   # load targets models
   #
   scene = pyrender.Scene(bg_color=0)
   for target in targets:
      target.nm = pyrender.Node(mesh=target.mesh,
                                translation=[target.r[0], target.r[1], target.r[2]],
                                rotation=[-target.q[1], -target.q[2], -target.q[3], target.q[0]])
      scene.add_node(target.nm)

   #
   # camera position
   #
   camera = pyrender.PerspectiveCamera(yfov=np.deg2rad(float(yfov)), aspectRatio=ar)
   nc = pyrender.Node(camera=camera,
                      translation=[0, 0, 0],
                      rotation=[-cambody.q[1], -cambody.q[2], -cambody.q[3], cambody.q[0]])
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
   r = cspice.spkpos(target, et, observerframe, 'LT+S', observer)[0]
   M = cspice.pxform(observerframe, targetframe, et)
   q = cspice.m2q(M)
   return r, q

def spiceSun(utc, observer, observerframe, illumsource):
   et = cspice.utc2et(utc)
   rsun = cspice.spkpos(illumsource, et, observerframe, 'LT+S', observer)[0]
   rsun = rsun/np.linalg.norm(rsun)
   return rsun

def main(config):
   with open(config, 'r') as f:
      config = json.load(f)

   class Camera:
      def __init__(self, body, frame):
         self.body = body
         self.frame = frame

   class Target:
      def __init__(self, mesh, name, frame):
         self.name = name
         self.frame = frame
         self.mesh = mesh

   #
   # get targets name, frame and obj file from config
   #
   targets = []
   names = [f for f in config["targetsname"]]
   frames = [f for f in config["targetsframe"]]
   objs = [f for f in config["targetsobj"]]
   if config["targetsobj"]:
      for i in range(0, len(objs), 1):
         fuze_trimesh = trimesh.load(objs[i])
         target = Target(pyrender.Mesh.from_trimesh(fuze_trimesh, smooth=config['smooth']),
                         names[i],
                         frames[i])
         targets.append(target)

   mk = config['metakernel']
   path = config['output']
   cspice.furnsh(mk)

   #
   # create time series
   #
   utc0 = config['utc0']
   et0 = cspice.utc2et(utc0)
   utcf = config['utcf']
   etf = cspice.utc2et(utcf)
   et = np.linspace(et0, etf, int(config['tsamples']))

   #
   # compute camera id and parameters from kernel pool
   #
   camera_name = config['camera']
   camera_id = cspice.bodn2c(camera_name)
   (shape, frame, bsight, vectors, bounds) = cspice.getfov(camera_id, 100)

   camera_frame = config['camera_frame']
   if not camera_frame:
      if frame:
         camera_frame = frame
      else:
         print("CAMERA FRAME not defined for "
               "{}".format(config['camera']))

   pixel_lines = config['pxlines']
   pixel_samples = config['pxsamples']
   if not pixel_lines or not pixel_samples:
      try:
         pixel_lines = int(cspice.gdpool('INS' + str(camera_id) + '_PIXEL_LINES', 0, 1))
         pixel_samples = int(cspice.gdpool('INS' + str(camera_id) + '_PIXEL_SAMPLES', 0, 1))
      except:
         pass
         print("PIXEL_SAMPLES and/or PIXEL_LINES not defined for "
               "{}".format(config['camera']))
         return

   yfov = config['yfov']
   ar = config['aspectratio']
   if not yfov or not ar:
      try:
         ref_angle = int(cspice.gdpool('INS' + str(camera_id) + '_FOV_REF_ANGLE', 0, 1))
         cross_angle = int(cspice.gdpool('INS' + str(camera_id) + '_FOV_CROSS_ANGLE', 0, 1))
         yfov = 2 * ref_angle
         ar = cross_angle / ref_angle
      except:
         pass
         print("Field of View aperture angles not defined for "
               "{}".format(config['camera']))
         return

   camera = Camera(config['observer'], camera_frame)

   n = 0
   for eti in et:
      n = n + 1
      index = int(n + 1e7)
      utc = cspice.et2utc(eti, 'ISOC', 2)
      print(utc)

      #
      # compute position and attitude for each target
      #
      for target in targets:
         r, q = spiceGeometry(utc=utc,
                                 observer=camera.body, observerframe=camera.frame,
                                 target=target.name, targetframe=target.frame,
                                 illumsource=config['illumsource'])
         target.r = r
         target.q = q

      #
      # flip camera boresight (-Z axis for rendering)
      #
      camera.q = cspice.m2q(cspice.eul2m(np.pi, 0, 0, 1, 2, 3))

      #
      # compute Sun vector defining directional light
      #
      rsun = spiceSun(utc=utc, observer=camera.body, observerframe=camera_frame, illumsource='SUN')

      #
      # generate image
      #
      imname = path + camera.body + '_' + utc + '.PNG'
      generateImage(yfov=yfov, ar=ar,
                    pxlines=pixel_lines, pxsamples=pixel_samples,
                    cambody=camera, targets=targets, rsun=rsun,
                    lightfactor=config['lightfactor'],
                    plot=(config['plot']), save=config['save'], imname=imname)

   return
main(config='config/config.json')
