# MdOutline

Md 结构解析工具已经完成！

## Output

### Todo List

#### MdTodoList

生成 Markdown 格式的 Todo List

### Mindmap

#### Xmind

方案基本敲定，准备开发，不过目前可以使用 opml 文件直接导入，支持的比较完美！

这里没有使用现有库 md2xmind 因为其识别的结果问题很大，
比如如果一级标题在更低级标题下面，那么识别会出现大错误，
因此我直接弃用了这个方案用自己解析器解析结果来生成！

#### freemind

目前仅支持标题生成导图，内部内容等待 HTML 功能完成后！

### OPML

目前生成的 OPML 文件仅支持 xmind 导入！

MindManager 界面我也挺喜欢的，但是用户比较少，而且格式比较复杂，至少很长一段时间不会去适配！

### HTML

还没有完成，完成后，就进行 freemind 内容开发。

## 等待评估

- [ ] OmniOutliner
- [ ] iThoughts
- [ ] DEVONthink
- [ ] Anki

以及一些其他的 macOS 平台应用
