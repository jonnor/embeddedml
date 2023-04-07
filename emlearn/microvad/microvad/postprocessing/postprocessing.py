
import copy

def merge_overlapped_predictions(window_predictions, window_hop):
    
    # flatten the predictions from overlapped windows
    predictions = []
    for win_no, win_pred in enumerate(window_predictions):
        win_start = window_hop * win_no
        for frame_no, p in enumerate(win_pred):
            s = {
                'frame': win_start + frame_no,
                'probability': p,
            }
        
            predictions.append(s)
        
    df = pandas.DataFrame.from_records(predictions)
    df['time'] = pandas.to_timedelta(df['frame'] * time_resolution, unit='s')
    df = df.drop(columns=['frame'])
    
    # merge predictions from multiple windows 
    out = df.groupby('time').median()
    return out

def predict_spectrogram(model, spec, window_hop=1):
    
    # prepare input data. NOTE: must match the training preparation in getXY
    wins = compute_windows(spec, frames=window_length, step=window_hop)       
    X = numpy.expand_dims(numpy.stack( [ (w-Xm).T for w in wins ]), -1)
    
    # make predictions on windows
    y = numpy.squeeze(model.predict(X, verbose=False))

    out = merge_overlapped_predictions(y, window_hop=window_hop)

    return out


def events_from_predictions(pred,
        threshold=0.5,
        label='yes',
        event_duration_max=1.0):

    
    event_duration_max = pandas.Timedelta(event_duration_max, unit='s')
    
    events = []
    inside_event = False
    event = {
        'start': None,
        'end': None,
    }
    
    for t, r in pred.iterrows():
        p = r['probability']

        # basic state machine for producing events
        if not inside_event and p > threshold:
            event['start'] = t
            inside_event = True
            
        elif inside_event and ((p < threshold) or ((t - event['start']) > event_duration_max)):
            event['end'] = t
            events.append(copy.copy(event))
            
            inside_event = False
            event['start'] = None
            event['end'] = None
        else:
            pass
    
    if len(events):
        df = pandas.DataFrame.from_records(events)
    else:
        df = pandas.DataFrame([], columns=['start', 'end'], dtype='timedelta64[ns]')
    df['label'] = label
    return df

