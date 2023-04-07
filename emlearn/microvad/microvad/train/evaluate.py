
import librosa
import numpy
import pandas


def to_sed_eval_events(e, label='label', end='end', start='start'):
    """
    Convert event lists to format expected by sed_eval
    """
    import dcase_util
    
    sed = e.copy()
    sed = e.rename(columns={
        label: 'event_label',
        end: 'event_offset',
        start: 'event_onset',
        #'file': 'source',
    })
    #print(sed)
    c = dcase_util.containers.MetaDataContainer(sed.to_dict(orient='records'))
    return c
    
def evaluate_events(ref, pred, threshold=0.5, tolerance=0.100):
    
    import sed_eval

    # Convert to sed_eval formats
    ref = to_sed_eval_events(ref, label='event')

    estimated = events_from_predictions(pred, threshold=threshold)
    estimated['start'] = estimated['start'].dt.total_seconds()
    estimated['end'] = estimated['end'].dt.total_seconds()
    est = to_sed_eval_events(estimated)

    # Compute metrics 
    metrics = sed_eval.sound_event.EventBasedMetrics(
        evaluate_onset=True,
        evaluate_offset=False, # only onsets
        event_label_list=ref.unique_event_labels,
        t_collar=tolerance,
        percentage_of_length=1.0,
    )
    metrics.evaluate(
        reference_event_list=ref,
        estimated_event_list=est,
    )
    
    # Extract metrics as flat series
    m = metrics.results_overall_metrics()
    s = pandas.Series({
      'f_measure': m['f_measure']['f_measure'],
      'precision': m['f_measure']['precision'],
      'recall': m['f_measure']['recall'],
      'error_rate': m['error_rate']['error_rate'],
      'substitution_rate': m['error_rate']['substitution_rate'],
      'deletion_rate': m['error_rate']['deletion_rate'],
      'insertion_rate': m['error_rate']['insertion_rate'],
    })
    
    return s


def compute_pr_curve(annotations, pred, thresholds=50, tolerance=0.1):

    df = pandas.DataFrame({
        'threshold': numpy.linspace(0.0, 1.0, thresholds),
    })

    metrics = df.threshold.apply(lambda t: evaluate_events(annotations, pred, threshold=t, tolerance=tolerance))
    df = pandas.merge(df, metrics, right_index=True, left_index=True)
    
    return df


def plot_spectrogram(ax, spec, hop_length=512, sr=16000, events=None, label_activations=None, predictions=None):
    """
    Plot audio spectrogram, optionally with labeled data
    """

    events_lw = 1.5
    
    # Plot spectrogram
    librosa.display.specshow(ax=ax, data=spec, hop_length=hop_length, x_axis='time', y_axis='mel', sr=sr)

    # Plot events
    if events is not None:
        for start, end in zip(events.start, events.end):
            ax.axvspan(start, end, alpha=0.2, color='yellow')
            ax.axvline(start, alpha=0.7, color='yellow', ls='--', lw=events_lw)
            ax.axvline(end, alpha=0.8, color='green', ls='--', lw=events_lw)

    label_ax = ax.twinx()
    
    # Plot event activations
    if label_activations is not None:
        a = label_activations.reset_index()
        a['time'] = a['time'].dt.total_seconds()
        label_ax.step(a['time'], a['event'], color='green', alpha=0.9, lw=2.0)

    # Plot model predictions
    if predictions is not None:
        p = predictions.reset_index()
        p['time'] = p['time'].dt.total_seconds()
        label_ax.step(p['time'], p['probability'], color='blue', alpha=0.9, lw=3.0)
            
        label_ax.axhline(0.5, ls='--', color='black', alpha=0.5, lw=2.0)
        
    label_ax.set_ylim(-0.05, 1.05)


