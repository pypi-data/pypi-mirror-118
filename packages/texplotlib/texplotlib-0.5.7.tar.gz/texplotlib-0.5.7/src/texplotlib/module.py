# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 02:20:52 2021

@author: Mostafa
"""


import matplotlib as mpl
from os import system as run_command

#%%
plt_to_tex_marker={
        'None': 'None',
        's': 'square*',
        '.': '*',
        'o': 'o',
        '^': 'triangle*',
        'd': 'diamond*',
        '*': 'x',
        }
plt_to_tex_linestyle={
        'None': 'only marks',
        ':': 'dotted',
        '--': 'dashed',
        '-': 'solid',
#        '^': 'triangle*'
        }
#%%
def preview(pathname):
    run_command(f'pdflatex {pathname}.tex')
    run_command(f'start {pathname}.pdf')
#%%
def savetex(pathname,save_type='pic',_preview_=False):
#    x=np.linspace(0,4*np.pi,1000)
#    y=np.cos(x)
    mpl_gca=mpl.pyplot.gca()
    mpl_gcf=mpl.pyplot.gcf()
    
    fig_width_pt,fig_height_pt=mpl_gcf.get_size_inches()*72
#    print(fig_width,fig_height)
#    picture_name='some_test'
    num_of_lines=len(mpl_gca.lines)
    
    has_xgrid=all([xgrid_line.get_visible()=='on' for xgrid_line in mpl_gca.get_xgridlines()])
    has_ygrid=all([ygrid_line.get_visible()=='on' for ygrid_line in mpl_gca.get_ygridlines()])
#    has_ygrid=mpl_gca.get_ygridlines()
#    print(num_of_lines)
    
    tex_title=mpl_gca.title.get_text()
    tex_xlabel=mpl_gca.xaxis.get_label().get_text()
    tex_ylabel=mpl_gca.yaxis.get_label().get_text()
    tex_xlim=mpl_gca.get_xlim()
    tex_ylim=mpl_gca.get_ylim()
    tex_xticks=','.join([str(u) for u in mpl_gca.get_xticks()])
    tex_yticks=','.join([str(u) for u in mpl_gca.get_yticks()])
    temp_tex_legends=mpl_gca.get_legend_handles_labels()
    tex_legends={
            mpl_gca.lines.index(temp_tex_legends[0][n]):temp_tex_legends[1][n]\
            for n in range(len(temp_tex_legends[0]))
            }
    tex_legend_alpha=mpl.pyplot.rcParams['legend.framealpha']
#    
#    return tex_legends
#    for _legend_ in mpl_gca.legend().get_texts():
#        tex_legends.append(_legend_.get_text())
    tex_xy_data=[]
    tex_marker=[]
    tex_markersize=[]
    tex_markercolor=[]
    tex_linestyle=[]
    tex_linecolor=[]
    tex_linewidth=[]
    for line in mpl_gca.lines:
#        print('asaksalsk')
        temp_xy_data=list(zip(line.get_xdata(),line.get_ydata()))
        tex_xy_data.append(''.join([str(xy) for xy in temp_xy_data]))
        tex_marker.append(plt_to_tex_marker[line.get_marker()])
        tex_markersize.append(line.get_markersize()*0.4)
        tex_markercolor.append(mpl.colors.to_hex(line.get_mfc())[1:].upper())
        tex_linestyle.append(plt_to_tex_linestyle[line.get_linestyle()])
        tex_linecolor.append(mpl.colors.to_hex(line.get_color())[1:].upper())
        tex_linewidth.append(line.get_linewidth())
    
    has_tex_title=not tex_title==''
    has_tex_xlabel=not tex_xlabel==''
    has_tex_ylabel=not tex_ylabel==''
#    has_tex_legends=not tex_legends==[]
#    print(tex_markercolor)
#    if has_tex_title:
#        tex_title='\ttitle = {'+str(tex_title)+'},\n'
#    else:
#        tex_title=''
#        
#    if has_tex_xlabel:
#        tex_xlabel='\txlabel = {'+str(tex_xlabel)+'},\n'
#    else:
#        tex_xlabel=''
#    
#    if has_tex_ylabel:
#        tex_ylabel='\tylabel = {'+str(tex_ylabel)+'},\n'
#    else:
#        tex_ylabel=''
#    
#    if has_tex_title:
#        tex_title='\ttitle = {'+str(tex_title)+'},\n'
#    else:
#        tex_title=''
    
#    print(tex_title)
#    print(tex_xlabel)
#    print(tex_ylabel)
#    print(tex_xlim)
#    print(tex_ylim)
#    print(tex_xticks)
#    print(tex_yticks)
#    print(tex_legends)
    
#    return
#    raise Exception('aaaaaaaaaaaaaaaaaaaaaa')
#    path_name=picture_name
    
    file=open(pathname+'.tex','w+')
    
    if save_type=='full':
        file.writelines('\\documentclass{article}\n')
        file.writelines('\\usepackage{tikz,pgfplots}\n')
        file.writelines('\\begin{document}\n')
    
    for n in range(num_of_lines):
        file.writelines('\\definecolor{{linecolor{}}}{{HTML}}{{{}}}\n'.format(n,tex_linecolor[n]))
        file.writelines('\\definecolor{{markerfacecolor{}}}{{HTML}}{{{}}}\n'.format(n,tex_markercolor[n]))
    file.writelines('\\begin{tikzpicture}\n')
    file.writelines('\\pgfplotsset{compat=1.9}\n')
    file.writelines('\\begin{axis}\n')
    file.writelines('[\n')
    file.writelines(f'\twidth = {fig_width_pt},\n')
    file.writelines(f'\theight = {fig_height_pt},\n')
    file.writelines(f'\tscale only axis,\n')
    file.writelines(f'\ttitle = {{{tex_title}}},\n'*has_tex_title)
    file.writelines(f'\txlabel = {{{tex_xlabel}}},\n'*has_tex_xlabel)
    file.writelines(f'\tylabel = {{{tex_ylabel}}},\n'*has_tex_ylabel)
    file.writelines(f'\txmin = {tex_xlim[0]},\n')
    file.writelines(f'\txmax = {tex_xlim[1]},\n')
    file.writelines(f'\tymin = {tex_ylim[0]},\n')
    file.writelines(f'\tymax = {tex_ylim[1]},\n')
    file.writelines(f'\txtick = {{{tex_xticks}}},\n')
    file.writelines(f'\tytick = {{{tex_yticks}}},\n')
    if has_xgrid:
        file.writelines(f'\txmajorgrids,\n')
    if has_ygrid:
        file.writelines(f'\tymajorgrids,\n')
    file.writelines(f'\tlegend style={{\n')
    file.writelines(f'\t\tfill=white,\n')
    file.writelines(f'\t\tfill opacity={tex_legend_alpha},\n')
    file.writelines(f'\t\tdraw opacity=1,\n')
    file.writelines(f'\t\ttext opacity=1,\n')
    file.writelines(f'\t}},\n')
#    file.writelines(f'\tlegend style={{fill=white, fill opacity={tex_legend_alpha}, draw opacity=1}},\n')
    file.writelines(']\n')
    
    for n in range(num_of_lines):
        file.writelines('\\addplot\n')
        file.writelines('[\n')
        file.writelines(f'\t{tex_linestyle[n]},\n')
        file.writelines(f'\tmark={tex_marker[n]},\n')
        file.writelines(f'\tmark size={tex_markersize[n]},\n')
        file.writelines(f'\tmark options={{\n')
        file.writelines(f'\t\tfill = markerfacecolor{n},\n')
        file.writelines(f'\t\tsolid,\n')
        file.writelines(f'\t}},\n')
        file.writelines(f'\tcolor=linecolor{n},\n')
        file.writelines(f'\tline width={tex_linewidth[n]}pt,\n')
        file.writelines(']\n')
        file.writelines('coordinates{\n')
        file.writelines(tex_xy_data[n])
        file.writelines('\n};\n')
    
#    print(tex_legends=={})
    if not tex_legends=={}:
        file.writelines('\\legend{\n')
#        print(tex_legends)
        for n in range(num_of_lines):
            if n in tex_legends:
                file.writelines('\t{{{}}},\n'.format(tex_legends[n]))
            else:
                file.writelines('\t{},\n')
        file.writelines('}\n')
#    file.writelines('[\n')
    
    
    
    file.writelines('\\end{axis}\n')
    file.writelines('\\end{tikzpicture}\n')
    
    if save_type=='full':
        file.writelines('\\end{document}')
    
    file.close()
    
    if _preview_:
        preview(pathname)
    
    return