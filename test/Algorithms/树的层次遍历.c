树的广度优先遍历

层次遍历（用队列实现
①若树非空，则根节点入队
②若队列非空，队头元素出队并访问，同时将该元素的孩子依次入队
③重复②直到队列为空

```c
/**
 * @brief 层次遍历
 *
 * @param root
 */
void levelOrder(treeNode *root) {
// 空树
if (NULL == root) return;

// 创建一个队列保存节点
queue<treeNode *> nodeQueue;
// 将根节点入队
nodeQueue.push(root);

// 队非空时进行访问
while (!nodeQueue.empty()) {
// 取头结点
treeNode *node = nodeQueue.front();
// 访问节点数据
printf("%d ", node->data);
// 左子节点入队
if (node->left) nodeQueue.push(node->left);
// 右子节点入队
if (node->right) nodeQueue.push(node->right);
// 头结点出队
nodeQueue.pop();
}
}
