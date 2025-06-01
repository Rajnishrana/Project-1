import yaml

def load_config(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    # Debug prints for the loaded config
    print("DEBUG - Config keys:", config.keys())
    print("DEBUG - Training config:", config.get('training'))
    print("DEBUG - Type of training config:", type(config.get('training')))
    print("DEBUG - Training config keys:", config['training'].keys() if 'training' in config else None)
    print("DEBUG - batch_size:", config['training'].get('batch_size') if 'training' in config else None)
    print("DEBUG - learning_rate:", config['training'].get('learning_rate') if 'training' in config else None)
    print("DEBUG - type(batch_size):", type(config['training'].get('batch_size')) if 'training' in config else None)
    print("DEBUG - type(learning_rate):", type(config['training'].get('learning_rate')) if 'training' in config else None)

    return config
