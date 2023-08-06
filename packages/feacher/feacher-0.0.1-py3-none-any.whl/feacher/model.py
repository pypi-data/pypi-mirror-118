import torchvision.models as models

def Model(pretrained_model, layer):
    model = getattr(models, '%s' %pretrained_model)(pretrained=True)
    layer = model._modules.get('%s' %layer)
    
    # Set the model to Evaluation mode
    model.eval()
    
    return (model, layer)