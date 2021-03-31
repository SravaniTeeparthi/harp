dataset_type = 'CocoDataset'
data_root = 'data/coco/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', flip_ratio=0.5, direction='horizontal'),
    dict(
        type='Resize',
        img_scale=(858, 480),
        multiscale_mode='value',
        ratio_range=(0.8, 1.2),
        keep_ratio=True
    ),
    # _MAX_LEVEL_VALUE=10 in shear means I am allowing shear to pick
    # a random number between [-max_shear_magnitude*(level/_MAX_LEVEL_VALUE),
    # max_shear_magnitude*(level/_MAX_LEVEL_VALUE)]
    dict(type='CustomShear',
         level=10,
         prob=0.5,
         img_fill_val=0,
         direction='horizontal',
         max_shear_magnitude=0.05240778,
         random_negative_prob=0.5),
    # level=10 in rotate means I am allowing the roation to happen between
    # [-10, 10] degrees.
    dict(type='CustomRotate',
         level=10,
         prob=0.5,
         img_fill_val=0,
         max_rotate_angle=7,
         random_negative_prob=0.5),
    # Translate. I don't want to use 10 pixels for a 858 width image. So
    # I am going with 10 pixels here.
    dict(type='CustomTranslate',
         level=10,
         prob=0.5,
         img_fill_val=0,
         direction='horizontal',
         max_translate_offset=20,
         random_negative_prob=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1333, 800),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip', flip_ratio=0.0),  # flip_ration=0.0 => Flip is not used
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_train2017.json',
        img_prefix=data_root + 'train2017/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_val2017.json',
        img_prefix=data_root + 'val2017/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'annotations/instances_val2017.json',
        img_prefix=data_root + 'val2017/',
        pipeline=test_pipeline))
evaluation = dict(interval=1, metric='bbox')
