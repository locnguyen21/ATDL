import base64
import re
from PIL import Image
from io import BytesIO,StringIO
import numpy as np
a = "data:image/png;base64,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"
b = "data:image/png;base64,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"
#a = a.strip('data:image/png;base64,iVBOR')
#print(a)
#b = base64.b64decode(a)
imgstr = re.search(r'base64,(.*)', b).group(1)
print(imgstr)
temping = BytesIO(base64.b64decode(imgstr))
im = Image.open(temping)
im.show()
#arr = np.array(im)
#print(arr)
#np.savetxt("foo.csv", arr, delimiter=",")