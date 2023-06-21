<?xml version='1.0' encoding='utf-8'?>
<map version="1.0.1">
	<node CREATED="1687362736233" ID="98828719-104b-11ee-ae73-34c93d029fa3" MODIFIED="1687362736233" TEXT=" 树.md">
		<node CREATED="1687362736233" ID="9882871a-104b-11ee-a386-34c93d029fa3" MODIFIED="1687362736233" TEXT="1 树">
			<node CREATED="1687362736233" ID="9882871b-104b-11ee-8ef6-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.1 &quot;概念？&quot; '概念！'">
				<richcontent TYPE="NOTE">
					<head />
					<body>
						<p>这个是用来测试引号用的！</p>
					</body>
				</richcontent>
			</node>
			<node CREATED="1687362736233" ID="9882d4fd-104b-11ee-80a7-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.2 概念">
				<node CREATED="1687362736233" ID="9882d4fe-104b-11ee-b4aa-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.2.1 树、有序树、二叉树区别">
					<richcontent TYPE="NOTE">
						<head />
						<body>
							<p>
								每个结点至多有两棵子树的
								<strong>有序树</strong>
								<strong> 并不是</strong>
								<strong>二叉树</strong>
							</p>
						</body>
					</richcontent>
					<node CREATED="1687362736233" ID="9882d4ff-104b-11ee-8365-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.2.1.1 树">
						<richcontent TYPE="NOTE">
							<head />
							<body>
								<p>树是个结点的有限集，结点的孩子没有左右之分。</p>
							</body>
						</richcontent>
					</node>
					<node CREATED="1687362736233" ID="9882d500-104b-11ee-bef4-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.2.1.2 有序树">
						<richcontent TYPE="NOTE">
							<head />
							<body>
								<p>有序树的孩子的左右子树的次序是相对于另一个孩子而言的，若某个结点只有一个孩子，则这个孩子就无须区分左右次序。</p>
							</body>
						</richcontent>
					</node>
					<node CREATED="1687362736233" ID="9882d501-104b-11ee-b1e4-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.2.1.3 二叉树">
						<richcontent TYPE="NOTE">
							<head />
							<body>
								<p>二叉树是一种树形结构，且二叉树是有序树，其主要特征是每个节点至多只能有两棵子树，
并且二叉树的子树有左右之分，其次序不能颠倒，
且无论二叉树其孩子数是否为2，均需确定其左右孩子次序，
即二叉树的结点次序不是相对于另一结点而言的。</p>
							</body>
						</richcontent>
					</node>
				</node>
				<node CREATED="1687362736233" ID="9882fbfb-104b-11ee-b293-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.2.2 某个结点祖先">
					<richcontent TYPE="NOTE">
						<head />
						<body>
							<p>某个结点上面的所有结点根节点</p>
						</body>
					</richcontent>
				</node>
			</node>
			<node CREATED="1687362736233" ID="9882fbfc-104b-11ee-a084-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.3 树的存储结构">
				<richcontent TYPE="NOTE">
					<head />
					<body>
						<p>
							树的存储结构有
							<strong>双亲表示法</strong>
							<strong>孩子表示法</strong>
							<strong>孩子兄弟表示法</strong>
						</p>
					</body>
				</richcontent>
				<node CREATED="1687362736233" ID="9882fbfd-104b-11ee-9c0d-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.3.1 孩子兄弟表示法(二叉链表)">
					<richcontent TYPE="NOTE">
						<head />
						<body>
							<p>左孩子右兄弟
根节点后面没有右子树(不是森林)</p>
							<p>
								<code>C
typedef struct CSNode{
    ElemType data;
    struct CSNode *firstchild, *nextsibling;
}CSNode, *CSTree;</code>
							</p>
							<p>这种表示法，对孩子兄弟表示法的先序遍历等于原树的先序遍历，对孩子兄弟表示法二叉链表的中序遍历等于原树的后序遍历</p>
							<p>先-&gt;先
中-&gt;后</p>
						</body>
					</richcontent>
				</node>
				<node CREATED="1687362736233" ID="988322ed-104b-11ee-90be-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.3.2 资料">
					<richcontent TYPE="NOTE">
						<head />
						<body>
							<p>https://www.bilibili.com/video/BV1Dg411G7xt</p>
						</body>
					</richcontent>
				</node>
			</node>
			<node CREATED="1687362736233" ID="988322ee-104b-11ee-b003-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.4 树的遍历">
				<node CREATED="1687362736233" ID="988322ef-104b-11ee-a7a1-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.4.1 树的层次遍历">
					<richcontent TYPE="NOTE">
						<head />
						<body>
							<p>树的广度优先遍历</p>
							<p>层次遍历（用队列实现
