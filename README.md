**这个文件的主要作用是介绍我在us01上各个文件的作用。**

1. 我所使用的各软件版本如下：
	<img src="https://i.imgur.com/qDEUcOx.png" width="200%" alt=""/>


2. 项目所在目录： /slowfs/us01dwt2p200/tengjie/APEX\_DEEP\_LEARNING
3. APEX\_ARC\_gene\_7d\_clk20\_assignW： ARChitect工程，在该工程中直接采用xflow来生成最后的bit文件，是一个过渡用的工程。
4. APEX\_ARC\_gene\_7d\_clk20\_assignW\_empty：ARChitect工程，在该工程中将扩展的Apex\_extension.v修改为了黑盒子，使用Synplify\_premier综合得到了core\_chip.edf。
5. xst\_uxNN: Xilinx工程，工程文件只有一个，就是包含用户逻辑的真正的Apex\_extension.v，在该工程中只进行了综合操作，得到xilinx的网表文件Apex\_extension.ngc。Apex\_extension.ngc与core\_chip.edf将融合得到最后的设计文件。
6. edf\_merge\_scripts：Xilinx工程，用来将Apex\_extension.ngc与core\_chip.edf两个设计网表融合，并执行映射，布局布线等流程得到最终的bit文件。**注意，上面的这些流程是使用命令行模式执行的，xst\_flow文件存放这所有的这些命令。**