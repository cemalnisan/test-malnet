import os


def filter_types(args, lines):
    types_to_exclude = ['adware', 'trojan', 'benign', 'riskware']

    filtered_files = []
    files = [args['image_dir'] + file.strip() + '.png' for file in lines]

    for file in files:
        mtype = file.split('/')[-2]
        if mtype not in types_to_exclude:
            filtered_files.append(file)

    '''for file in files:
        # Update for new dataset structure
        try:
            mtype = file.split('malnet-images-tiny01/')[1].split('/')[0]
            if mtype not in types_to_exclude:
                filtered_files.append(file)
        except IndexError:
            print(f"Skipping file due to unexpected format: {file}")'''

    return filtered_files


def get_split_info(args):
    with open(os.getcwd() + '/split_info/{}/train.txt'.format(args['group']), 'r') as f:
        lines_train = f.readlines()

    # Check if val.txt exists, if not, create an empty list
    # to avoid errors when trying to read it
    val_path = os.getcwd() + '/split_info/{}/val.txt'.format(args['group'])
    if os.path.exists(val_path):
        with open(val_path, 'r') as f:
            lines_val = f.readlines()
    else:
        print("Validation dataset (val.txt) not found. Proceeding without validation data.")
        lines_val = []

    with open(os.getcwd() + '/split_info/{}/test.txt'.format(args['group']), 'r') as f:
        lines_test = f.readlines()

    if args['malnet_tiny']:
        files_train = filter_types(args, lines_train)
        files_val = filter_types(args, lines_val)
        files_test = filter_types(args, lines_test)
    else:
        files_train = [args['image_dir'] + file.strip() + '.png' for file in lines_train]
        files_val = [args['image_dir'] + file.strip() + '.png' for file in lines_val]
        files_test = [args['image_dir'] + file.strip() + '.png' for file in lines_test]

    if args['group'] == 'type':
        labels = sorted(list(set([file.split('/')[-2] for file in files_train])))
        label_dict = {t: idx for idx, t in enumerate(labels)}

        train_labels = [label_dict[file.split('/')[-2]] for file in files_train]
        val_labels = [label_dict[file.split('/')[-2]] for file in files_val]
        test_labels = [label_dict[file.split('/')[-2]] for file in files_test]

    elif args['group'] == 'family':
        labels = sorted(list(set([file.split('/')[-2] for file in files_train])))
        label_dict = {t: idx for idx, t in enumerate(labels)}

        train_labels = [label_dict[file.split('/')[-2]] for file in files_train]
        val_labels = [label_dict[file.split('/')[-2]] for file in files_val]
        test_labels = [label_dict[file.split('/')[-2]] for file in files_test]

    elif args['group'] == 'binary':
        labels = ['benign', 'malicious']
        label_dict = {t: idx for idx, t in enumerate(labels)}

        train_labels = [0 if 'benign' in file.split('malnet-images-tiny01/')[1].rsplit('/')[-2] else 1 for file in files_train]
        val_labels = [0 if 'benign' in file.split('malnet-images-tiny01/')[1].rsplit('/')[-2] else 1 for file in files_val]
        test_labels = [0 if 'benign' in file.split('malnet-images-tiny01/')[1].rsplit('/')[-2] else 1 for file in files_test]

    else:
        print('Group does not exist')
        exit(1)

    print('Number of train samples: {}, val samples: {}, test samples: {}'.format(len(files_train), len(files_val), len(files_test)))

    return files_train, files_val, files_test, train_labels, val_labels, test_labels, label_dict


def create_image_symlinks(args):
    print('Creating image symlinks')

    files_train, files_val, files_test, _, _, _, _ = get_split_info(args)

    # create symlinks for train/val/test folders
    dst_dir = args['data_dir'] + 'malnet_tiny={}/{}/'.format(args['malnet_tiny'], args['group'])

    for src_path in files_train:
        dst_path = src_path.replace(args['image_dir'], dst_dir + 'train/')

        if args['group'] == 'binary':
            if 'benign' not in dst_path:
                dst_path = dst_path.split('train/')[0] + 'train/malicious/' + dst_path.split('train/')[1].split('/')[2]
            else:
                dst_path = dst_path.split('train/')[0] + 'train/benign/' + dst_path.split('train/')[1].split('/')[2]

        elif args['group'] == 'family':
            dst_path = dst_path.split('train/')[0] + 'train/' + '/'.join(dst_path.split('train/')[1].split('/')[1:3])

        # 1. If the destination directory does not exist, create it
        if not os.path.exists(os.path.dirname(dst_path)):
            os.makedirs(os.path.dirname(dst_path))
        # 2. delete the symlink if it exists
        if os.path.lexists(dst_path):
            os.remove(dst_path)
        # 3. Create symlink
        os.symlink(src_path, dst_path)

    
    for src_path in files_val:
        dst_path = src_path.replace(args['image_dir'], dst_dir + 'val/')

        if args['group'] == 'binary':
            if 'benign' not in dst_path:
                dst_path = dst_path.split('val/')[0] + 'val/malicious/' + dst_path.split('val/')[1].split('/')[2]
            else:
                dst_path = dst_path.split('val/')[0] + 'val/benign/' + dst_path.split('val/')[1].split('/')[2]

        elif args['group'] == 'family':
            dst_path = dst_path.split('val/')[0] + 'val/' + '/'.join(dst_path.split('val/')[1].split('/')[1:3])

        # 1. If the destination directory does not exist, create it
        if not os.path.exists(os.path.dirname(dst_path)):
            os.makedirs(os.path.dirname(dst_path))
        # 2. delete the symlink if it exists
        if os.path.lexists(dst_path):
            os.remove(dst_path)
        # 3. Create symlink
        os.symlink(src_path, dst_path)


    for src_path in files_test:
        dst_path = src_path.replace(args['image_dir'], dst_dir + 'test/')

        if args['group'] == 'binary':
            if 'benign' not in dst_path:
                dst_path = dst_path.split('test/')[0] + 'test/malicious/' + dst_path.split('test/')[1].split('/')[2]
            else:
                dst_path = dst_path.split('test/')[0] + 'test/benign/' + dst_path.split('test/')[1].split('/')[2]

        elif args['group'] == 'family':
            dst_path = dst_path.split('test/')[0] + 'test/' + '/'.join(dst_path.split('test/')[1].split('/')[1:3])

        # 1. If the destination directory does not exist, create it
        if not os.path.exists(os.path.dirname(dst_path)):
            os.makedirs(os.path.dirname(dst_path))
        # 2. delete the symlink if it exists
        if os.path.lexists(dst_path):
            os.remove(dst_path)
        # 3. Create symlink
        os.symlink(src_path, dst_path)


    print('Finished creating symlinks')