①若树非空，则根节点入队
②若队列非空，队头元素出队并访问，同时将该元素的孩子依次入队
③重复②直到队列为空</p>
							<p>
								```c
/
								<em>
									<em>
 * @brief 层次遍历
 *
 * @param root
 </em>
								</em>
							</p>
							<p>queue&lt;treeNode *&gt; nodeQueue;  // 创建一个队列保存节点
nodeQueue.push(root);         // 将根节点入队</p>
							<p>// 队非空时进行访问
while (!nodeQueue.empty()) {
treeNode *node = nodeQueue.front();            // 取头结点
printf("%d ", node-&gt;data);                     // 访问节点数据
if (node-&gt;left) nodeQueue.push(node-&gt;left);    // 左子节点入队
if (node-&gt;right) nodeQueue.push(node-&gt;right);  // 右子节点入队
nodeQueue.pop();                               // 头结点出队
}
}
```</p>
						</body>
					</richcontent>
				</node>
				<node CREATED="1687362736233" ID="988349e6-104b-11ee-a9fe-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.4.2 特殊的遍历序列">
					<node CREATED="1687362736233" ID="988349e7-104b-11ee-a3c9-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.4.2.1 后序遍历序列与中序遍历序列">
						<richcontent TYPE="NOTE">
							<head />
							<body>
								<p>二叉树在没有右子树的情况下，二叉树的中序和后序序列是相同的。</p>
								<p>分析如下：</p>
								<p>二叉树的中序序列为：左子树、根、右子树；二叉树的后序序列为：左子树、右子树、根；要想使二叉树的中序和后序序列相同，则只有两种情况可以满足：</p>
								<p>1、没有根的二叉树，然而根据二叉树的性质可知，所有的二叉树都有有根节点的，因此此项不满足；</p>
								<p>2、没有右子树的二叉树，只有左子树的二叉树，这样二叉树的中序和后序序列都为：左子树、根是满足情况的。</p>
							</body>
						</richcontent>
					</node>
					<node CREATED="1687362736233" ID="988349e8-104b-11ee-91ac-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.4.2.2 先序遍历序列与中序遍历序列相同">
						<richcontent TYPE="NOTE">
							<head />
							<body>
								<p>只有根结点的二叉树或非叶子结点只有右子树的二叉树</p>
							</body>
						</richcontent>
					</node>
				</node>
			</node>
			<node CREATED="1687362736233" ID="988349e9-104b-11ee-be9c-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.5 m叉树">
				<richcontent TYPE="NOTE">
					<head />
					<body>
						<p>设一颗m叉树中度为0的节点数为$N_0$，度数为1的节点数为$N_1$，...，度数为m的节点数为$N_m$，则$N_0=1+N_2+2N_3+3N_4+...+(m-1)N_m$</p>
						<p>
							<a href="https://www.nowcoder.com/questionTerminal/0572ff24ecaf425ba9db2b560c24caab%E2%80%B8">牛客网</a>
						</p>
						<p>要注意树中度数（又为边数、指针数）、结点数与叶子结点数之间的关系。</p>
						<p>在这里，总结点数：N₀+N₁+N₂+N₃......Nм</p>
						<p>总度数为：N₁+2N₂+3N₃......mNм;</p>
						<p>总结点数=总度数+1</p>
						<p>※很重要※
N₀+N₁+N₂+N₃......Nм = N₁+2N₂+3N₃......mNм + 1</p>
						<p>度数加一为总节点个数</p>
						<p>N₀ = 1 + N₂ + 2N₃ + (m-1)Nm</p>
						<p>
							设一棵 m 叉树 的结点数为 n ，用多重链表表示其存储结构，则该树中有
							<strong>$mn-(n-1)$</strong>
						</p>
						<p>一棵 m 叉树的结点数为 n，指针域共mn，n结点除根节点外都有一个指针指向，空指针域:mn-(n-1)</p>
					</body>
				</richcontent>
			</node>
			<node CREATED="1687362736233" ID="988370e0-104b-11ee-9350-34c93d029fa3" MODIFIED="1687362736233" TEXT="1.6 典型题">
				<richcontent TYPE="NOTE">
					<head />
					<body>
						<p>设F是一个森林，B是由F变换得的二叉树。若F中有n个非终端结点，则B中右指针域为空的结点有多少个？
