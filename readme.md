Readme
===========
#####同级目录下添加的文件说明
- **gitignore** : xcode 工程忽略文件
- **findUnsedImage.sh** : 找出工程没有用的图片;
     
      1.工程里没有图片名,不一定就没用这个图片;
      2.如图片名是拼接的
      ```
      int i = 0;
      [NSString stringWithFormat:@"image_%d",i]; 
      ```
      3.还有工的启动图片等
- **FinClass.py**: 找出没有引用的类
- ------------------