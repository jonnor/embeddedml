
def build_spec_rnn(bands=40,
                  timesteps=None,
                  n_classes=1,
                  reduce=None,
                  batch_norm=True,
                  rnn_units=(13, 10, 4)):
    """
    Basic RNN/GRU model for mel-spectrogram

    Based on "Voice activity detection for low-resource settings"
    http://cs230.stanford.edu/projects_winter_2020/reports/32224732.pdf
    where it outperformed WebRTC VAD

    Default parameters will build their model
    """
    
    from tensorflow.keras import layers as l
    from tensorflow.keras import Sequential
    import numbers
                              
    # Feature reduction
    reduction_layers = []
    if reduce is not None:
        if isinstance(reduce, numbers.Number):
            reduce = [ reduce ]
        
        for n in reduce:
            reduction_layers += [ l.TimeDistributed(l.Dense(n)) ]
    
    # RNN
    rnn_layers = []
    for n in rnn_units:
        rnn_layers += [ l.GRU(n, return_sequences=True) ]
        if batch_norm:
            rnn_layers += [ l.BatchNormalization() ]
                              
    model = Sequential([
        l.Input(shape=(timesteps, bands)),
        *reduction_layers,
        *rnn_layers,
        l.TimeDistributed(l.Dense(n_classes)),
        l.Activation('sigmoid'),
    ])

    return model
