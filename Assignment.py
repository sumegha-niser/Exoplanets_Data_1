#importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from tabulate import tabulate
from main import radius_requirement, FGK ,density

#reading the csv file
dataset = pd.read_csv('PSCompPars_2023.04.03_23.35.45.csv',comment='#')


############################## QUESTION 1 ###########################
#radius bounds
lower_bound = 0.5
upper_bound = 1.6
#stars with radius that satisfy this condition
req=radius_requirement(dataset,upper_bound, lower_bound)
answer1=len(req[0])
print('There are %d planets with radius in the range %.1f REarth and %.1fREarth.\n'%(answer1 ,lower_bound ,upper_bound))

############################## QUESTION 2 ##########################
#planets that satisy FGK and rad_condition
FGK_c = FGK(dataset)
filtered_dataset = dataset[req[1] & FGK_c]
answer2 = (len(filtered_dataset))
print('Of these planets,%d revolve around F,G,K stars'%answer2)

#LIST THEM IN A TABLE
table1 = tabulate(filtered_dataset, headers='keys', tablefmt='psql')
#make a csv table out of it
filtered_dataset.to_csv('FGK_0.5to1.6.csv', index=False)
# write the table, but nan in the place of blank values gotta change that
with open('q2.txt','w') as f:
    f.write(table1)

#Make a plot of Equilibrium temperature vs Distance from Earth for these planets.
fig, ax = plt.subplots()
ax.scatter(filtered_dataset['sy_dist'],filtered_dataset['pl_eqt'],color = 'k', s=3)
ax.set_title('Equilibrium temperature v/s Distance from Earth' , fontsize=16,fontweight='bold')
ax.legend(['planet'])
ax.set_xlabel('Distance from Earth (pc)')
ax.set_ylabel('Equilibrium temperature (K)')
fig.savefig('pl_eqt_vs_sy_dist.png')

#discovery condition
discovery_method=filtered_dataset['discoverymethod'].astype(str)
direct_imaging=filtered_dataset[discovery_method.str.startswith('Imaging')]
answer3 = len(direct_imaging)
print('%d planets among them are discovered through direct imaging method.\n'%answer3)

############################## QUESTION 3 ###########################
l_bound=1.6
u_bound =4
filtered_dataset2 = dataset[radius_requirement(dataset,u_bound,l_bound)[1] & FGK_c]
answer4 = (len(filtered_dataset2))

print('There are %d planets with radius in the range %.1fREarth and %.1fREarth.'%(answer4 ,l_bound ,u_bound))
#make a csv table out of it
filtered_dataset2.to_csv('FGK_1.6to4.csv', index=False)
#List them in a table. 
table2 = tabulate(filtered_dataset2, headers='keys', tablefmt='psql')
with open('q3.txt','w') as f:
    f.write(table2)

############################## QUESTION 4 ###########################
#Make a plot of radius vs. mass of all the planets in the dataset 
fig1, ax = plt.subplots()
ax.scatter(dataset['pl_bmasse'],dataset['pl_rade'],s=250,color='k',alpha=0.5)
ax.set_title('Radius of planet v/s mass of planet' , fontsize=16,fontweight='bold')
ax.set_ylabel('(Earth)Radius of the planet (R_Earth)')
ax.set_xlabel('(Earth)Mass of the planet (M_Earth)')
#To plot Earth, Venus and Jupiter
earth = plt.imread('image.png')
venus = plt.imread('venus.png')
jupiter = plt.imread('Jupiter-PNG.png')
earth_imgbox = OffsetImage(earth, zoom=0.0289, alpha=0.8)
venus_imgbox = OffsetImage(venus, zoom=0.07, alpha=0.8)
jup_imgbox=OffsetImage(jupiter, zoom=0.08, alpha=0.8)
ert = AnnotationBbox(earth_imgbox, (1, 1), frameon=False, label='Earth')
vns = AnnotationBbox(venus_imgbox, (0.815, 0.949), frameon=False, label='Venus')
jptr = AnnotationBbox(jup_imgbox, (317.907, 10.973), frameon=False, label='Jupiter')
ax.text(100000,75,'*The images are not to scale', fontsize=10)

ax.add_artist(ert)
ax.add_artist(vns)
ax.add_artist(jptr)
ax.legend(['planet'])
fig1.savefig('rad_vs_mass.png')

############################## QUESTION 5 ###########################

fig3, ax = plt.subplots()
ax.scatter(dataset['st_met'],dataset['pl_rade'],color='k', s=9,alpha=0.7)
#setting the y-scale to be log for more resolution
ax.set_title('log of radius v/s stellar metallicity of the planet')
ax.set_yscale('log')
ax.set_ylabel('(Earth)Radius of the planet (R_Earth) (log)')
ax.legend(['planet'])
ax.set_xlabel('Stellar metallicity')
fig3.savefig('q5.png')

#PART 2


fig, ax = plt.subplots()
ax.scatter(dataset['st_met'],dataset['pl_bmasse'],color='k', s=9,alpha=0.7)
ax.set_title(' log of mass v/s stellar metallicity of the planet')
ax.legend(['planet'])
#setting the x-scale to be log for more resolution
ax.set_yscale('log')
ax.set_ylabel('(Earth)Mass of the planet (M_Earth) in log scale')
ax.set_xlabel('Stellar metallicity (dex)')
fig.savefig('q5_2.png')



############################## QUESTION 6 ###########################

filtered_dataset = dataset[dataset['pl_rade'].notnull() & dataset['pl_bmasse'].notnull()]
fig,ax= plt.subplots()
denisy= density(filtered_dataset)
ax.scatter(filtered_dataset['pl_rade'],denisy,color='k', s=9,alpha=0.7)
ax.set_title('log(Density) v/s log(mass of the planet)')
ax.legend(['planet'])

ax.set_xlabel('(Earth)Radius of the planet (R_Earth) (log)')
ax.set_ylabel('Density of the planet (log)')
ax.set_yscale('log')
ax.set_xscale('log')
#setting the scales to be log for more resolution
fig.savefig('den_vs_rad.png')