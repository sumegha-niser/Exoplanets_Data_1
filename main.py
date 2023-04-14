# arsenal of some functions

#extracting planets according to radius requirements
def radius_requirement(dataset,bound_upr, bound_lwr):
    radius=dataset['pl_rade']
    rad_condition = (radius>=bound_lwr) & (radius<= bound_upr)
    req_rad = dataset[rad_condition]
    return req_rad, rad_condition

#to extract planets around FGK stars
def FGK(dataset):
    spec_type=dataset['st_spectype'].astype(str)
    FGK = spec_type.str.startswith(('F', 'G', 'K'))
    return FGK
#finding the density of the planet
def density(dataset):
    import numpy as np
    dataset['pl_vole'] = 4/3 * np.pi * (dataset['pl_rade']**3)
    dataset['pl_densitye'] = dataset['pl_bmasse']/dataset['pl_vole']
    return dataset['pl_densitye']