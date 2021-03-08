import streamlit as st
import pesummary
from pesummary.io import read
from peutils import *
#from makewaveform import make_waveform, plot_gwtc1_waveform
from makealtair import make_altair_plots, get_params_intersect
#from makeskymap import make_skymap
from copy import deepcopy

import matplotlib
matplotlib.use('Agg')

from matplotlib.backends.backend_agg import RendererAgg
lock = RendererAgg.lock

st.title('Testing with GWTC-1 pesummary plots')

sectionnames = [
    'Violin plot',
    '2-D posterior plots (time consuming)'
]





def getLatexLabels():
    latexLabels = {
        "mass_1":r"$m_1$",
        "mass_2":r"$m_2$",
        "luminosity_distance":r"$D_{\rm L}$",
        "ra":r"$\alpha$",
        "dec":r"$\delta$",
        "a_1":r"$a_1$",
        "a_2":r"$a_2$"
        }
    return latexLabels



def headerlabel(number):
    return "{0}".format(sectionnames[number-1])

#page = st.radio('Select Section:', [1,2,3,4], format_func=headerlabel)
page = st.radio('Select Section:', [1,2], format_func=headerlabel)
st.markdown("## {}".format(headerlabel(page)))

# -- Query GWOSC for GWTC events
eventlist = get_eventlist(catalog=['GWTC-2', 'GWTC-1-confident'],
                          optional=False)

# -- 2nd and 3rd events are optional, so include "None" option
eventlist2 = deepcopy(eventlist)
eventlist2.insert(0,None)    



eventNames = eventlist


eventsSelected = st.sidebar.multiselect('Select events', eventlist, default = 'GW150914')
x = eventsSelected



chosenlist = list(filter(lambda a: a != None, x))

if len(chosenlist)>3:
    st.markdown("Loading {} events, this will take a while.".format(len(chosenlist)))


if page == 1:

    st.markdown("### Making plots for events:")

    for ev in chosenlist:
        if ev is None: continue
        st.markdown(ev)

    # -- Load PE samples for all events into a pesummary object
    published_dict = load_multiple_events(chosenlist)

    # -- Select parameters to plot
    st.markdown("## Select parameters to plot")
    params = get_params_intersect(published_dict, chosenlist)

    try:
        indx1 = params.index('mass_1')
    except:
        indx1 = 0
        
    param1 = st.selectbox( 'Parameter 1', params, index=indx1 )

    # -- Make plot based on selected parameter
    st.markdown("### Violin plot")
    ch_param = [param1]
    

    latexLabels = getLatexLabels()


    samples = [published_dict[ev][param1] for ev in chosenlist]


        
    fig = pesummary.gw.plots.publication.violin_plots(param1,\
                                                      samples, \
                                                      chosenlist,\
                                                      latexLabels)
    st.pyplot(fig)


if page == 2:  
  

    st.markdown("### Making plots for events:")

    for ev in chosenlist:
        if ev is None: continue
        st.markdown(ev)

    # -- Load PE samples for all events into a pesummary object
    published_dict = load_multiple_events(chosenlist)

    # -- Select parameters to plot
    st.markdown("## Select two parameters to plot")
    params = get_params_intersect(published_dict, chosenlist)

    try:
        indx1 = params.index('mass_1')
        indx2 = params.index('mass_2')
    except:
        indx1 = 0
        indx2 = 1

    param1 = st.selectbox( 'Parameter 1', params, index=indx1 )
    param2 = st.selectbox( 'Parameter 2', params, index=indx2 )


    parameters = [param1,param2]
    samples = [ [published_dict[ev][param1],published_dict[ev][param2]] for ev in chosenlist]

    latexLabels=getLatexLabels()
    fig = pesummary.gw.plots.publication.twod_contour_plots(parameters,\
                                                            samples, \
                                                            chosenlist,\
                                                            latexLabels)
    st.pyplot(fig) 




st.markdown("## About this app")

st.markdown("""
This borrows heavily from Jonah Kanner's [streamlit-pe-demo](https://github.com/jkanner/streamlit-pe-demo)
This app displays data from LIGO, Virgo, and GEO downloaded from the Gravitational Wave Open Science Center at https://gw-openscience.org .
Code for this app [here](https://github.com/hannahm8/streamlit-plot-test)

""")
