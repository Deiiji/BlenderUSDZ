import bpy
import os
import subprocess

from io_scene_usdz.file_data import *
from io_scene_usdz.scene_data import *

def export_usdz(context, filepath = '', materials = True, keepUSDA = False,
                bakeTextures = False, bakeAO = False, bakeSeparate = False,
                samples = 8, scale = 1.0, animated = False):
    filePath, fileName = os.path.split(filepath)
    fileName, fileType = fileName.split('.')

    usdaFile = filePath+'/'+fileName+'.usda'
    usdzFile = filePath+'/'+fileName+'.usdz'

    scene = Scene()
    scene.exportMaterials = materials
    scene.exportPath = filePath
    scene.bakeAO = bakeAO
    scene.bakeSeparate = bakeSeparate
    scene.bakeSamples = samples
    scene.scale = scale
    scene.animated = animated
    scene.loadContext(context)

    if bakeTextures:
        scene.bakeTextures()

    # Export images and write the text USDA file
    data = scene.exportFileData()
    data.writeUsda(usdaFile)

    # Run the USDZ Converter Tool
    args = ['xcrun', 'usdz_converter', usdaFile, usdzFile]
    args += ['-v']
    subprocess.run(args)

    scene.cleanup()
    return {'FINISHED'}
