import torch
import torchvision
import yaml

# Download and trace the model.
model = torchvision.models.mobilenet_v2(pretrained=True)
model.eval()
traced_script_module = torch.jit.script(model)

# Save traced TorchScript model.
traced_script_module.save("MobileNetV2.pt")

# Dump root ops used by the model (for custom build optimization).
ops = torch.jit.export_opnames(traced_script_module)
ops.append('aten::ones')  # HACK because predictor.cpp explicitly calls this!
with open('MobileNetV2.yaml', 'w') as output:
    yaml.dump(ops, output)
