import os
import PIL


from .utils import import_with_auto_install

pgmpy = import_with_auto_install('pgmpy')

from pgmpy.readwrite import BIFReader
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD

BIF_FOLDER_MAP = {
    'alarm': 'medium',
    'child': 'medium',
    'insurance': 'medium',
    'asia': 'small',
    'cancer': 'small',
    'sachs': 'small',
    'survey': 'small',
    'earthquake': 'small'
}


def load_bn_from_BIF(main_data_path, data_folder='bayesian', dataset_name='child', verbose=False):
    bif_file = os.path.join(
        main_data_path, data_folder, BIF_FOLDER_MAP[dataset_name], dataset_name + '.bif', dataset_name + '.bif'
    )
    image_file = os.path.join(main_data_path, data_folder, BIF_FOLDER_MAP[dataset_name], dataset_name + '.png')

    if verbose:
        print(f'Loading graph from {bif_file}')

    reader = BIFReader(bif_file)
    model = reader.get_model()

    if os.path.exists(image_file):
        if verbose:
            print(f'Loading graph image from {image_file}')
        model.image = PIL.Image.open(image_file)

    # Take the leaves as features
    __FEATURES = model.get_leaves()
    __ROOTS = model.get_roots()
    __NODES = model.nodes()
    __NOT_FEATURES = list({node for node in __NODES if node not in __FEATURES and node not in __ROOTS})

    if verbose:
        print(f'Nodes: {__NODES} ({len(__NODES)})')
        print(f'Features/Leaves: {__FEATURES} ({len(__FEATURES)})')
        print(f'Roots: {__ROOTS} ({len(__ROOTS)})')
        print(f'Intermediate (non-roots/non-leaves): {__NOT_FEATURES} ({len(__NOT_FEATURES)})')

    return model


# %%
""""
    ____ ____ ____ ___ _  _ ____ _  _ ____ _  _ ____ 
    |___ |__| |__/  |  |__| |  | |  | |__| |_/  |___ 
    |___ |  | |  \  |  |  | |_\| |__| |  | | \_ |___ 
                                                 
"""


def load_earthquake_with_police():
    """
        Earthquake : 8 samples, 3 features, 2 classifications
    """

    # FEATURES =
    V, M, P = 'Feel Vibration', 'Mary Calls', 'Police Calls'
    # CLASSES =
    A, E = 'Alarm', 'Earthquake'
    VALUES = {
        E: ['No', 'Weak', 'Strong'],
        A: ['Not Ringing', 'Ringing'],
        V: ['No', 'Weak', 'Strong'],
        P: ['No', 'Yes'],
        M: ['No', 'Yes'],
    }

    def card(V):
        return len(VALUES[V])

    def states(V):
        return VALUES

    earthquake_model = BayesianModel([(E, V), (E, A), (A, P), (A, M)])
    earthquake_model.add_cpds(
        TabularCPD(variable=E, variable_card=card(E), values=[[.9], [.05], [.05]], state_names=states(E)),
        TabularCPD(
            variable=A,
            variable_card=card(A),
            values=[
                [.95, .7, .6],
                [.05, .3, .4],
            ],
            evidence=[E],
            evidence_card=[card(E)],
            state_names=states(A)
        ),
        TabularCPD(
            variable=V,
            variable_card=card(V),
            values=[
                [.85, .19, .01],
                [.14, .80, .04],
                [.01, .01, .95],
            ],
            evidence=[E],
            evidence_card=[card(E)],
            state_names=states(V)
        ),
        TabularCPD(
            variable=P,
            variable_card=card(P),
            values=[
                [.97, .5],
                [.03, .5],
            ],
            evidence=[A],
            evidence_card=[card(A)],
            state_names=states(P)
        ),
        TabularCPD(
            variable=M,
            variable_card=card(M),
            values=[
                [.95, .3],
                [.05, .7],
            ],
            evidence=[A],
            evidence_card=[card(A)],
            state_names=states(M)
        ),
    )
    return earthquake_model


def load_BN(main_data_path, name, verbose=False):
    if name in list(BIF_FOLDER_MAP.keys()):
        return load_bn_from_BIF(main_data_path, dataset_name=name, verbose=verbose)
    elif name == 'earthquake_police':
        return load_earthquake_with_police()
    else:
        raise ValueError('Cannot load a BN with name {name}. Check that name.')


def load_toy_financial():
    """
        ____ _ _  _ ____ _  _ ____ ____    ___ ____ _   _ 
        |___ | |\ | |__| |\ | |    |___     |  |  |  \_/  
        |    | | \| |  | | \| |___ |___     |  |__|   |   
                                                    
    """

    from pgmpy.models import BayesianModel
    from pgmpy.factors.discrete.CPD import TabularCPD

    # FEATURES =
    W, D, H, N = ['Warning', 'Devaluation', 'House Crash', 'Negative News']
    # CLASSES =
    C, E = ['Drop Consumer Confidence', 'External Problem']

    model = BayesianModel([(E, C), (E, W), (C, D), (C, H), (C, N), (D, H)])
    model.add_cpds(TabularCPD(E, 2, [[.5], [.5]], evidence=[], evidence_card=[]))
    model.add_cpds(TabularCPD(C, 2, [[.43, .57], [.03, .97]], evidence=[E], evidence_card=[2]))
    model.add_cpds(TabularCPD(W, 2, [[.70, .30], [.34, .66]], evidence=[E], evidence_card=[2]))
    model.add_cpds(TabularCPD(D, 2, [[.93, .07], [.39, .61]], evidence=[C], evidence_card=[2]))
    model.add_cpds(TabularCPD(N, 2, [[.93, .07], [.39, .61]], evidence=[C], evidence_card=[2]))
    model.add_cpds(
        TabularCPD(H, 2, [[.64, .64, .36, .36], [.46, .46, .54, .54]], evidence=[C, D], evidence_card=[2, 2])
    )

    return model