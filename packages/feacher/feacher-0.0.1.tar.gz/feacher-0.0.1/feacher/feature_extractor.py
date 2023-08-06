import torch
from feacher import preprocess as ps
from feacher import model as ml

def feature_vector(pretrained_model, image, layer, layer_size, resize_dim):
    model, layer = ml.Model(pretrained_model=pretrained_model, layer=layer)
    input_image = ps.image_preprocess(image, resize_dim)
    feature_vector = torch.zeros(layer_size)

    def flatten(m, i, o):
        feature_vector.copy_(o.flatten())
    h = layer.register_forward_hook(flatten)

    with torch.no_grad():
        model(input_image.unsqueeze(0))
    h.remove()

    return feature_vector
