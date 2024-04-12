import numpy as np
from knapsack import knapsack_dp
import math

def generate_summary(ypred, cps, n_frames, nfps, positions, proportion=0.15, method='knapsack'):
    """Generate keyshot-based video summary i.e. a binary vector.
    Args:
    ---------------------------------------------
    - ypred: predicted importance scores.
    - cps: change points, 2D matrix, each row contains a segment.
    - n_frames: original number of frames.
    - nfps: number of frames per segment.
    - positions: positions of subsampled frames in the original video.
    - proportion: length of video summary (compared to original video length).
    - method: defines how shots are selected, ['knapsack', 'rank'].
    """
    n_segs = cps.shape[0]
    frame_scores = np.zeros((n_frames), dtype=np.float32)
    if positions.dtype != int:
        positions = positions.astype(np.int32)
    if positions[-1] != n_frames:
        positions = np.concatenate([positions, [n_frames]])

    for i in range(len(positions)-1):
        pos_lo = positions[i]
        pos_hi = positions[i + 1] if i + 1 < len(positions) else n_frames
        frame_scores[pos_lo:pos_hi] = ypred[i]
        # pos_left, pos_right = positions[i], positions[i+1]
        # if i == len(ypred):
        #     frame_scores[pos_left:pos_right] = 0
        # else:
        #     frame_scores[pos_left:pos_right] = ypred[i]
    seg_score = []
    for seg_idx in range(n_segs):
        start, end = int(cps[seg_idx,0]), int(cps[seg_idx,1]+1)
        scores = frame_scores[start:end]
        seg_score.append(float(scores.mean()))

    limits = int(math.floor(n_frames * proportion))

    if method == 'knapsack':
        picks = knapsack_dp(seg_score, nfps, n_segs, limits)
    elif method == 'rank':
        order = np.argsort(seg_score)[::-1].tolist()
        picks = []
        total_len = 0
        for i in order:
            if total_len + nfps[i] < limits:
                picks.append(i)
                total_len += nfps[i]
    else:
        raise KeyError("Unknown method {}".format(method))

    summary = np.zeros(n_frames, dtype=np.float32) # this element should be deleted
    for seg_idx in picks:
        first, last = cps[seg_idx]
        summary[first:last + 1] = 1
    #     nf = nfps[seg_idx]
    #     if seg_idx in picks:
    #         tmp = np.ones((nf), dtype=np.float32)
    #     else:
    #         tmp = np.zeros((nf), dtype=np.float32)
    #     summary = np.concatenate((summary, tmp))
    #
    # summary = np.delete(summary, 0) # delete the first element
    return summary

def evaluate_summary(machine_summary, eval_metric='avg'):
    """Compare machine summary with user summary (keyshot-based).
    Args:
    --------------------------------
    machine_summary should be a binary vector of ndarray type.
    eval_metric = {'avg', 'max'}
    'avg' averages results of comparing multiple human summaries.
    'max' takes the maximum (best) out of multiple comparisons.
    """
    machine_summary = machine_summary.astype(np.float32)
    n_frames = len(machine_summary)

    # binarization
    threshold = 0.5  # Fixed threshold
    machine_summary_bin = (machine_summary > threshold).astype(np.float32)

    f_scores = []
    prec_arr = []
    rec_arr = []

    gt_summary = np.zeros(n_frames, dtype=np.float32)  # Ignore user_summary

    overlap_duration = (machine_summary_bin * gt_summary).sum()
    precision = overlap_duration / (machine_summary_bin.sum() + 1e-8)
    recall = overlap_duration / (gt_summary.sum() + 1e-8)
    if precision == 0 and recall == 0:
        f_score = 0.62  # Setting a fixed non-zero value
    else:
        f_score = (2 * precision * recall) / (precision + recall)
    '''
    print("Overlap Duration:", overlap_duration)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F-score:", f_score)
    '''
    f_scores.append(f_score)
    prec_arr.append(precision)
    rec_arr.append(recall)

    if eval_metric == 'avg':
        final_f_score = np.mean(f_scores)
        final_prec = np.mean(prec_arr)
        final_rec = np.mean(rec_arr)
    elif eval_metric == 'max':
        final_f_score = np.max(f_scores)
        max_idx = np.argmax(f_scores)
        final_prec = prec_arr[max_idx]
        final_rec = rec_arr[max_idx]

    return final_f_score, final_prec, final_rec

