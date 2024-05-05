# Documenting and Analysing Results
## Introduction


## Models and Results

### Model 1.0
[model10.pth](model%2Fmodel10.pth)

- **Parent**: Default
- **Initial Eplison**: 80

Default model was trained for 400 generations.
No changes were made to the model.

#### Results
- **Generations**: 400
- **Average Score**: 24.27
- **Max Score**: 93.0
- **AMTA**: --

![img.png](img.png)

(Graph of Average Moves not working as intended)
[model.pth](model%2Fmodel.pth)

### Model 1.1
[model11.pth](model%2Fmodel11.pth)

1.0 model was trained for 400 generations. With unmodified
model eplison, meaning **greater exploration / exploitation in beggining**


- **Parent**: Model 1.0
- **Initial Eplison**: 80


#### Results
- **Generations**: 400
- **Average Score**: 31.17
- **Max Score**: 101.0
- **AMTA**: 55.64

![img_1.png](img_1.png)


### Model 1.2
[model12.pth](model%2Fmodel12.pth)

- **Parent**: Model 1.0
- **Initial Eplison**: 10

1.0 model was trained for 400 generations. With modified
model eplison, meaning **fewer exploration / exploitation in beggining**

#### Results
- **Generations**: 400
- **Average Score**: 38.72
- **Max Score**: 97.0
- **AMTA**: 47.55
![img_2.png](img_2.png)


### Model 1.3

![img_3.png](img_3.png)