https://blog.csdn.net/l_jd_gululu/article/details/105530290</p>
						<p>空树是指树中没有结点的树，空树的度为0，空树的结点数为0，空树的叶子结点数为0。</p>
						<p>最小的树是指只有一个根结点的树，最小的树的度为0，最小的树的结点数为1，最小的树的叶子结点数为1。</p>
						<p>度为2的树与二叉树的区别：
一棵度为 2 的有序树与一棵二叉树的区别是:度为 2 的树有两个分支,没有左右之分;
一棵二叉树也有两个分支,但有左右之分,且左右不能交换.
度为2的树的结点数至少为3，二叉树的结点数至少为2。</p>
						<p>
							画出有3个节点的树和有3个结点的二叉树的所有不同的形态
							<img alt="3个节点的树和二叉树" src="img/3nodetree.png" title="3个节点的树和二叉树" />
						</p>
						<p>
							<img alt="" src="img/3nodetree.png" />
						</p>
						<p>
							满足以下条件的二叉树：
（1）先序序列和中序序列相同的二叉树为：
							<strong>空树</strong>
							<strong>空树</strong>
							<strong>空树</strong>
						</p>
						<p>
							不要忘记
							<strong>空树</strong>
						</p>
						<p>设F是一个森林，B是由F转换得到的二叉树，F中有n个非终端结点，则B中右指针域为空的结点有n+1个
每个非终端结点，其所有孩子结点在转换之后，最后一个孩子的右指针也为空
只要是非终端结点，那就有孩子
肯定有一个右指针域为空
再加个根节点右指针域为空
这里考虑一棵树，多棵树的话还得考虑剩下的树
怎么简单怎么考虑</p>
						<p>假设在一棵二叉树中，度为2的结点数为15，度为1的结点数为10个，则该二叉树的分支总数为40个
$n_0=1+n_2=16$
15+16+10=41
而根节点没有爹，分之总数可以理解为有爹的结点
41-1=40为分支总数</p>
						<p>一颗二叉树的高度为h，所有结点的度为0或2，则这颗二叉树最少有2h-1个结点
左子树有俩孩子，右子树没孩子</p>
						<p>
							序遍历的第一个/最后一个结点问题
若一个二叉树的
							<strong>树叶</strong>
							<strong>中序遍历序列中的第一个</strong>
							<strong>必是</strong>
							<strong>后序遍历序列中的第一个</strong>
						</p>
						<p>中 左中右
后 左右中</p>
						<p>如果没有限制树叶，那么参考“入”字，的根节点，没有左子树，但是他限制了树叶，所以没有问题</p>
						<p>若一个叶子结点是某子树的中序遍历序列的最后一个结点，则它必是孩子树的先序遍历中的最后一个结点。这种说法是否正确？
一个结点是某子树的中序遍历序列的最后一个结点，则它必是孩子树的先序遍历中的最后一个结点，这句话就是错的，
因为该结点可能只有左子树没有右子树，
但题目中强调了叶子结点，那就对了
叶子结点是中序遍历的最后一个结点，则必定是右子树右下角的结点。则也必为先序遍历的最后一个结点。</p>
						<p>设一棵m叉树的结点数为n，用多重链表表示其存储结构，则该树中有多少个空指针域？
总的这个指针域m*n，减去非空的数目(注意非根节点的父节点都会消耗一个指针域来指向它，总共n-1个)，所以减一下就是答案</p>
					</body>
				</richcontent>
			</node>
		</node>
		<node CREATED="1687362736233" ID="98839a69-104b-11ee-89bc-34c93d029fa3" MODIFIED="1687362736233" TEXT="2 图" />
		<node CREATED="1687362736233" ID="98839a6a-104b-11ee-ac4d-34c93d029fa3" MODIFIED="1687362736233" TEXT="3 搜索" />
		<node CREATED="1687362736233" ID="98839a6b-104b-11ee-b4d5-34c93d029fa3" MODIFIED="1687362736233" TEXT="4 排序" />
	</node>
</map>