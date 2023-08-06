# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['picnik']
install_requires = \
['derivative==0.3.1',
 'matplotlib==3.1.2',
 'numpy==1.19.1',
 'pandas==1.2.2',
 'scipy==1.6.3']

setup_kwargs = {
    'name': 'picnik',
    'version': '0.1.0',
    'description': 'A package to make isoconversional computations for non-isothermal kinetics',
    'long_description': '# pICNIK \n\npICNIK is a package for isoconversional computations for non-isothermal kinetcis.\\\nThe package has an object oriented interface with two classes: DataExtraction and ActivationEnergy, with the purpose of managing the experimental data and computing activation energies ($E_{\\alpha}$) with the next isoconversional methods: \n\n- Ozawa-Flynn-Wall (OFW)\\\n$\\ln{\\left(\\beta_{i}\\right)} = \\left[\\ln{\\left(\\frac{A_{\\alpha}E_{\\alpha}}{g(\\alpha)R}\\right)}-5.331\\right]-1.052\\frac{E_{\\alpha}}{RT_{\\alpha,i}}}$ \n\n- Kissinger-Akahira-Sunose (KAS)\\ \n$\\ln{\\left(\\frac{\\beta_{i}}{T_{\\alpha ,i}^{2}}\\right)}\\approx\\ln{\\left[\\frac{A_\\alpha R}{E_\\alpha g(\\alpha)}\\right]}-\\frac{E_\\alpha}{RT_{\\alpha ,i}}$\n\n- Friedman (Fr)\\\n$\\ln{\\left(\\frac{d\\alpha}{dt}\\right)_{\\alpha ,i}} = \\ln{\\left[A_{\\alpha}f\\left(\\alpha\\right)\\right]} - \\frac{E_{\\alpha}}{RT_{\\alpha ,i}}$\n\n- Vyazovkin (Vy)\\\n$\\phi=n(n-1) - \\sum_{i}^{n} \\sum_{j \\neq i}^{n-1} \\frac{\\beta_j I(E_{\\alpha},T_{\\alpha ,i})}{\\beta_i I(E_{\\alpha},T_{\\alpha ,j})}$\n\n- Advanced method of Vyazovkin (aVy)\\\n$\\phi=n(n-1) - \\sum_{i}^{n} \\sum_{j \\neq i}^{n-1} \\frac{\\beta_j J(E_{\\Delta\\alpha},T_{\\Delta\\alpha ,i})}{\\beta_i J(E_{\\Delta\\alpha},T_{\\Delta\\alpha ,j})}$\n\n### Installation\n\n`picnik` can be installed from PyPi with `pip`:\n`$ pip install picnik`\n\n\n### DataExtractioin class\n\nIt has methods to open the .csv files containing the thermogravimetric data as pandas DataFrames for the experimental data, computing and adding the conversion for the process ($\\alpha$) and the conversion rate ($d\\alpha/dt$) as columns in the DataFrame.\\\nThe class also has methods for creating isoconversional DataFrames of time, temperature, conversion rates (for the OFW, KAS, Fr and Vy methods) and also "advanced" DataFrames of time and temperature (for the aVy method).\\\nExample:\n\n    import picnik as pnk\n \n    files = ["HR_1.csv","HR_2.csv",...,"HR_n.csv"]\n    xtr = pnk.DataExtraction()\n    xtr.set_data(files)\n    xtr.data_extraction()\n    xtr.isoconversional()\n    xtr.adv_isoconversional()\n    \nThe DataFrames are stored as attributes of the `xtr` object \n\n\n### ActivationEnergy class\n\nThis class has methods to compute the activation energies with the DataFrames created with the `xtr` object along with its associated error. The `Fr()`,`OFW()`,`KAS()` methods return a tuple of three, two and two elements respectively. The first element of the tuples is a numpy array containing the isoconversional activation energies. The second element contains the associated error within a 95\\% confidence interval. The third element in the case of the `Fr()` method is a numpy array containing the intercept of the Friedman method. The `Vy()` and `aVy()` only return a numpy array of isoconversional activation energies, the error associated to this methods are obtained with the `Vy_error()` and `aVy_error()` methods\nExample:\n\n    ace = pnk.ActivationEnergy(xtr.Beta,\n                               xtr.TempIsoDF,\n                               xtr.diffIsoDF,\n                               xtr.TempAdvIsoDF,\n                               xtr.timeAdvIsoDF)\n    E_Fr, E_OFW, E_KAS, E_Vy, E_aVy = ace.Fr(), ace.OFW(), ace.KAS(), ace.Vy(), ace.aVy()\n    Vy_e, aVy_e = ace.Vy_error(), ace.aVy_error()\n    \nThe constructor of this class needs five arguments, a list/array/tuple of Temperature rates, and four DataFrames: one of temperature, one of convertsion rates and two "advanced" one of temperature and the other of time.\n\n### Saving results\n\nThe DataExtractionclass also has a method to export the results as .csv or .xlsx files:\n\n    xtr.save_df(E_Fr = E_Fr[0], \n                E_OFW = E_OFW[0], \n                E_KAS = E_KAS[0], \n                E_Vy = E_Vy, \n                E_aVy = E_aVy,\n                file_t="xlsx" )\n',
    'author': 'ErickErock',
    'author_email': 'ramirez.orozco.erick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ErickErock/pICNIK',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
