import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def pad_image(image, target_size=(224, 224)):
    old_size = image.size  
    ratio = min(target_size[0] / old_size[0], target_size[1] / old_size[1])
    new_size = (int(old_size[0] * ratio), int(old_size[1] * ratio))

    image = image.resize(new_size, Image.Resampling.LANCZOS)
    new_image = Image.new("RGB", target_size, (255, 255, 255))
    new_image.paste(image, ((target_size[0] - new_size[0]) // 2, (target_size[1] - new_size[1]) // 2))

    return new_image

transform = transforms.Compose([
    transforms.Lambda(lambda img: pad_image(img, (224, 224))),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

label_map = {
    0: "0-degree",
    1: "180-degree",
    2: "270-degree",
    3: "90-degree"
}

class OrientationClassifier(nn.Module):
    def __init__(self):
        super(OrientationClassifier, self).__init__()
        self.model = models.resnet18(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, 4)

    def forward(self, x):
        return self.model(x)

def load_model(model_path="orientation_classifier.pt"):
    model = OrientationClassifier()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

def predict_orientation(image_path, model_path="orientation_classifier.pt"):
    model = load_model(model_path)

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)

    label = label_map[predicted.item()]
    print(f"Predicted Orientation: {label}, Confidence: {confidence.item()*100:.2f}%")
    return label

image_path = "test_png/270_A032100242 Executed batch record Compound 29A_63.png" 
model_path = "orientation_classifier.pt"
predict_orientation(image_path, model_path)
