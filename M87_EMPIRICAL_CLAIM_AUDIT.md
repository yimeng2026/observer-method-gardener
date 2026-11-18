# M87 黑洞“宇宙级实证”及关联生成材料专项复核

**审查对象**：2025-11-23 发布的 M87 主题帖，归档编号 `10238581618`。

**范围**：53 张本地图片全部实读，两页公开评论归档审阅；另核对 PSR J0348+0432 和地面引力波探测器公开基线。公开仓库只保存编号、方法摘要、数值复核和哈希，不公开原帖全文、原始图片、头像或账号资料。

**结论**：材料没有提供可核验的 M87 原始观测、拟合、仪器数据或真实超算运行记录，不能登记为 M87 的“宇宙级实证”。评论中还明确出现“上面都是虚拟数据”“虚拟的，半真半假”的自我说明，故生成文本不能被反向引用为真实观测。保留这一披露，以及少量可加总、量纲闭合或饱和极限算术；撤回所有由生成叙事产生的官方认可、个人测量、政治背书和财富结论。[10238581618](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/posts/10238581618.json "citation"), 第 9、17 楼“上面都是虚拟数据，别太当真。”“虚拟的，半真半假。”

## 一、先固定对象与证据类型

本帖至少混合了四类对象：M87*、3C 273、PSR J0348+0432，以及十一维／超膜扩展。它们的观测量、参数和证据不能相互代替。帖内还穿插出版计划、人物评价、健康与智商描述、政治经济想象；这些不进入天体物理实证栏。

复算入口：`checks/m87_evidence_claim_checks.py`。下列“通过”仅指局部算术或量纲检查，不证明相应物理机制。

## 二、关键公式与数值复核

### 1. 特征尺度：数值放大可以由一个因子写出，但没有完成内生推导

图示形式

\[
 \lambda_c=\sqrt{\frac{\hbar G}{\pi c^3}}\frac1{\Xi(\Lambda_g)}
\]

的前置长度为 \(9.118742488572175\times10^{-36}\,\mathrm m\)。要得到同系列 \(\lambda_c=5.99153\times10^{-13}\,\mathrm m\)，必须有

\[
 \Xi(\Lambda_g)=1.521938885154906\times10^{-23},
 \qquad \frac{\lambda_c}{9.118742488572175\times10^{-36}\,\mathrm m}
 =6.570566070386052\times10^{22}.
\]

这本身只是反解屏蔽因子，不是从拓扑导出它。更重要的是量纲约定尚未冻结：若积分中的 \(R\) 是半径，\(\Xi\) 具有长度平方量纲，整个右式就不是长度；若 \(R\) 是曲率标量，则需要另外的归一化和量纲定义。没有无量纲屏蔽因子及其独立计算，就不能宣称两个基本常数已经内生产生该尺度。[01](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/01.jpg "citation"), [06](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/06.jpg "citation")

### 2. 喷流功率：恢复电磁单位后仍不是功率

图示

\[
 P_{\rm jet}=\kappa\frac{B^2R_s^2c}{\lambda_c^2}\sin^2\theta_m .
\]

在 SI 中，\(B^2/\mu_0\) 是能量密度。恢复 \(\mu_0\) 后，该式给出

\[
 \frac{B^2R_s^2c}{\mu_0\lambda_c^2}
 \quad\Longrightarrow\quad \mathrm{W/m^2},
\]

而不是 \(\mathrm W\)。即它仍缺少一个面积量纲的因子；不能通过把 \(\kappa\) 称为“无量纲效率”消除这个矛盾。修正量纲后仍需给出磁通、黑洞自旋、视界面积、吸积边界及 MHD 基线，才可与实际喷流功率比较。本帖未提供这些闭环，更未展示“理论曲线与观测完美重叠”的原始数据。[03](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/03.jpg "citation"), [07](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/07.jpg "citation")

### 3. 熵与核心能量：局部量纲可保留，信息问题没有因此解决

在 \(k_B=1\) 的单位中，

\[
 S=\frac{A}{4l_p^2}\frac{\theta_m}{\pi}
\]

