# this is based on mscalev3 but with some small differences

import tensorflow as tf
from wispy.mscalev3 import make_scale_tensor, ScaleLayer


def build_subnetwork(
    input_tensor,
    output_shape,
    units,
    output_name,
    activation="relu",
    n_blocks=1,
    layers_per_block=3,
    skip_connection=False,
    skip_connection_dense=False,
):
    """
    subnetwork with the option of skip-connections

    n_blocks >= 1
    """
    assert n_blocks >= 1, f"n_blocks must be >=1, got {n_blocks}"

    if skip_connection:
        if skip_connection_dense:
            tmp = tf.keras.layers.Dense(units, activation=activation)(input_tensor)
        else:
            tmp = input_tensor

    # x = tf.keras.layers.Dense(units, activation=activation)(input_tensor)
    x = input_tensor

    # x = tfa.layers.GroupNormalization(groups=1)(x)
    # x = tf.keras.layers.BatchNormalization(momentum=0.9)(x)
    for _ in range(n_blocks):
        for _ in range(layers_per_block):
            x = tf.keras.layers.Dense(units, activation=activation)(x)
        # x = tfa.layers.GroupNormalization(groups=1)(x)
        # x = tf.keras.layers.BatchNormalization(momentum=0.9)(x)

        if skip_connection:
            x = tf.keras.layers.add([x, tmp])
            tmp = x

    # single output here?
    x = tf.keras.layers.Dense(output_shape, activation="linear", name=output_name)(x)

    return x


def build_model(
    input_shape=1,
    output_shape=1,
    units=[128],
    activation="relu",
    scale_activation="relu",
    n_blocks=[1],
    scales=[1],
    layers_per_block=3,
    scale_dimension=0,
    dtype=None,
    skip_connection=False,
    skip_connection_dense=False,
    final_dense=False,
):
    """[summary]

    Args:
        input_shape (int, optional): [description]. Defaults to 1.
        output_shape (int, optional): [description]. Defaults to 1.
        units (list, optional): [description]. Defaults to [128].
        activation (str, optional): [description]. Defaults to "relu".
        n_blocks (list, optional): [description]. Defaults to [2].
        scales (list, optional): [description]. Defaults to [1].
        layers_per_block (int, optional): [description]. Defaults to 3.
        scale_dimension (int, optional): [description]. Defaults to 0.
            Use this to select which feature to apply the scaling to.
        dtype ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    assert (
        len(scales) == len(n_blocks) == len(units)
    ), "units, n_blocks, scales must have same length"

    input_layer = tf.keras.Input(shape=(input_shape,))

    # create sub-networks
    xs = []
    for i, scale in enumerate(scales):
        scale_tensor = make_scale_tensor(
            input_shape, scale_dimension, scale, dtype=dtype
        )
        scaled_input = ScaleLayer(scale_tensor)(input_layer)
        scaled_input = tf.keras.layers.Dense(units[i], activation=scale_activation)(
            scaled_input
        )
        xs.append(
            build_subnetwork(
                input_tensor=scaled_input,
                output_shape=output_shape,
                units=units[i],
                activation=activation,
                n_blocks=n_blocks[i],
                layers_per_block=layers_per_block,
                skip_connection=skip_connection,
                skip_connection_dense=skip_connection_dense,
                output_name=f"outputs_{i}",
            )
        )

    if len(xs) > 1:
        output_layer = tf.keras.layers.add([x for x in xs])
    else:
        output_layer = xs[0]

    if final_dense:
        output_layer = tf.keras.layers.Dense(output_shape, activation="linear")(
            output_layer
        )
    model = tf.keras.models.Model(inputs=input_layer, outputs=output_layer)
    return model