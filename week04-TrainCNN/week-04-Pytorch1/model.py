import torch
import torch.nn as nn
import torchvision

class vanillaCNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.cv1 = nn.Conv2d(in_channels=3, out_channels=96, kernel_size=11, stride=4)
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.cv2 = nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, padding=2)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.cv3 = nn.Conv2d(in_channels=256, out_channels=384, kernel_size=3, padding=1)
        self.cv4 = nn.Conv2d(in_channels=384, out_channels=384, kernel_size=3, padding=1)
        self.cv5 = nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.relu = nn.ReLU()
        
        self.dropout = nn.Dropout()
        self.head = nn.Linear(in_features=9216, out_features=20)
    
    def forward(self, x):
        #################### fill here #####################
        #   TODO: forward()를 정의해주세요.
        #   cv1 -> relu -> pool1 -> cv2 -> relu -> pool2
        #   -> cv3 -> relu -> cv4 -> relu -> cv5 -> relu -> 
        #   pool3 -> dropout -> head 순서로 거쳐야 합니다.
        ####################################################
        x = self.pool1(self.relu(self.cv1(x)))
        x = self.pool2(self.relu(self.cv2(x)))
        x = self.relu(self.cv3(x))
        x = self.relu(self.cv4(x))
        x = self.pool3(self.relu(self.cv5(x)))
        x = self.dropout(x)
        x = x.view(x.size(0), -1)
        x = self.head(x)
        return x

class vanillaCNN2(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.cv1 = nn.Conv2d(in_channels=3, out_channels=96, kernel_size=11, stride=4)
        self.pool1 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.cv2 = nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, padding=2)
        self.pool2 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.cv3 = nn.Conv2d(in_channels=256, out_channels=384, kernel_size=3, padding=1)
        self.cv4 = nn.Conv2d(in_channels=384, out_channels=384, kernel_size=3, padding=1)
        self.cv5 = nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=3, stride=2)
        self.relu = nn.ReLU()
        
        self.dropout = nn.Dropout()
        ################### fill here #####################
        #   TODO: MLP head (self.head)를 정의해주세요
        ###################################################
        self.head = nn.Sequential(
            nn.Linear(in_features=9216, out_features=4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(in_features=4096, out_features=2048),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(in_features=2048, out_features=20)
        )
    
    def forward(self, x):
        ################### fill here #####################
        #   TODO: forward()를 정의해주세요
        #   vanillaCNN 과 동일하게 사용해도 무방합니다.
        ###################################################
        x = self.pool1(self.relu(self.cv1(x)))
        x = self.pool2(self.relu(self.cv2(x)))
        x = self.relu(self.cv3(x))
        x = self.relu(self.cv4(x))
        x = self.pool3(self.relu(self.cv5(x)))
        x = self.dropout(x)
        x = x.view(x.size(0), -1)
        x = self.head(x)
        return x
    
class VGG19(nn.Module):
    def __init__(self):
        super().__init__()
        
        print("loading Imagenet pretrained VGG19")
        self.vgg = torchvision.models.vgg19(weights='IMAGENET1K_V1', progress=True)
        self.classifier = nn.Sequential(
            nn.Linear(in_features=25088, out_features=4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(in_features=4096, out_features=2048),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(in_features=2048, out_features=20)
        )
        # replace classifier of pretrained VGG-19 with self defined classifier
        setattr(self.vgg, 'classifier', self.classifier)
    
    def forward(self, x):
        return self.vgg(x)