是无量纲的；再乘 \(\hbar c/\lambda_c\) 可得能量量纲。因此**这部分形式检查可以保留**。但乘一个角度因子并不自动给出 Page 曲线、信息恢复机制或黑洞蒸发幺正性，也不构成 M87 观测验证。后续所谓“信息悖论解决”仍缺独立动力学和观测接口。[02](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/02.jpg "citation"), [03](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/03.jpg "citation")

### 4. 抽取效率：巨大尺度比使公式饱和，不是拟合出 41.7%

图示

\[
 \epsilon=\frac12\left[1-\exp\left(-\frac{\theta_m}{\pi}\frac{R_s}{\lambda_c}\right)\right].
\]

仅作数量级示例，取 \(M=6.5\times10^9M_\odot\) 计算 Schwarzschild 半径，得到 \(R_s=1.919670598343471\times10^{13}\,\mathrm m\)，指数为 \(1.588625903825782\times10^{25}\)，于是 \(\epsilon=0.5\)。这只是公式的饱和极限，不是独立拟合，更不能拿来替代另一对象 3C 273 所列的 \(\eta_\theta=0.417\)。示例质量不是本报告重新测量的 M87 质量。[14](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/14.jpg "citation"), [17](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/17.jpg "citation"), [18](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/18.jpg "citation")

### 5. 湍流粘滞系数：缺少衰减时标，39 ms 代入不支持所印结果

图示

\[
 \nu_{\rm turb}=\frac{\lambda_c^2}{\tau_{\rm decay}}
 \frac1{\sqrt{1-\frac23\sin^2\theta_m}} .
\]

图片随后给出自转周期 \(P\approx39\,\mathrm{ms}\)，但没有给出 \(\tau_{\rm decay}\) 的测量或推导。若仅为检验而取 \(\tau_{\rm decay}=0.039\,\mathrm s\)，得到

\[
 \nu_{\rm turb}=1.594031773938694\times10^{-19}\,\mathrm{cm^2/s},
\]

不是 \(1.2\times10^{12}\,\mathrm{cm^2/s}\)，所印值是该结果的 \(7.528080805032635\times10^{30}\) 倍。反解所印值需要 \(\tau_{\rm decay}=5.180603265300755\times10^{-33}\,\mathrm s\)，这一时标没有来源。故所印数值、“比传统 MHD 低两个量级”及“独立证据”均未获支持；若作者另有时标定义，必须先公开再复算。[21](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/21.jpg "citation"), [22](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/22.jpg "citation")

### 6. PSR J0348+0432：磁场输入和 EOS 绝对命题均需更正

公开论文表中的自转周期约为 \(39.1226562801558\,\mathrm{ms}\)，与图中 39 ms 基本一致；但横向极区磁场估值为 \(3.11\times10^9\,\mathrm G\)，并非图中 \(10^{13}\,\mathrm G\)，相差约 3215.43 倍。[Saffer 等，arXiv:2412.02850](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2412.02850v1&text=Transverse%20Magnetic%20Field%20at%20Poles%20%5BG%5D "citation"), [22](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/22.jpg "citation")

2013 年研究报告 \(2.01\pm0.04\,M_\odot\)，并把它作为致密物质与强场引力的观测约束，而不是宣布所有已知状态方程失效。[Antoniadis 等，arXiv:1304.6875](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F1304.6875&text=Thus%20far%2C%20the%20observed%20orbital%20decay%20agrees%20with%20GR "citation")

较新的 CHIME／脉冲星计时分析给出 \(1.806(37)\,M_\odot\)，并讨论旧光学质量估计的系统偏差；同文还概述了最大质量约 \(2.1\)—\(2.5\,M_\odot\) 的多种 EOS 模型。因此，“2.01 倍太阳质量下任何已知核物质状态方程都无法支撑”不能保留为普遍事实。材料若采用旧质量或旧磁场，必须明确版本，不能与现代数据拼成一组 \(10^{-4}\) 精度验证。[Saffer 等，arXiv:2412.02850](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2412.02850v1&text=we%20determine%20a%20pulsar%20mass%20of%201.806(37) "citation"), [24](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/24.jpg "citation")

### 7. 参数和“实证”计数：加总通过，证据口径不通过

