'''
Created on July 3, 2019

@author: Chris Granados - Xian
@contact: chris.granados@xiancg.com http://www.chrisgranados.com/
TODO: Implement attributes on default and arnold. This will require 
a lot of work to do it automatically, use config file preset for now.
'''
import os
import json
import pkgutil
import inspect
import maya.cmds as mc
from cgxLightingTools.scripts.toolbox import tools
import cgxLightingTools.scripts.core.namingConventions as naming
import cgxLightingTools.scripts.toolbox.post_functions as post_functions


class LightsFactory(object):
    def __init__(self):
        super(LightsFactory, self).__init__()
        self.lightNodeTypes = tools.getDefaultLightNodes()
        repoPath = os.path.join(os.path.dirname(os.path.abspath(naming.__file__)),'cfg')
        os.environ['NAMING_REPO'] = repoPath
        naming.loadSession()
        self.naming = naming
        lightAttrsPath = os.path.join(repoPath, 'lightAttrs.json')
        with open(lightAttrsPath) as fp:
            config = json.load(fp)
        self._lightAttrs = config
        self.post_fn = self._initPostFunctions()
    
    def createLight(self, lightNodeType, lightName, *args, **kwargs):
        if lightNodeType == 'spotLight':
            shapeNode = mc.spotLight(name=lightName)
        elif lightNodeType == 'directionalLight':
            shapeNode = mc.directionalLight(name=lightName)
        elif lightNodeType == 'pointLight':
            shapeNode = mc.pointLight(name=lightName)
        elif lightNodeType == 'ambientLight':
            shapeNode = mc.ambientLight(name=lightName)
        elif lightNodeType == 'volumeLight':
            initNode = mc.createNode('volumeLight')
            transform = mc.listRelatives(initNode, parent=True, fullPath=True)[0]
            result = mc.rename(transform, lightName)
            shapeNode = mc.listRelatives(result, shapes=True, 
                                        noIntermediate=True, type='light')[0]
        elif lightNodeType == 'areaLight':
            initNode = mc.createNode('areaLight')
            transform = mc.listRelatives(initNode, parent=True, fullPath=True)[0]
            result = mc.rename(transform, lightName)
            shapeNode = mc.listRelatives(result, shapes=True,
                                        noIntermediate=True, type='light')[0]
        else:
            return None
        if shapeNode:
            tools.setDefaultAttrs(shapeNode)
            transformNode = mc.listRelatives(shapeNode, parent=True)[0]
            try:
                self.post_fn.postLightCreation(transformNode, shapeNode, *args, **kwargs)
            except BaseException as e:
                tools.logger.warning("Post light creation function not executed due to exceptions.")
                raise
            finally:
                return transformNode, shapeNode
        else: 
            return None
    
    def duplicateLight(self, lightNode, withInputs=False, withNodes=False, *args, **kwargs):
        objTransform, objShape= tools.getTransformAndShape(lightNode)
        transformNode = str()
        shapeNode = str()
        if mc.nodeType(objShape) in tools.getLightNodesList():
            parsedName = self.parseOldNameByTokens(objTransform)
            if parsedName is not None:
                lightName = self.buildName(**parsedName)
                if withInputs and not withNodes:
                    transformNode = mc.duplicate(objTransform, name= lightName, ic= True)[0]
                elif withInputs and withNodes:
                    transformNode = mc.duplicate(objTransform, name= lightName, ic= True, un=True)[0]
                else:
                    transformNode = mc.duplicate(objTransform, name= lightName)[0]
            else:
                if withInputs and not withNodes:
                    transformNode = mc.duplicate(objTransform, ic= True)[0]
                elif withInputs and withNodes:
                    transformNode = mc.duplicate(objTransform, ic= True, un=True)[0]
                else:
                    transformNode = mc.duplicate(objTransform)[0]
            shapeNode = mc.listRelatives(transformNode, shapes=True, noIntermediate=True, fullPath=True)[0]
        else:
            tools.logger.info('Only lights accepted. {} is {}'.format(lightNode, mc.nodeType(lightNode)))
            return None
        
        self.post_fn.postLightDuplicate(transformNode, shapeNode, *args, **kwargs)

        return transformNode, shapeNode
    
    def renameLight(self, lightNode, lightName, *args, **kwargs):
        objTransform, objShape= tools.getTransformAndShape(lightNode)
        parsedName = self.naming.parse(lightName)
        finalLightName = self.buildName(**parsedName)
        result = mc.rename(objTransform, finalLightName)
        shapeNode = mc.listRelatives(result, shapes=True, noIntermediate=True, fullPath=True)[0]

        self.post_fn.postLightRename(result, shapeNode, *args, **kwargs)
        
        return result
    
    def deleteLight(self, lightNode, lightName, *args, **kwargs):
        objTransform, objShape= tools.getTransformAndShape(lightNode)
        success = False
        try:
            mc.delete(objTransform)
            success = True
        except:
            pass

        self.post_fn.postLightDelete(objTransform, objShape, *args, **kwargs)
        
        return success
    
    def parseOldNameByTokens(self, lightNode):
        objTransform, objShape= tools.getTransformAndShape(lightNode)
        nameSplit = objTransform.split('_')
        result = None
        if len(nameSplit) == len(self.naming.getActiveRule().fields):
            if mc.nodeType(objShape) in self.lightNodeTypes:
                result = self.naming.parse(objTransform)

        return result
    
    def buildName(self, *args, **kwargs):
        '''Recursive method to check if the light name
        is already in use and modify it accordingly if it is'''
        lightName = self.naming.solve(*args, **kwargs)
        if not mc.objExists(lightName):
			return lightName
        else:
            #Number might be passed as arg or kwarg
            argsList= list(args)
            for i, arg in enumerate(argsList):
                if isinstance(arg, int):
                    argsList[i] += 1
            args = tuple(argsList)
            for k, v in kwargs.iteritems():
                if isinstance(v, int):
                    kwargs[k] = v + 1

            lightName = self.buildName(*args, **kwargs)
            return lightName
    
    def _initPostFunctions(self):
        currentRenderer = tools.getCurrentRenderPlugin()
        renderers = tools.getRenderEngines()
        if renderers is not None:
            rendererNames = renderers.keys()
            postFuncPath = os.path.dirname(post_functions.__file__)
            postFuncs = [name for _, name, _ in pkgutil.iter_modules([postFuncPath]) if name.endswith('post_functions')]
            for postFunc in postFuncs:
                if postFunc.rsplit('_')[0] in rendererNames and postFunc.rsplit('_')[0] == currentRenderer:
                    for name, obj in inspect.getmembers(eval('post_functions.{}'.format(postFunc))):
                        if inspect.isclass(obj) and name == ('PostFunctions_{}'.format(currentRenderer)):
                            postFuncObj = eval('post_functions.{}.{}()'.format(postFunc, name))
                            return postFuncObj
            # Returns default post functions if no match for current renderer found
            postFuncObj = post_functions.default_post_functions.PostFunctions_default()
            return postFuncObj

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == '__main__' or 'eclipsePython' in __name__:
    main()
