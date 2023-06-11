
from microvad.models.spec_rnn import build_spec_rnn

def test_spec_rnn_construction():
    """
    Ensure that the different options construct valid models (does not throw an Exception)
    """

    # default
    build_spec_rnn()

    # enable feature reduction
    build_spec_rnn(reduce=4)

    # multi-layer feature reduction
    build_spec_rnn(reduce=(8, 4))
    
    # remove batch normalization
    build_spec_rnn(batch_norm=False)

