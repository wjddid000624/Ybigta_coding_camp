import torch
from torch.utils.data import Dataset, DataLoader
import os
import json
from PIL import Image
from torchvision import transforms as T

valid_images = [".jpg", ".gif", ".png", ".tga", ".jpeg", ".PNG", ".JPG", ".JPEG"]
with open("./class_info.json", 'r') as f:
    class2id = json.load(f)

class FoodDataset(Dataset):
    def __init__(
        self, 
        root: str, 
        split: str, 
        transforms=None
    ):
        self.root = root
        self.split = split
        self.transforms = transforms
        self.totensor = T.ToTensor()
        self.class2id = class2id
        self.data = self.prepare_dataset()
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        ##################### fill here ####################
        #   TODO: __getitem__을 정의해주세요
        # 1. self.data를 인덱스로 참조해 image path와 class index를 받아온다.
        # 2. image path에 해당하는 image를 받아온다. PIL.Image.open 을 사용할 수 있습니다
        # 3. transform을 적용한다. transform이란 이미지 데이터 증강을 의미합니다. 대부분의 transform은 callable한 object로 제공됩니다. 다른 말로 아래와 같은 간단한 형태로 transform을 적용할 수 있습니다.
        # 이번 과제에서는 torchvision.transforms 에서 제공하는 transform을 사용합니다.
        # 4. tensor로 변환. self.totensor를 이용해 transform을 적용한 이미지를 tensor로 바꿀 수 있습니다.
        # 5. dict 형태로 반환. __getitem__()의 return 값은 dataloader에 의해 batch화 됩니다. readability 를 위해 관습적으로 __getitem__()의 출력은 dict로 구성합니다. 그러면 이후 batch에서도 같은 field로 접근할 수 있습니다.
        ####################################################
        
        image_path, label = self.data[index]
        image = Image.open(image_path)
        if self.transforms:
            image = self.transforms(image)
        image = self.totensor(image)
        label = torch.tensor(label)

        return{
            'image': image,
            'target': label
        }



    def prepare_dataset(self):
        split_base = os.path.join(self.root, self.split)
        data = []
        
        for label in os.listdir(split_base):
            if label not in self.class2id:
                continue
            
            for image_name in os.listdir(os.path.join(split_base, label)):
                if os.path.splitext(image_name)[1] not in valid_images:
                    continue
                data.append((os.path.join(split_base, label, image_name), self.class2id[label]))
        
        return data