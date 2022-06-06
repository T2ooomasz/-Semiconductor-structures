import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
from typing import List, Optional, Mapping, Union, Dict

class GIF:
    def __init__(
        self,
        name,
        fps: Optional[float] = 20
    ):
        self.name = "GIF/" + name
        self.fps = fps

    def make(self, table):
        filenames = []
        for i in range(len(table)):
            filename=f'graphsforGIF/{i}.png'
            filenames.append(filename)

        # build gif
        with imageio.get_writer(self.name + '.gif', mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(filename,)
                writer.append_data(image)

        # Remove files
        for filename in set(filenames):
            os.remove(filename)