- 七组参数数 \(12+15+11+9+18+14+5=84\)，加法正确；未给出 84 个映射和独立推导，不能把数量当内生性证明。
- 五个领域数 \(287+194+219+173+236=1109\)，三个强度档 \(417+392+300=1109\)，且 \(973+136=1109\)，三组加法本身一致。
- 但“已确认实证”标为 973，而领域与强度分项合计均为 1109。如果其中包含 136 个待验证项，就不能同时把全部分项称作已确认；尤其“革命性预言”不应直接计入已确认实证。
- 未提供逐项注册表、原始数据、统计量定义、空模型、系统误差及检验结果，故 \(2.8\sigma\)、\(9.1\sigma\)、\(10\sigma\) 等数字不能登记为统计显著性。[36](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/36.jpg "citation"), [37](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/37.jpg "citation"), [38](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/38.jpg "citation"), [39](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/39.jpg "citation")

### 8. 探测频段与补偿项：真实设施名称不是数据凭证

图 20 将 \(10^{-10}\,\mathrm{Hz}\) 残留背景归于 LIGO–Virgo–KAGRA 历史数据分析。LIGO 官方科普所给连续波搜索示例从自转频率 10 Hz 起，对应引力波 20 Hz，并明确说明更低频率处灵敏度不足；这与 \(10^{-10}\,\mathrm{Hz}\) 相差十个数量级。所述“3σ 一致”没有论文、数据或统计记录支持。[LIGO Scientific Collaboration](kimi-cite://web?url=https%3A%2F%2Fligo.org%2Fscience-summaries%2Fo1allskylowfreq%2F&text=below%20which%20detector%E2%80%99s%20sensitivity%20is%20not%20good%20enough "citation"), [20](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/20.jpg "citation")

图 50 的指数因子 \(\exp[-\tfrac12(\theta_m/\pi)^2]=0.8843312071126088\) 可以计算，但所乘 \(\mathcal K^{(5)}\) 在前文以 \(\mathrm{m^{-2}}\) 标记，因此乘积不是无量纲耦合系数。没有似然、协方差与 WMAP 数据，就不能从 4.1σ 直接升级到 7.9σ，更不能宣称解释了指定多极矩区间的异常。[50](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/50.jpg "citation")

图 51—52 的十一维表达式没有给出作用量、指标约定、五类张力张量定义、耦合量纲、Bianchi 守恒或四维约化，不能登记为闭合场方程。LHC 5.2 TeV、日食三重震荡等句子仍需冻结通道、频率、幅度、时间区间及排除准则；“将发现”不等于已经观测。[51](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/51.jpg "citation"), [52](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/52.jpg "citation"), [53](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/53.jpg "citation")

## 三、非物理叙事与真实凭证的边界

1. 生成文本中的超算控制室、院士反应、全球节点、机构评估与自动认证，不是实验日志或真实机构文件。
2. 图书页数、厚度、数据体量、印刷成本、公司市值、版权收益等没有真实书稿、合同、报价或审计底稿，不进入科研质量和经济价值评估。
3. 生成文本中的政治组织决议、国家财政安排、免税身份和馆藏预留，均没有官方文件支持，不得作为事实传播。
4. 个体年龄、端粒酶、脑结构、IQ、认知能级及营养方案，没有真实测量或医学审查，不是个人资料、临床结果或健康建议；本报告不据此推断作者的身体、智力或身份。
5. 可保留的是虚构场景的创作标记和“虚拟数据”披露，而不是场景中的权威性与结论。文学想象力不转化为物理证据。[28](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/28.jpg "citation"), [35](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/35.jpg "citation"), [47](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/47.jpg "citation"), [48](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/48.jpg "citation"), [49](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/49.jpg "citation")

## 四、53 图逐图索引

| 图 | 主题与处理 |
|---:|---|
| 01 | 特征尺度与屏蔽积分；反解因子不即内生，量纲约定未闭合。[01](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/01.jpg "citation") |
| 02 | 角度参数、核心能量与熵；能量量纲可保留，信息结论未证明。[02](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/02.jpg "citation") |
| 03 | 喷流功率和熵；功率量纲不成立。[03](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/03.jpg "citation") |
| 04 | 喷流准直高度与统治半径；量纲可构造，指数和物理来源未推导。[04](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/04.jpg "citation") |
| 05 | “第一性原理”“可证伪”与新时代宣言；未见拉格朗日量和观测闭环。[05](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/05.jpg "citation") |
| 06 | 超算与学者反应的生成场景；不作真实人物或机构记录。[06](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/06.jpg "citation") |
| 07 | 熵公式与“观测重叠”叙事；无原始曲线和不确定度。[07](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/07.jpg "citation") |
| 08 | MHD 评价和拉格朗日量叙事；无作用量及推导过程。[08](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/08.jpg "citation") |
| 09 | “10σ”及范式转移场景；没有统计模型。[09](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/09.jpg "citation") |
| 10 | 场景总结；情绪表达不登记为证据。[10](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/10.jpg "citation") |
| 11 | 参数簇表前段；先保存分类，不认定收敛。[11](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/11.jpg "citation") |
| 12 | 七组参数数量；84 的加总保留，内生宣称待证。[12](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/12.jpg "citation") |
| 13 | 新参数示例；名称和物理意义不能代替定义与映射。[13](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/13.jpg "citation") |
| 14 | 抽取效率；巨大尺度比下饱和为 0.5，非拟合。[14](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/14.jpg "citation") |
| 15 | \(10^{23}\,\mathrm{Hz}\) 共振峰与参数网络；峰频、幅度和仪器接口未闭合。[15](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/15.jpg "citation") |
| 16 | “98.7% 完备度”；无评分定义，不采用。[16](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/16.jpg "citation") |
| 17 | 3C 273 参数输出；与 M87 分轨，不把生成值当观测。[17](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/17.jpg "citation") |
| 18 | 喷流功率、宽线区、视超光速与 Fe Kα；逐条保留为待检验，不作已验证。[18](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/18.jpg "citation") |
| 19 | 1274 源与 83% 反馈；无样本清单、拟合或留出设计。[19](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/19.jpg "citation") |
| 20 | LVK 的 \(10^{-10}\,\mathrm{Hz}\) 宣称；频段与公开仪器基线不符。[20](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/20.jpg "citation") |
| 21 | 湍流粘滞公式；量纲可闭合，衰减时标未给。[21](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/21.jpg "citation") |
| 22 | 脉冲星磁场与粘滞数值；磁场输入及所印结果均不支持。[22](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/22.jpg "citation") |
| 23 | 全球节点反应场景；不是独立科研复现。[23](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/23.jpg "citation") |
| 24 | 中子星 EOS、晶核与 PTA；纠正磁场和 EOS 绝对命题，其他量待可执行模型。[24](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/24.jpg "citation") |
| 25 | 0.1 ms 抖动与 AI 诊断；没有波形、时序数据或拟合记录。[25](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/25.jpg "citation") |
| 26 | 分项 σ 表；没有观测量、误差和零假设，不采用显著性结论。[26](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/26.jpg "citation") |
| 27 | “最强标准”重新定义；不得用范式口号替代统计定义。[27](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/27.jpg "citation") |
| 28 | 生理年龄和认知增强生成文本；不作健康测量或建议。[28](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/28.jpg "citation") |
| 29 | “超越 IQ”认知评估；不作心理测量或身份判断。[29](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/29.jpg "citation") |
| 30 | 认知维度表；术语映射不构成神经科学证据。[30](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/30.jpg "citation") |
| 31 | IQ 等效数字与大脑描述；无真实测量，排除出证据栏。[31](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/31.jpg "citation") |
| 32 | 脑活动相似性、时间反演和历史定位；全部缺可核验证定义。[32](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/32.jpg "citation") |
| 33 | 历史人物比较与特殊能力；不作个人或科学史排名。[33](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/33.jpg "citation") |
| 34 | 历史定位续页；与图 33 内容重复，不重复计证。[34](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/34.jpg "citation") |
| 35 | 新认知单位与自动勋章；生成创作，不是学术认证。[35](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/35.jpg "citation") |
| 36 | “973 实证、136 待验”及领域表前段；保留计数口径检查。[36](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/36.jpg "citation") |
| 37 | 领域及强度数量；合计均为 1109，不等于 973 个独立实证。[37](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/37.jpg "citation") |
| 38 | 领域及强度数量续页；预测项不得计入确认实证。[38](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/38.jpg "citation") |
| 39 | 实证网络与历史比较；比较单位不统一，σ 无原始统计。[39](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/39.jpg "citation") |
| 40 | “千证”与自动认证；对话次数和文本数量不等于独立实验数。[40](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/40.jpg "citation") |
| 41 | 认证续页及出版规划；不登记为真实纪录或书稿完成。[41](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/41.jpg "citation") |
| 42 | 字符数、数据量和页面规划；缺实际书稿、编码口径与数据目录。[42](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/42.jpg "citation") |
| 43 | 页数、载体和历史比较；生产设想不是研究成果。[43](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/43.jpg "citation") |
| 44 | 页数、厚度和重量续页；可作印刷设想，不证明理论价值。[44](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/44.jpg "citation") |
| 45 | 分卷、环保及动态出版建议；须另行工程和环境评估。[45](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/45.jpg "citation") |
| 46 | 动态出版与馆藏预留叙事；无真实机构凭证。[46](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/46.jpg "citation") |
| 47 | 出版成本与公司市值；没有报价、审计或估值模型，不采用。[47](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/47.jpg "citation") |
| 48 | 国际财政、知识产权及补偿安排；无官方文件，不作事实。[48](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/48.jpg "citation") |
| 49 | 富翁与政治组织模拟；不登记为真实资产、决议或免税安排。[49](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/49.jpg "citation") |
| 50 | 五维曲率补偿与 WMAP；因子有量纲，σ 升级没有推导。[50](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/50.jpg "citation") |
| 51 | 五重“膜”及十一维表达式；缺作用量、指标、耦合与守恒闭合。[51](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/51.jpg "citation") |
| 52 | 新增方程与 LHC 预言；没有张量定义和可观测通道。[52](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/52.jpg "citation") |
| 53 | 日食预言与最终完成宣言；时间和观测量未冻结，不升级为实证。[53](C:/Users/一梦/Documents/kimi/workspace/tieba_observer_audit/images/10238581618/53.jpg "citation") |

本帖 53 图与已登记图片的文件级哈希比对未发现逐字节完全重复；部分页面存在内容重叠，仍只按同一组生成材料处理，不重复累计证据。

## 五、`M87-GR-MHD-Evidence-Gate` 整改立项

**当前状态**：本帖 53 图及两页评论审查完成；9 项专项检查通过；没有 M87 实证升级。

**下一项最小工作**：停止使用 M87、3C 273 和脉冲星之间的互相背书。先只在 M87 问题上冻结同一版 \(\lambda_c\)、黑洞质量、磁场、面积和效率定义，修正喷流功率量纲，并与一个公开的 Kerr／MHD 基线比较。PSR J0348+0432 则另按已发表磁场和质量版本建立独立账本。

**进入真实数据前的门槛**：公开公式、参数、单位、代码、原始数据、拟合与不确定度；预先规定留出样本和失败条件；给出可证伪观测量，而非只给“一致”字样。

**停止条件**：若屏蔽因子、功率量纲和衰减时标不能独立闭合，停止“宇宙级实证”“国家科学中心顶级验证”“10σ”等表述。虚构内容可继续作为文学创作，但必须与科研材料分开发布。

**禁止的跳跃**：把生成数字当实验输出，把人物反应当同行评议，把论文或探测器名称当已做数据分析，把旧观测值当永恒真值，把财富、政治和健康叙事当科学证据。

## 六、验证与覆盖

- `python -m unittest tests.test_m87_evidence_claim_checks -v`：9 项通过；
- `python -m unittest discover -s tests -p "test_*.py" -v`：325 项通过；
- 档案侧年度及图片门禁：28 项通过；
- 覆盖生成器复核：累计 107 帖、2103 图；2025 年已审 1270／4862 图，仍有 3592 图待审。

这些测试只证明本报告列出的算术、口径和证据边界通过检查，不验证任何新物理理论。`readyForTraining=false`，方法卡和本报告不是训练许可、事实数据库或真实用户替身。
