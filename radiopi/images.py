from twisted.web.resource import Resource

import os


class ImageRootResource(Resource):
    def getChild(self, path, request):
        try:
            return ImageResource(path)
        except ValueError:
            return "XX"
            # BadResource()


class ImageResource(Resource):
    def __init__(self, path):
        self.path = path
        Resource.__init__(self)

    def render_GET(self, request):
        if b'..' in self.path:
            request.setRespnseCode(400)
            return b''

        name = self.path.decode('utf-8')
        imgname = os.path.basename(name)
        imgpath = os.path.join('radiopi', 'static', 'image', imgname)
        imgpath = os.path.abspath(imgpath)
        if os.path.exists(imgpath):
            with open(imgpath, 'rb') as source:
                filename = 'filename="%s"' % (name)
                request.setHeader('content-disposition', filename)
                request.setHeader('content-type', 'image/jpg')

                return source.read()

        return b'File ' + str.encode(imgname) + b' does not exist.'
