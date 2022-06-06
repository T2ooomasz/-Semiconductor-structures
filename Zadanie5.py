from G_R_M import G_R_M
from make_gif import GIF

class grapgh_for_gif:
    def __init__(
        self,
        #compound_1,
        #compound_2,  
        #mix_proportion, 
        #temperature,
        #bowing,
        #tension,
        #resolution,
        #percent_range
    ):  
        #self.compound_1 = compound_1,
        #self.compound_2 = compound_2,  
        #self.mix_proportion = mix_proportion, 
        #self.temperature = temperature,
        #self.bowing = bowing,
        #self.tension = tension,
        #self.resolution = resolution,
        #self.percent_range = percent_range
        #self.iteration = 0
        self.name = "noname"

    def git_with_(self, name, List):
        if name == 'mix_proportion':
            self.mix_proportion = List
        elif name == 'temperature':
            self.temperature = List
        elif name == 'bowing':
            self.bowing = List
        elif name == 'tension':
            self.tension = List
        else:
            print("Error - no posible gif from ", name)

        #self.iteration = len(List)
        #self.name = name
        self.gif_from_list(name, List)

    def gif_from_list(
        self,
        name,
        List
    ):

        bands = G_R_M(self.compound_1, self.compound_2)
        for i in range(len(List)):
            bands.draw(
                compound_1=self.compound_1,
                compound_2=self.compound_2,
                mix_proportion=self.mix_proportion,
                temperature=self.temperature,
                bowing=self.bowing,
                tension=self.tension,
                resolution=self.resolution,
                percent_range=self.percent_range,
                name=str(i)
            ) 
        gif = GIF(str(name))
        gif.make(List)

    def gif_with_mix_proportion(
        self,
        compound_1,
        compound_2,  
        MIX_proportion, 
        temperature,
        bowing,
        tension,
        resolution,
        percent_range):

        bands = G_R_M(compound_1, compound_2)
        for i in range(len(MIX_proportion)):
            bands.draw(
                compound_1=compound_1,
                compound_2=compound_2,
                mix_proportion=MIX_proportion[i],
                temperature=temperature,
                bowing=bowing,
                tension=tension,
                resolution=resolution,
                percent_range=percent_range,
                name=str(i)
            ) 
        gif = GIF("mix_proportion")
        gif.make(MIX_proportion)

    def gif_with_temperature(
        self,
        compound_1,
        compound_2,  
        mix_proportion, 
        Temperature,
        bowing,
        tension,
        resolution,
        percent_range):

        bands = G_R_M(compound_1, compound_2)
        for i in range(len(Temperature)):
            bands.draw(
                compound_1=compound_1,
                compound_2=compound_2,
                mix_proportion=mix_proportion,
                temperature=Temperature[i],
                bowing=bowing,
                tension=tension,
                resolution=resolution,
                percent_range=percent_range,
                name=str(i)
            ) 
        gif = GIF("temperature")
        gif.make(Temperature)

    def gif_with_bowing(
        self,
        compound_1,
        compound_2,  
        mix_proportion, 
        temperature,
        Bowing,
        tension,
        resolution,
        percent_range):

        bands = G_R_M(compound_1, compound_2)
        for i in range(len(Bowing)):
            bands.draw(
                compound_1=compound_1,
                compound_2=compound_2,
                mix_proportion=mix_proportion,
                temperature=temperature,
                bowing=Bowing[i],
                tension=tension,
                resolution=resolution,
                percent_range=percent_range,
                name=str(i)
            ) 
        gif = GIF("bowing")
        gif.make(Bowing)

    def gif_with_tensin(
        self,
        compound_1,
        compound_2,  
        mix_proportion, 
        temperature,
        bowing,
        Tension,
        resolution,
        percent_range):

        bands = G_R_M(compound_1, compound_2)
        for i in range(len(Tension)):
            bands.draw(
                compound_1=compound_1,
                compound_2=compound_2,
                mix_proportion=mix_proportion,
                temperature=temperature,
                bowing=bowing,
                tension=Tension[i],
                resolution=resolution,
                percent_range=percent_range,
                name=str(i)
            ) 
        gif = GIF("tension")
        gif.make(Tension)
