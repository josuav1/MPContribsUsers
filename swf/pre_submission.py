from mpcontribs.users.swf.rest.rester import SWFRester
from mpcontribs.io.core.recdict import RecursiveDict
import pandas as pd
import pymatgen

def run(mpfile, nmax = None):
#    def store_images(paths, names):
#        from PIL import Image
#        Figures = RecursiveDict()
#        for i in range(len(paths)):
#            Figures[names[i]] = Image.open(paths[i])
#        return Figures
    prepath = '~/work/MPContribs/mpcontribs/users/swf/' 
#    paths = [prepath + 'Figure_3.PNG', prepath + 'Figure_4_a.png', prepath + 'Figure_4_b.PNG']
#    names = ['3', '4a', '4b']
#    Figures = store_images(paths, names)
    
    df = pd.read_csv(prepath + 'Energy_product_kJ.csv')
    df = df[df['IP Energy product (kJ/m3)'] != 0]
    del df['Pad #']
      
    def round_to_100_percent(number_set, digit_after_decimal=1):
        unround_numbers = [x / float(sum(number_set)) * 100 * 10 ** digit_after_decimal for x in number_set]
        decimal_part_with_index = sorted([(index, unround_numbers[index] % 1) for index in range(len(unround_numbers))], key=lambda y: y[1], reverse=True)
        remainder = 100 * 10 ** digit_after_decimal - sum([int(x) for x in unround_numbers])
        index = 0
        while remainder > 0:
            unround_numbers[decimal_part_with_index[index][0]] += 1
            remainder -= 1
            index = (index + 1) % len(number_set)
        return [int(x) / float(10 ** digit_after_decimal) for x in unround_numbers]
    
    for index, row in df.iterrows():
        row_3 = round_to_100_percent([row['Fe (at%)'], row['Co (at%)'], row['V (at%)']])
        row['Fe (at%)'] = row_3[0]
        row['Co (at%)'] = row_3[1]
        row['V (at%)'] = row_3[2]
        row['IP Energy product (kJ/m3)'] = round(row['IP Energy product (kJ/m3)'],1)
    
    df_new = df.rename(index = str, columns = {'IP Energy product (kJ/m3)': 'IP_Energy_product', 'Fe (at%)' : 'Fe',
                                      'V (at%)' : 'V', 'Co (at%)' : 'Co'})
    
    idx = 0
    d = RecursiveDict()
    for index, row in df_new.iterrows():
        d['Fe'] = row['Fe']*10
        d['V'] = row['V']*10
        d['Co'] = row['Co']*10
        comp = pymatgen.Composition(d)
        comp = str(comp).split(' ')
        formula = comp[1]+ comp[0] + comp[2]
        p = RecursiveDict()
        p['compositions'] = RecursiveDict()
        p['IP_Energy_product'] = RecursiveDict()
        p['compositions']['Fe'] = str(row['Fe']) + '%'
        p['compositions']['Co'] = str(row['Co']) + '%'
        p['compositions']['V'] = str(row['V']) + '%'
        p['IP_Energy_product'] = str(row['IP_Energy_product']) + ' kJ/m3'
        mpfile.add_hierarchical_data(p, formula)
        if nmax is not None and idx >= nmax-1:
                break
        idx += 1
 
    print(mpfile)

