import os
import json
import numpy as np
import pickle

from sklearn import metrics

import py_neuromodulation as nm
import skops


if __name__ == "__main__":

    # skops.io.dump(model, "movement_decoder.skops")
    model = skops.io.load(os.path.join("src", "movement_decoder.skops"))

    # Create a new stream object
    # Note that the model was trained using features estimated given the settings in settings.json
    settings = json.load(open(os.path.join("src", "settings.json")))

    (
        RUN_NAME,
        PATH_RUN,
        PATH_BIDS,
        PATH_OUT,
        datatype,
    ) = nm.nm_IO.get_paths_example_data()

    (
        raw,
        data,
        sfreq,
        line_noise,
        coord_list,
        coord_names,
    ) = nm.nm_IO.read_BIDS_data(
        PATH_RUN=PATH_RUN, BIDS_PATH=PATH_BIDS, datatype=datatype
    )

    nm_channels = nm.nm_define_nmchannels.set_channels(
        ch_names=raw.ch_names,
        ch_types=raw.get_channel_types(),
        reference="default",  # CAR re-reference for ECoG
        bads=raw.info["bads"],
        new_names="default",
        used_types=("ecog", "dbs", "seeg"),
        target_keywords=["MOV_RIGHT"],
    )

    stream = nm.Stream(
        sfreq=sfreq,
        nm_channels=nm_channels,
        settings=settings,
        line_noise=line_noise,
        coord_list=coord_list,
        coord_names=coord_names,
        verbose=True,
    )

    features = stream.run(data=data)

    features_ECOG_RIGHT_5 = features[
        [f for f in features.columns if "ECOG_RIGHT_5" in f]
    ]

    pr_ = model.predict(features_ECOG_RIGHT_5.to_numpy())

    metrics.accuracy_score(features["MOV_RIGHT"] > 0, pr_)
