AcrossPatientDecodingModel
==========================

This package demonstrates the use of the across-patient and cohort movement decoding model, presented in the publication *"Invasive neurophysiology and whole brain connectomics for neural decoding in patients with brain implants"* [1]_.

We recommend installing the package using `rye <https://rye-up.com/guide/installation/>`_:

.. code-block::

    git clone https://github.com/neuromodulation/AcrossPatientDecodingModel.git
    rye pin 3.10
    rye sync
    .\.venv\Scripts\activate


An example script, including the respective feature estimation, is shown in the `src/run_model.py`. 

.. code-block::

    import py_neuromodulation as nm
    import skops

    model = skops.io.load("movement_decoder.skops")

    stream = nm.Stream(...)
    features = stream.run()

    model.predict(features.to_numpy())

References
----------

.. [1] Merk, T. et al. *Invasive neurophysiology and whole brain connectomics for neural decoding in patients with brain implants*, `https://doi.org/10.21203/rs.3.rs-3212709/v1` (2023).

