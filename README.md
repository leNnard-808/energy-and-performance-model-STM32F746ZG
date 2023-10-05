# Energy and performance model of Neural Networks for TinyML systems

This repository serves to provide the automation scripts to ultimately create an energy and performance model.
The scripts include subjective paths, hence, prior to usage, ensure that they are tailored specifically for your application.
For further and more detailed instructions, please refer to the thesis itself.


### Performance (ms) model for CNNs for the Nucleo-144 STM32F746ZG board at 70MHz:

$$\mathrm{performance} = (-164.33 + 0.0049x_1+ 89.83x_2 + 0.043x_3 - 43.30x_4 + 0.0046x_5)$$


### Energy (mWs) model for CNNs for the Nucleo-144 STM32F746ZG board at 70MHz:
$$\mathrm{energy} = (-164.33 + 0.0049x_1+ 89.83x_2 + 0.043x_3 - 43.30x_4 + 0.0046x_5) \cdot 0.7W$$

The variable $x_1$ represents the sum of convolutional layer MACs, $x_2$ the number of convolutional layers, $x_3$ the sum of maxpooling layer MACs, $x_4$ the amount of maxpooling layers, and $x_5$ the MACs of the fully-connected layer.


#### Disclaimer:
The *build_custom_model* function in the *model_creation.py* script contains an additional return argument containing the model string. This is then added to the dataset so that each row in the dataset can be identified.
Furthermore, some variables may be named slightly differently, as there have been many iterations of the script before writing the thesis.
