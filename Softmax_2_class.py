#import input_data # 调用input_data
#mnist = input_data.read_data_sets('data/', one_hot=True)
import tensorflow as tf
import numpy as np
from PIL import Image
import os

def ReadImages():
    #print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    data_set = []
    label_set = []
    data_set_disordered = []
    label_set_disordered = []
    for i in range(10):
        DIR = 'C:/STJ/Deep_Learning/Generate_handwritten_number-master/data_pngs/'
        DIR = DIR + "Num_" + str(i) + "/" + str(i) + "_"
        for j in range(150):
            im = Image.open(DIR + str(j+1) + ".png")
            im2 = np.array(im)
            im2_1 = array2vector(im2)
            label = [0, 0]
            if i<5:
                label[0] = 1
            else:
                label[1] = 1
            data_set.append(im2_1)
            label_set.append(label)
    index = [ k for k in range(1500) ]  
    np.random.shuffle(index);
    for m in range(1500):
        data_set_disordered.append(data_set[index[m]])
        label_set_disordered.append(label_set[index[m]])
    return data_set_disordered, label_set_disordered

            
def array2vector (a2):
    returnVect = np.zeros(64)
    for i in range (8):
        for j in range (8):
            returnVect[8*i+j] = 1 - a2[i][j]
    return returnVect

def next_batch(train_data, train_target, batch_size):  
    index = [ i for i in range(0,len(train_target)) ]  
    np.random.shuffle(index);  
    batch_data = []; 
    batch_target = [];  
    for i in range(0,batch_size):  
        batch_data.append(train_data[index[i]]);  
        batch_target.append(train_target[index[i]])  
    return batch_data, batch_target

x = tf.placeholder("float", [None, 64])
y_ = tf.placeholder("float", [None, 2])  
w = tf.Variable(tf.zeros([64, 2]))
b = tf.Variable(tf.zeros([2]))

y = tf.nn.softmax(tf.matmul(x,w) + b)
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.global_variables_initializer()

sess = tf.Session()

sess.run(init)

data_set, label_set = ReadImages()

for i in range(1000):
    batch_xs, batch_ys = next_batch(data_set[0:1000], label_set[0:1000], 100)
    ts, w_val, b_val = sess.run([train_step, w, b], feed_dict={x:batch_xs, y_:batch_ys})

correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

test_xs, test_ys = next_batch(data_set[1001:1500], label_set[1001:1500], 300)

##如果修改了下面这个，那么准确率就是0.9，说明这个模型没问题
##test_xs[0] = [1., 1., 1., 0., 0., 0., 1., 0., 0., 1., 0., 0., 1., 1., 0., 0., 0.,
##       1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 1., 1.,
##       0., 0., 1., 0., 1., 0., 0., 0., 0., 1., 0., 0., 1., 1., 0., 0., 0.,
##       0., 0., 0., 0., 1., 0., 0., 1., 0., 0., 1., 1., 0.]
##test_ys[0] = [0, 0]

print (sess.run(accuracy, feed_dict={x: test_xs, y_: test_ys}))
##np.savetxt("W_2calss_int.txt", w_val*100, fmt="%d", delimiter=",", newline=",")
##np.savetxt("b_2class_int.txt", b_val*100, fmt="%d", delimiter=",", newline=",")

np.savetxt("W_2calss_int.txt", w_val*100, fmt="%d", delimiter=",")
np.savetxt("b_2class_int.txt", b_val*100, fmt="%d", delimiter=",")

#test_x, test_y = next_batch(data_set[1001:1500], label_set[1001:1500], 20)
#for i in range(20):
#	test_x[i] = test_x[i].astype(np.int16)
        
