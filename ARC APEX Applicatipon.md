## ARC APEX在神经网络识别数字中的应用
### 1. Introduction
使用神经网络进行数字识别的模型如下图所示。使用的是最简单的BP神经网络，输入为8*8像素的数字图片，二分类输出。可以注意到，在预测阶段，需要的运算有两个：W\*X+B的矩阵乘法和softmax运算。在本文所做工作中，我们集中解决矩阵乘法的加速。易知，如果使用纯C语言实现矩阵乘法需要大量时钟周期，而如果扩展一个APEX指令，则可以在一个时钟周期内得到运算结果，这就是本文的目的。
![](https://i.imgur.com/6ncDTbm.png)

### 2. How to get the images
由于没有找到符合要求的数据集，所以使用python自己生成8*8的数字图片集。程序文件为：generate_imgs.py. 画图所使用的python库为 Python Imaging Library (PIL)。

- 在该程序的开头即定义了图片存放的目录：
```
path_img = "data_pngs/"
```

- 由于一共会产生0-9的数字图片集，所以需要为每个数字建立一个文件夹，程序中的`mkdir_for_imgs`函数就是这个作用，所以当初次生成图片时，首先运行一下该函数。
- 除此以外，函数`del_imgs`的作用是把文件夹中所有的图片删掉。
- 函数`generate_0to9`则是用来生成数字图片的，其用法为`generate_0to9(n)`,n为要产生的图片的总数，例如当n为2000时，产生的0-9的数字图片总数为2000幅，每个数字大概为200幅，但是会有多有少（因为有随机数）。

参考链接：[https://www.cnblogs.com/AdaminXie/p/8379749.html](https://www.cnblogs.com/AdaminXie/p/8379749.html)

### 3. Tensorflow 训练模型
我们采用APEX的核心目的是加速预测阶段的矩阵计算，这是出于现实角度出发，在嵌入式设备中一般都是采用训练好的神经网络模型，直接进行预测阶段。这里我们采用Tensorflow来训练模型。程序文件为：Softmax.py和Softmax\_2\_class.py。前者是10分类的，输出节点为10；后者是2分类，只有两个输出节点，我们目前使用的是Softmax\_2\_class.py。

在该程序的开头，是几个针对数字图片集的接口函数。

- **`ReadImages`函数**：作用是对0-9的每个数字读取出150幅图片，并将其转换为列向量（`array2vector`函数），然后为每幅图片生成标签（labels）。最后返回**打乱顺序**的1500幅图片组成的数据集。

- **`next_batch(train_data, train_target, batch_size)`**：该函数的作用是提供训练时需使用的指定数量的数据集。例如
`batch_xs, batch_ys = next_batch(data_set[0:1000], label_set[0:1000], 100)`
该语句的作用是，从data\_set和label\_set的前1000个中随机选出100个，用来进行本轮训练。

关于Tensorflow模型的建立过程，在此不赘述，参考链接为：[http://www.tensorfly.cn/tfdoc/tutorials/mnist_beginners.html](http://www.tensorfly.cn/tfdoc/tutorials/mnist_beginners.html)

在程序的最后，使用以下语句将神经网络训练好的模型参数保存在了文件中，注意参数是乘以100以后以整数存放的，这是为了方便在verilog中直接使用。

```
np.savetxt("W_2calss_int.txt", w_val*100, fmt="%d", delimiter=",")
```

### 4. 在ARChitect中扩展APEX指令

下面的命令仅限Synopsys内部使用。下面的命令是建立ARChitect工程的命令，其中最后一句包含了一个库叫Demolib2，作者所扩展的所有库均在其中，加速矩阵运算的APEX名为`NN_instruction_assignW`。

    ARChitect2 -argument_file /slowfs/us01dwt2p200/tengjie/ARChitect2_test/release-2.2.0/rel/Configurations/emsk_2p2_em7d.txt \
    -projectpath project_name \
     -libraries /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARC_Debug_v2.1.3.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/release-2.2.0/rel/ip_library \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARC_RDF_CGR_v2.0.6.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARC_RDF_SEIF_v5.0.12.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARC_RDF_SMS_v2.0.2.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARC_RDF_Synopsys_v7.0.11.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARConnect_v2.0.6.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARCv2EM_v3.1.5.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARCv2MSS_v2.0.5.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/ARCv2_FPGA_RDF_v1.2.3.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/ARC_EM_3_1_LIBRARY/tool_configuration_v1.0.51.iplib \
     /slowfs/us01dwt2p200/tengjie/ARChitect2_test/Demolib2


下面还是给出通过APEX Wizard扩展该指令的详细步骤：

1. 指定名字和相应库。
![](https://i.imgur.com/5glyTFz.png)
2. 指定指令的名称，类型，相关寄存器
![](https://i.imgur.com/60lSa9O.png)
3. 编写逻辑代码，该代码的文件名为`uxNN_instruction_assignW.v`，请在该文件中查看详细内容。
![](https://i.imgur.com/nJeWHLN.png)
4. 编写测试代码
![](https://i.imgur.com/ZvJyKG8.png)

5. **要注意修改下相关的时钟频率，如下图所示,时钟主频改为20MHz,JTAG频率改为5MHz**。
	<img src="https://i.imgur.com/Nwtd6Rb.png" width="60%" alt=""/>

6. 最后，在ARChitect工程build之后，进入到工程目录下的build文件夹下，执行`make -f arcsyn.makefile`命令即可自动生成Xilinx的bit文件。我们可以使用`make -f arcsyn.makefile -n`来查看执行了那些命令：
![](https://i.imgur.com/Zxj3gYW.png)
可以看到首先使用synplify_premier命令执行综合，生成edf网表文件；然后将生成的edf文件和约束文件拷贝到fpga文件夹下，并在该文件夹下执行了xflow命令生成最终的bit。

### 5. 测试APEX指令的性能
对比使用纯软件实现与使用APEX实现两种方案所消耗的时钟周期数，来评估APEX加速的效果。

在Metaware中建立工程时需要注意，Toolchains选项选择`ARC EM Generic`一项，在ARChitect-generated Tool Configuration File选择中选`Browse to a TCF file`,相应的tcf文件可以在下面链接中下载到。

[https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp/tree/master/board/emsk/configs/22/tcf](https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_osp/tree/master/board/emsk/configs/22/tcf)

其次，在使用APEX实现时需要一个定义了APEX指令的头文件`apexextensions.h`，该头文件是在ARChitect编译过程中产生的，位于`Project_name/build/tests/common`目录下，可以直接拷贝过来使用。

提供了两个Metaware工程供参考，一个名为2\_class\_8\_8\_7d，另一个为2\_class\_8\_8\_7d\_APEX，显然，前者是纯软件的实现；后者是APEX的实现。

测试结果如下所示：
![](https://i.imgur.com/4Pd9U5L.png)

![](https://i.imgur.com/mlaznZY.png)

### 6. 将ARC CORE与扩展的APEX分开
为了能够让ARC的用户独立探索APEX的应用，同时又不接触到ARC CORE的细节，提出了如下的设计flow。

![](https://i.imgur.com/kg9Gxc1.png)

1. 按照第四大部分所讲述的建立ARChitect工程并扩展好相应的APEX程序，并build工程。
2. 将扩展的APEX的.v文件从Project\_name/build/verilog/RTL中拷贝一份出来，并将Project\_name/build/verilog/RTL中的这份改为black box文件。
3. 使用`synplify_premier -batch ./scripts/sythesis.prj`命令得到core\_chip.edf文件。
4. 在ISE GUI中依次加入core\_chip.edf, core\_chip.ucf, iccm0.bmm, Apex_extension.v四个文件，并依照par\_implement.opt和bitgen.opt两个文件配置ISE布局布线及生成bit过程中的选项。最后生成bit。


### 7. 如何将bit下载到FPGA以及如下下载elf到EMSK
1. Xilinx提供了一个工具可以方便地将bit文件下载到FPGA中：iMPACT。该过程在EMSK的文档“ARC EM Starter Kit Guide”中的Appendix C中有详细的操作步骤，不赘述。
2. 在windows下打开cmd命令行，cd到目标文件夹下，使用`mdb -cl -digilent 2_class_8_8_7d.elf`命令，即可用命令行模式开启Metaware debug。`run`命令可以使程序运行。如果去掉`-cl`则可以打开Metaware debug的GUI模式进行调试。





----------

Written by Tengjie

20/23/2018


