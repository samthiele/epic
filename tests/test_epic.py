import unittest
import os
from pathlib import Path
import numpy as np


from epic import load_image, pick_single, pick_multi

class MyTestCase(unittest.TestCase):
    def test_load(self):
        pth = os.path.join(str(Path(__file__).parent), "stinkbug.jpg")
        self.assertTrue( os.path.exists(pth))
        image = load_image(pth)
        self.assertEqual( image.shape, (240,320,3) )
        self.assertEqual( np.max(image), 207 )
        return image

    def test_pick_single(self):

        image = self.test_load()
        pick_single( image, line=True, n=3 )

    def test_pick_multi(self):

        image = self.test_load()
        image2 = image[::-1, :, : ].copy()

        pick_multi( image, image2, line=False, n=3 )

if __name__ == '__main__':
    unittest.main()
