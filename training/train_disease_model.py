"""Fine-tune MobileNetV2 for plant-disease classification.

Expects an ImageFolder layout:
    <data-dir>/train/<class_name>/*.jpg
    <data-dir>/val/<class_name>/*.jpg

Writes plant_disease_model.pth *and* class_names.json (the label order the
model was trained with) to the output directory.

Usage:
    python training/train_disease_model.py --data-dir data/dataset_split --epochs 5
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "dataset_split")
    parser.add_argument("--out", type=Path, default=ROOT / "models")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    args = parser.parse_args()

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    train_ds = datasets.ImageFolder(args.data_dir / "train", transform=transform)
    val_ds = datasets.ImageFolder(args.data_dir / "val", transform=transform)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
    for param in model.features.parameters():
        param.requires_grad = False
    model.classifier = nn.Sequential(
        nn.Dropout(0.2), nn.Linear(model.last_channel, len(train_ds.classes))
    )
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=args.lr)

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch}/{args.epochs}", leave=False):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        model.eval()
        correct = total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                correct += (model(images).argmax(1) == labels).sum().item()
                total += labels.size(0)
        print(f"Epoch {epoch}: loss={total_loss:.2f}  val_acc={100 * correct / total:.2f}%")

    args.out.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), args.out / "plant_disease_model.pth")
    (args.out / "class_names.json").write_text(json.dumps(train_ds.classes, indent=2), encoding="utf-8")
    print(f"Saved weights + class_names.json to {args.out}")


if __name__ == "__main__":
    main()
