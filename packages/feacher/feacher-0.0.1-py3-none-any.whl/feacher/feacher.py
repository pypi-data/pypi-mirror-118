from feacher import feature_extractor as fe
from feacher import dataloader as dl

def extract(path, pretrained_model, layer, layer_size, resize_dim):

    images = dl.DataLoader(path)
    image_features = []
    for image in images:
        extracted_features = fe.feature_vector(pretrained_model, image, layer, layer_size, resize_dim)
        image_features.append(extracted_features)

    return image_features