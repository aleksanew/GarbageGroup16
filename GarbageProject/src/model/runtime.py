from pathlib import Path
import yaml
import numpy as np
from dataclasses import dataclass

@dataclass
class Detection:
    bbox: list[int] | None
    class_id: int
    score: float
# Dataholder for en prediction
# bbox er [x1, y1, x2, y2] med piksler
# class_id er index i labels
# score er confidence 0-1

class TrashNet:
    def __init__(self, weights: str|None, labels: str):
        self.weights = Path(weights) if weights else None
        with open(labels) as f:
            self.labels = yaml.safe_load(f)['names']
        self.model = self._load_model()

# Kaller _load_model for å bygge neural net og laste paremetre
# model er TinyCNN
# weights er path til trent modell vekter
# labels er path til yaml fil med labels


    def _load_model(self):
        try:
            import torch, torch.nn as nn
        except Exception as e:
            self._torch_error = e
            return None
# importerer PyTorch
# hvis det feiler lagres feilen i self._torch_error og None returneres


        class TinyCNN(nn.Module):
            def __init__(self, n_classes):
                super().__init__()
                # Bygger et lite convolutional neural network
                # n_classes er antall søppeltyper
                
                self.features = nn.Sequential(
                    nn.Conv2d(3, 16, 3, 2, 1), nn.ReLU(),
                    # Conv lag, 3 kanaler (RGB), 16 feature maps, kernel 3x3, stride 2(nedskalering), padding 1(samme størrelse)
                    # Relu aktivering legger til ikke-linearitet
                    nn.Conv2d(16, 32, 3, 2, 1), nn.ReLU(),
                    # Conv lag, 16 kanaler, 32 feature maps, kernel 3x3, stride 2, padding 1
                    # Relu aktivering for å lære mer komplekse mønstre
                    nn.AdaptiveAvgPool2d(1),
                    # Pooling: gjennomsnitt av hver feature map til én verdi
                    # Output blir (batch_size, 32, 1, 1)
                )
                self.head = nn.Linear(32, n_classes)
                # Fullt koblet lag for klassifisering
                # Tar 32 input features (fra conv lag) og gir n_classes score (sannsynligheter for hver klasse)

            def forward(self, x):
                # Definerer fremover-passering gjennom nettverket
                x = self.features(x) # CNN + pooling
                x = x.flatten(1) # Flater ut til (batch_size, 32)
                return self.head(x) # Prediksjoner for alle klasser

        n = len(self.labels)
        model = TinyCNN(n)
        # Bygger TinyCNN

        if self.weights and self.weights.exists():
            sd = torch.load(self.weights, map_location='cpu') # Laster vekter fra fuk
            model.load_state_dict(sd, strict=False) # Laster vekter i modellen
        model.eval()
        # Setter modellen i evalueringsmodus (ingen dropout, batchnorm i eval modus)
        return model


class Detector:
    def __init__(self, weights: str|None, labels: str):
        self.net = TrashNet(weights, labels)
