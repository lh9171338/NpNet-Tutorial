import numpy as np
import matplotlib.pyplot as plt

import npnet


np.random.seed(1)
x0 = np.random.normal(-2, 1, (100, 2))
x1 = np.random.normal(2, 1, (100, 2))
y0 = np.zeros((100, 1), dtype=np.int32)
y1 = np.ones((100, 1), dtype=np.int32)
x = np.concatenate((x0, x1), axis=0)
y = np.concatenate((y0, y1), axis=0)


class Net(npnet.Module):
    def __init__(self):
        super().__init__()
        w_init = npnet.init.RandomUniform()
        b_init = npnet.init.Constant(0.1)

        self.l1 = npnet.layers.Dense(2, 10, npnet.act.tanh, w_init, b_init)
        self.l2 = npnet.layers.Dense(10, 10, npnet.act.tanh, w_init, b_init)
        self.out = npnet.layers.Dense(10, 1, npnet.act.sigmoid)

    def forward(self, x):
        x = self.l1(x)
        x = self.l2(x)
        o = self.out(x)
        return o


net = Net()
opt = npnet.optim.Adam(net.params, lr=0.1)
loss_fn = npnet.losses.SigmoidCrossEntropy()

for step in range(30):
    o = net.forward(x)
    loss = loss_fn(o, y)
    net.backward(loss)
    opt.step()
    acc = npnet.metrics.accuracy(o.data > 0.5, y)
    print("Step: %i | loss: %.5f | acc: %.2f" % (step, loss.data, acc))

    if step % 1 == 0:
        plt.figure()
        plt.scatter(x[:, 0], x[:, 1], c=(o.data > 0.5).ravel(), s=100, lw=0, cmap='RdYlGn')
        plt.show()
        plt.close()

print(net.forward(x[:10]).data.ravel(), "\n", y[:10].ravel())
