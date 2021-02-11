import os
import sys
import time
import numpy as np 
from tqdm import tqdm

from sklearn.metrics import confusion_matrix, balanced_accuracy_score
from tensorflow.keras.models import load_model

from wavenet import build_wavenet_model
from wavenet_loader import HeySnipsDataset 
from train_wavenet import parse_args


def main(args):
    start = time.time()

    testset = HeySnipsDataset(os.path.join(args.dataset_dir, args.testset), 
                              num_features=args.num_features, workers=2,
                              shuffle=False)

    model = load_model(args.eval_model)
    model.summary()

    preds = model.predict(testset)
    targets = testset.get_labels()

    class_preds = np.where(preds < 0.5, 0, 1)

    cf = confusion_matrix(targets, class_preds)
    print(cf)

    tn, fp, fn, tp = cf.ravel()
    print(f'True Positive: {tp}')
    print(f'True Negative: {tn}')
    print(f'False Positive: {fp}')
    print(f'False Negative: {fn}')
    print(f'Precision: {tp/(tp+fp)}')
    print(f'Recall: {tp/(tp+fn)}')

    print(f'Balanced Accuracy: {balanced_accuracy_score(targets, class_preds)}')

    print(f'Script completed in {time.time()-start:.2f} secs')

    return 0

if __name__ == '__main__':
    args = parse_args()
    sys.exit(main(args))
