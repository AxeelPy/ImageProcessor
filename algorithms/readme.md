# IMPORTANT
### If you make an algorithm, there is ALWAYS a ImageProcessor class, and the class has an `assigner` function that runs the image processor
### NEVER make the image processing function to be processed directly. MainWindow will always run `self.algorithm.assigner(self, file)` where `algorithm == ImageProcessor`  